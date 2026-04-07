import json
import xapian
import binascii
from pathlib import Path

import pdfplumber

class DB:
    def __init__(self, path):
        self.db = xapian.WritableDatabase(path, xapian.DB_CREATE_OR_OPEN)

    def _index_text(self, title, text, metadata={}):
        hash = binascii.crc32((title+text).encode()) % (1<<32)
        id = "Q" + hash # for some reason for idempotency xapian requires "Q" prefix

        doc = xapian.Document()
        termgen = xapian.TermGenerator()
        termgen.set_stemmer(xapian.Stem("en"))
        termgen.set_document(doc)

        termgen.index_text(title, 1, "S")  # S = subject/title
        termgen.index_text(text)

        doc.add_boolean_term(id)

        doc.set_data(json.dumps({
            "title": title,
            "hash": hash,
            "metadata": metadata or {},
        }))

        return self.db.replace_document(id, doc)

    def index(self, path, metadata={}):
        # detect the magic file name
        # if filename_stem.extracted.[file_hash].txt exists,
        # use that
        path = Path(path)
        file_hash = binascii.crc32(path.read_bytes()) % (1<<32)
        cache_file = path.parent / f"{path.stem}.extracted.{file_hash}.txt"

        if cache_file.exists():
            text = cache_file.read_text()
            return self._index_text(path.stem, text, metadata)

        # otherwise, extract text and cache it based on extension
        if path.suffix == ".pdf":
            # extract text from pdf
            with pdfplumber.open(path) as pdf:
                document = f"\n\n==========\n\n".join(
                    f"# page {idx}\n" + (page.extract_text() or "")
                    for idx, page in enumerate(pdf.pages)
                )
            cache_file.write_text(document)
            # this should find the cache file we just wrote and index it
            return self.index(path, metadata)



            
            
