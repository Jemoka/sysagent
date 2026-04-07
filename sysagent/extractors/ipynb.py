import json

from sysagent.extractors.common import read_text_file


def _extract_ipynb(path):
    notebook = json.loads(read_text_file(path))
    parts = []

    for index, cell in enumerate(notebook.get("cells", []), start=1):
        source = "".join(cell.get("source", []))
        source = source.strip()
        if not source:
            continue

        cell_type = cell.get("cell_type", "cell")
        parts.append(f"# {cell_type} {index}\n{source}")

    return "\n\n==========\n\n".join(parts)
