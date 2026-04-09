import binascii
import json
from pathlib import Path

import nltk
from nltk.tokenize import TextTilingTokenizer
from tqdm import tqdm
import xapian

from sysagent.extractors import (
    EXTRACTORS, TEXT_FILE_SUFFIXES,
    read_text_file as _read_text_file,
    _extract_pdf_page, _pdf_page_count,
)

nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
_tiler = TextTilingTokenizer()


def _chunk_text(text):
    try:
        chunks = _tiler.tokenize(text)
    except ValueError:
        chunks = [text]
    return [c.strip() for c in chunks if c.strip()]


class DB:
    def __init__(self, path):
        self.db = xapian.WritableDatabase(str(path), xapian.DB_CREATE_OR_OPEN)
        self.qp = xapian.QueryParser()
        self.qp.set_stemmer(xapian.Stem("en"))
        self.qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
        self.qp.set_database(self.db)  # needed for wildcard expansion
        self.qp.add_prefix("title", "S")
        self.qp.add_prefix("author", "A")

        self.flags = (
            xapian.QueryParser.FLAG_BOOLEAN |        # AND, OR, NOT
            xapian.QueryParser.FLAG_PHRASE |          # "exact phrase"
            xapian.QueryParser.FLAG_LOVEHATE |        # +required -excluded
            xapian.QueryParser.FLAG_WILDCARD |        # prefix*
            xapian.QueryParser.FLAG_PARTIAL            # partial matching
        )

    def close(self):
        self.db.close()

    def _index_chunks(self, title, chunks, metadata=None):
        total_chunks = len(chunks)
        metadata = metadata or {}

        for i, chunk in enumerate(chunks):
            hash_value = binascii.crc32((title + chunk).encode("utf-8")) % (1 << 32)
            doc_id = f"Q{hash_value}"

            doc = xapian.Document()
            termgen = xapian.TermGenerator()
            termgen.set_stemmer(xapian.Stem("en"))
            termgen.set_document(doc)

            termgen.index_text(title, 1, "S")
            termgen.index_text(chunk)

            doc.add_boolean_term(doc_id)
            doc.set_data(
                json.dumps(
                    {
                        "title": title,
                        "hash": hash_value,
                        "metadata": {
                            **metadata,
                            "chunks": {
                                "chunk": i,
                                "total_chunks": total_chunks,
                            },
                        },
                        "text": chunk,
                    }
                )
            )

            self.db.replace_document(doc_id, doc)

        return total_chunks

    def _extract_text(self, path):
        suffix = path.suffix.lower()
        if suffix in TEXT_FILE_SUFFIXES:
            return _read_text_file(path)

        extractor = EXTRACTORS.get(suffix)
        if extractor:
            return extractor(path)

        raise ValueError(f"Unsupported file type for indexing: {suffix or path.name}")

    def _cache_dir(self, path):
        file_hash = binascii.crc32(path.read_bytes()) % (1 << 32)
        return path.parent / ".chunks" / f"{path.name}.{file_hash:08x}"

    def _load_or_cache_chunks(self, cache_dir, extract_fn):
        if cache_dir.is_dir():
            return [f.read_text(encoding="utf-8") for f in sorted(cache_dir.glob("*.md"))]

        text = extract_fn()
        chunks = _chunk_text(text)
        cache_dir.mkdir(parents=True, exist_ok=True)
        for i, chunk in enumerate(chunks):
            (cache_dir / f"{i:04d}.md").write_text(chunk, encoding="utf-8")
        return chunks

    def index(self, path, metadata=None):
        path = Path(path)

        if path.suffix.lower() == ".pdf":
            return self._index_pdf(path, metadata)

        cache_dir = self._cache_dir(path)
        chunks = self._load_or_cache_chunks(cache_dir, lambda: self._extract_text(path))
        return self._index_chunks(path.stem, chunks, metadata)

    def _index_pdf(self, path, metadata=None):
        n_pages = _pdf_page_count(path)
        total_indexed = 0
        metadata = metadata or {}

        for page_num in tqdm(range(n_pages), desc=path.name, unit="pg"):
            page_cache = self._cache_dir(path) / f"p{page_num:04d}"
            page_title = f"{path.stem} (p{page_num + 1})"

            chunks = self._load_or_cache_chunks(
                page_cache, lambda pn=page_num: _extract_pdf_page(path, pn)
            )
            page_meta = {**metadata, "page": page_num + 1, "total_pages": n_pages}
            total_indexed += self._index_chunks(page_title, chunks, page_meta)

        return total_indexed

    def index_dir(self, path, metadata=None):
        path = Path(path)
        supported = TEXT_FILE_SUFFIXES | set(EXTRACTORS)
        files = [
            f for f in path.rglob("*")
            if f.is_file() and f.suffix.lower() in supported and ".chunks" not in f.parts
        ]
        for file in tqdm(files, desc="Indexing", unit="file"):
            self._index_one(file, metadata)
        return len(files)

    def _index_one(self, path, metadata=None):
        try:
            self.index(path, metadata)
        except Exception as e:
            import warnings
            warnings.warn(f"Skipping {path}: {e}")

    def search(self, query_str, limit=16):
        qp = xapian.QueryParser()
        qp.set_stemmer(xapian.Stem("en"))
        qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

        qp.set_database(self.db)

        qp.add_prefix("title", "S")
        qp.add_prefix("author", "A")

        flags = (
            xapian.QueryParser.FLAG_BOOLEAN |        # AND, OR, NOT
            xapian.QueryParser.FLAG_PHRASE |          # "exact phrase"
            xapian.QueryParser.FLAG_LOVEHATE |        # +required -excluded
            xapian.QueryParser.FLAG_WILDCARD |        # prefix*
            xapian.QueryParser.FLAG_PARTIAL            # partial matching
        )
        query = qp.parse_query(query_str, flags)

        results = []
        query = self.qp.parse_query(query_str, self.flags)

        enq = xapian.Enquire(self.db)
        enq.set_query(query)
        for match in enq.get_mset(0, limit):
            data = json.loads(match.document.get_data())
            results.append(data)

        return results

