import tomllib

from sysagent.extractors.common import flatten_structured_data, read_text_file


def _extract_toml(path):
    return flatten_structured_data(tomllib.loads(read_text_file(path)))
