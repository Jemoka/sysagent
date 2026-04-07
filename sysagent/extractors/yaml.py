import yaml

from sysagent.extractors.common import flatten_structured_data, read_text_file


def _extract_yaml(path):
    return flatten_structured_data(yaml.safe_load(read_text_file(path)))
