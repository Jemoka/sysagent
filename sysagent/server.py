import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from mcp.server.fastmcp import FastMCP, Context

from sysagent.db import DB

DB_PATH = Path("~/.local/share/sysagent/db").expanduser()


@asynccontextmanager
async def lifespan(app: FastMCP):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = DB(DB_PATH)
    yield db


mcp = FastMCP("sysagent", lifespan=lifespan)


def _get_db(ctx: Context) -> DB:
    return ctx.request_context.lifespan_context


@mcp.tool()
async def search(query: str, limit: int = 16, ctx: Context = None) -> list[dict]:
    """Search the index for documents matching a query.

    Supports boolean operators (AND, OR, NOT), quoted phrases,
    +required/-excluded terms, prefix wildcards, and field
    prefixes (title:, author:).

    Args:
        query: Search query string.
        limit: Maximum number of results to return.
    """
    db = _get_db(ctx)
    return await asyncio.to_thread(db.search, query, limit)


@mcp.tool()
async def index_file(path: str, ctx: Context = None) -> str:
    """Extract text from a file, chunk it, and add it to the search index.

    Supported formats: PDF, DOCX, PPTX, XLSX, CSV/TSV, HTML, JSON, YAML,
    TOML, XML, Jupyter notebooks, and plain text files.

    Args:
        path: Absolute path to the file to index.
    """
    db = _get_db(ctx)
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        return f"Error: {p} is not a file."
    n = await asyncio.to_thread(db.index, p)
    return f"Indexed {p.name} ({n} chunks)."


@mcp.tool()
async def index_directory(path: str, ctx: Context = None) -> str:
    """Recursively index all supported files in a directory.

    Args:
        path: Absolute path to the directory to index.
    """
    db = _get_db(ctx)
    p = Path(path).expanduser().resolve()
    if not p.is_dir():
        return f"Error: {p} is not a directory."
    n = await asyncio.to_thread(db.index_dir, p)
    return f"Indexed {n} files from {p}."


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
