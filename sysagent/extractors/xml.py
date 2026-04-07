import xml.etree.ElementTree as ET


def _extract_xml(path):
    tree = ET.parse(path)
    return "\n".join(text.strip() for text in tree.getroot().itertext() if text.strip())
