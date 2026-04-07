TEXT_FILE_SUFFIXES = {
    ".c",
    ".cc",
    ".cfg",
    ".conf",
    ".cpp",
    ".css",
    ".go",
    ".h",
    ".hpp",
    ".ini",
    ".java",
    ".js",
    ".jsonl",
    ".kt",
    ".log",
    ".md",
    ".py",
    ".rb",
    ".rs",
    ".rst",
    ".sh",
    ".sql",
    ".swift",
    ".tex",
    ".ts",
    ".tsx",
    ".txt",
}


def _iter_text_fragments(value):
    if value is None:
        return

    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key).strip()
            if isinstance(item, (dict, list, tuple, set)):
                if key_text:
                    yield key_text
                yield from _iter_text_fragments(item)
                continue

            item_text = str(item).strip()
            if key_text and item_text:
                yield f"{key_text}: {item_text}"
            elif key_text:
                yield key_text
            elif item_text:
                yield item_text
        return

    if isinstance(value, (list, tuple, set)):
        for item in value:
            yield from _iter_text_fragments(item)
        return

    text = str(value).strip()
    if text:
        yield text


def flatten_structured_data(value):
    return "\n".join(_iter_text_fragments(value))


def read_text_file(path):
    return path.read_text(encoding="utf-8", errors="replace")
