from sysagent.extractors.common import TEXT_FILE_SUFFIXES, read_text_file
from sysagent.extractors.csv import _extract_csv
from sysagent.extractors.docx import _extract_docx
from sysagent.extractors.html import _extract_html
from sysagent.extractors.ipynb import _extract_ipynb
from sysagent.extractors.json import _extract_json
from sysagent.extractors.pdf import _extract_pdf, _extract_pdf_page, _pdf_page_count
from sysagent.extractors.pptx import _extract_pptx
from sysagent.extractors.toml import _extract_toml
from sysagent.extractors.xlsx import _extract_xlsx
from sysagent.extractors.xml import _extract_xml
from sysagent.extractors.yaml import _extract_yaml


EXTRACTORS = {
    ".csv": _extract_csv,
    ".docx": _extract_docx,
    ".htm": _extract_html,
    ".html": _extract_html,
    ".ipynb": _extract_ipynb,
    ".json": _extract_json,
    ".pdf": _extract_pdf,
    ".pptx": _extract_pptx,
    ".toml": _extract_toml,
    ".tsv": _extract_csv,
    ".xlsx": _extract_xlsx,
    ".xml": _extract_xml,
    ".yaml": _extract_yaml,
    ".yml": _extract_yaml,
}


__all__ = ["EXTRACTORS", "TEXT_FILE_SUFFIXES", "read_text_file", "_extract_pdf_page", "_pdf_page_count"]
