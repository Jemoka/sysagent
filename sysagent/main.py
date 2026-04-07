from pathlib import Path

from sysagent.search_mcp import make_mcp

DB_PATH = Path("~/Downloads/aaaa").expanduser()


def main():
    mcp = make_mcp(DB_PATH)
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
