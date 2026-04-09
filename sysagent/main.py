import argparse
from pathlib import Path

from sysagent.search_mcp import make_mcp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path, help="path to the index database")
    parser.add_argument("--index", type=Path, metavar="FOLDER",
                        help="index a folder into the database and exit")
    args = parser.parse_args()

    target = args.target.expanduser()

    if args.index:
        from sysagent.db import DB
        database = DB(str(target))
        database.index_dir(str(args.index.expanduser()))
    else:
        mcp = make_mcp(target)
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
