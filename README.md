# sysagent

A local document search engine exposed as an MCP server. Indexes files into a [Xapian](https://xapian.org/) database and provides full-text search via the [Model Context Protocol](https://modelcontextprotocol.io/).

## Supported formats

PDF, DOCX, PPTX, XLSX, CSV/TSV, HTML, JSON, YAML, TOML, XML, Jupyter notebooks, and plain text.

## Requirements

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/)
- Xapian (with Python bindings)

## Setup

```bash
git clone <repo-url> && cd sysagent
uv sync
```

## Usage

### Index a folder

```bash
uv run sysagent /path/to/index_db --index /path/to/documents/
```

This recursively indexes all supported files in the given folder into the Xapian database at `/path/to/index_db`, then exits.

### Start the MCP server

```bash
uv run sysagent /path/to/index_db
```

Starts an MCP server over stdio. The server exposes three tools:

- **search** -- full-text search with boolean operators, quoted phrases, `+required`/`-excluded` terms, and field prefixes (`title:`, `author:`).
- **index_file** -- index a single file into the database.
- **index_directory** -- recursively index a directory.

### Claude Desktop configuration

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sysagent": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/sysagent", "sysagent", "/path/to/index_db"]
    }
  }
}
```
