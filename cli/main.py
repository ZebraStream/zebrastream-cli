# SPDX-License-Identifier: GPL-3.0-or-later
"""ZebraStream CLI main module."""
import datetime
import os
import time
from typing import Optional

import typer
from rich import print
from rich.table import Table

from api_client import AuthenticatedClient
from api_client.api.default import (
    accesstoken_create,
    accesstoken_delete,
    accesstoken_list,
    usage_show,
)

# TODO: simplify
from api_client.models.body_create_access_token_v0_accesstoken_create_post import (
    BodyCreateAccessTokenV0AccesstokenCreatePost as CreateTokenBody,
)
from api_client.models.body_delete_access_token_v0_accesstoken_delete_post import (
    BodyDeleteAccessTokenV0AccesstokenDeletePost as DeleteTokenBody,
)

DEFAULT_BASE_URL = "https://api.zebrastream.io"

app = typer.Typer()


def get_client(api_key: Optional[str] = None) -> AuthenticatedClient:
    """Get an authenticated API client."""
    if not api_key:
        api_key = os.getenv("ZEBRASTREAM_API_KEY")
    if not api_key:
        raise typer.BadParameter("API key is required. Set ZEBRASTREAM_API_KEY or use --api-key")
    base_url = os.getenv("ZEBRASTREAM_API_URL", DEFAULT_BASE_URL)
    return AuthenticatedClient(base_url=base_url, token=api_key)

@app.command()
def create_token(
    path: str = typer.Option(..., help="Path for the token (e.g. /some/path)"),
    access_mode: str = typer.Option(..., help="Access mode (e.g. read, write)"),
    expires: str = typer.Option(..., help="Expiration as ISO 8601 datetime (e.g. 2025-07-01 or 2025-07-01T12:34:56)."),
    recursive: bool = typer.Option(False, help="Whether the token is recursive (default: False)"),
    api_key: Optional[str] = typer.Option(None, help="API key (optional if ZEBRASTREAM_API_KEY is set)")
) -> None:
    """Create a new access token."""
    client = get_client(api_key)
    expires_ts = None
    if expires:
        try:
            dt = datetime.datetime.fromisoformat(expires)
            expires_ts = int(dt.timestamp())
        except Exception:
            typer.echo("[red]Invalid date format for --expires. Use ISO 8601, e.g. 2025-07-01 or 2025-07-01T12:34:56[/red]")
            raise typer.Exit(1)
    body = CreateTokenBody(
        path=path,
        access_mode=access_mode,
        expires=expires_ts,
        recursive=recursive
    )
    response = accesstoken_create.sync(client=client, body=body)
    table = Table(title="Created Access Token")
    table.add_column("Token ID")
    table.add_column("Path")
    table.add_column("Token")
    table.add_row(
        response["token_id"],
        response["path"],
        response["token"],
    )
    print(table)

@app.command()
def list_tokens(
    api_key: Optional[str] = typer.Option(None, help="API key (optional if ZEBRASTREAM_API_KEY is set)")
) -> None:
    """List all access tokens."""
    client = get_client(api_key)
    tokens = accesstoken_list.sync(client=client)

    table = Table(title="Access Tokens")
    table.add_column("Token ID")
    table.add_column("Path")
    table.add_column("Access Mode")
    table.add_column("Recursive")
    table.add_column("Expires")

    now = int(time.time())
    for token in tokens:
        expires_ts = token.get("expires")
        if expires_ts:
            expires_str = datetime.datetime.fromtimestamp(expires_ts).strftime("%Y-%m-%d %H:%M:%S")
            if expires_ts < now:
                expires_str = f"[red]{expires_str}[/red]"
        else:
            expires_str = ""
        table.add_row(
            token["id"],
            token["path"],
            token["access_mode"],
            "✓" if token.get("recursive") else "✗",
            expires_str
        )
    print(table)


@app.command()
def delete_token(
    token_id: str = typer.Option(..., help="ID of the token to delete (e.g. key_xxxxxxxxxxxxxxxx)"),
    api_key: Optional[str] = typer.Option(None, help="API key (optional if ZEBRASTREAM_API_KEY is set)")
) -> None:
    """Delete an access token."""
    client = get_client(api_key)
    accesstoken_delete.sync(client=client, body=DeleteTokenBody(token_id=token_id))
    print(f"Token '{token_id}' deleted successfully")


@app.command()
def show_usage(
    month: Optional[str] = typer.Option(None, help="Month in YYYY-MM format (e.g. 2025-06)"),
    api_key: Optional[str] = typer.Option(None, help="API key (optional if ZEBRASTREAM_API_KEY is set)")
) -> None:
    """Show usage statistics."""
    client = get_client(api_key)
    usage = usage_show.sync(client=client, month=month) if month else usage_show.sync(client=client)

    def format_bytes(size):
        # Human-readable bytes conversion
        for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"

    table = Table(title="Usage Statistics")
    table.add_column("Month")
    table.add_column("Volume (bytes)")
    table.add_column("Volume (human)")

    table.add_row(
        usage["month"],
        str(usage["volume_bytes"]),
        format_bytes(usage["volume_bytes"])
    )
    print(table)

def main() -> None:
    app()

if __name__ == "__main__":
    main()
