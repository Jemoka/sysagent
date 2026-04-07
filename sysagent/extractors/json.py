import json

from sysagent.extractors.common import flatten_structured_data, read_text_file


def _extract_json(path):
    return flatten_structured_data(json.loads(read_text_file(path)))
