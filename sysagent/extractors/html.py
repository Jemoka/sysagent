from bs4 import BeautifulSoup

from sysagent.extractors.common import read_text_file


def _extract_html(path):
    soup = BeautifulSoup(read_text_file(path), "html.parser")
    return soup.get_text("\n", strip=True)
