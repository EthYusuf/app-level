"""Key-free MCP tools that prepare app-research and device-shopping links."""

from __future__ import annotations

import os
from typing import Any, Literal
from urllib.parse import urlencode

from mcp.server.fastmcp import FastMCP

SERVER_NAME = "app-level"
GOOGLE_SEARCH_URL = "https://www.google.com/search"
BING_SEARCH_URL = "https://www.bing.com/search"
TRENDYOL_SEARCH_URL = "https://www.trendyol.com/sr"

mcp = FastMCP(SERVER_NAME)


def _search_links(query: str, purpose: str) -> list[dict[str, str]]:
    return [
        {
            "provider": provider,
            "purpose": purpose,
            "query": query,
            "url": f"{search_url}?{urlencode({'q': query})}",
        }
        for provider, search_url in (
            ("Google", GOOGLE_SEARCH_URL),
            ("Bing", BING_SEARCH_URL),
        )
    ]


@mcp.tool()
def research_app_requirements(
    app_name: str,
    platform: Literal["auto", "mobile", "computer"] = "auto",
) -> dict[str, Any]:
    """Prepare browser-search links for app requirements and low-settings research.

    The MCP server does not fetch the web. An MCP host with browsing capability
    can open these links, verify sources, and summarize the findings.
    """
    app_name = app_name.strip()
    if not app_name:
        raise ValueError("app_name must not be empty.")
    if len(app_name) > 120:
        raise ValueError("app_name must be 120 characters or fewer.")

    platform_query = {
        "auto": "PC Windows Android iOS",
        "mobile": "Android iOS",
        "computer": "PC Windows",
    }[platform]
    official_query = (
        f'"{app_name}" {platform_query} official minimum system requirements'
    )
    settings_query = (
        f'"{app_name}" {platform_query} lowest settings performance requirements'
    )
    store_query = f'"{app_name}" {platform_query} app store requirements'
    return {
        "app_name": app_name,
        "platform": platform,
        "research_links": [
            *_search_links(official_query, "official_requirements"),
            *_search_links(settings_query, "low_settings"),
            *_search_links(store_query, "store_listings"),
        ],
        "notice": (
            "These are search links, not fetched or verified results. Open them "
            "in the MCP host's browser, cite the source URLs, and prefer the "
            "publisher's official requirements."
        ),
    }


@mcp.tool()
def search_trendyol_devices(
    search_terms: str,
    device_type: Literal["phone", "laptop"] = "phone",
    minimum_ram_gb: int | None = None,
    minimum_storage_gb: int | None = None,
    budget_try: int | None = None,
) -> dict[str, Any]:
    """Prepare Trendyol and web-search links for a device shortlist.

    The MCP server does not fetch listings. An MCP host with browsing capability
    can open links and check product pages, sellers, prices, and specifications.
    """
    search_terms = search_terms.strip()
    if not search_terms:
        raise ValueError("search_terms must not be empty.")
    if len(search_terms) > 160:
        raise ValueError("search_terms must be 160 characters or fewer.")
    if minimum_ram_gb is not None and minimum_ram_gb < 1:
        raise ValueError("minimum_ram_gb must be at least 1.")
    if minimum_storage_gb is not None and minimum_storage_gb < 1:
        raise ValueError("minimum_storage_gb must be at least 1.")
    if budget_try is not None and budget_try < 1:
        raise ValueError("budget_try must be at least 1.")

    device_label = "akıllı telefon" if device_type == "phone" else "dizüstü bilgisayar"
    constraints = [device_label, search_terms]
    if minimum_ram_gb is not None:
        constraints.append(f"{minimum_ram_gb} GB RAM")
    if minimum_storage_gb is not None:
        constraints.append(f"{minimum_storage_gb} GB depolama")
    if budget_try is not None:
        constraints.append(f"{budget_try} TL altı")

    terms = " ".join(constraints)
    marketplace_url = f"{TRENDYOL_SEARCH_URL}?{urlencode({'q': terms})}"
    web_query = f"site:trendyol.com {terms}"
    return {
        "marketplace": "Trendyol",
        "search_terms": terms,
        "search_url": marketplace_url,
        "research_links": _search_links(web_query, "marketplace_listings"),
        "notice": (
            "These are search links, not fetched listings. Verify the exact "
            "model, seller, price, and specifications on each product page."
        ),
    }


def main() -> None:
    """Run over stdio locally or Streamable HTTP for a remote MCP client."""
    transport = os.environ.get("APP_LEVEL_TRANSPORT", "stdio")
    if transport not in {"stdio", "streamable-http"}:
        raise ValueError("APP_LEVEL_TRANSPORT must be stdio or streamable-http.")

    host = os.environ.get("APP_LEVEL_HOST", "127.0.0.1")
    try:
        port = int(os.environ.get("APP_LEVEL_PORT", "8000"))
    except ValueError as exc:
        raise ValueError("APP_LEVEL_PORT must be an integer.") from exc
    if not 1 <= port <= 65535:
        raise ValueError("APP_LEVEL_PORT must be between 1 and 65535.")

    mcp.settings.host = host
    mcp.settings.port = port
    allowed_hosts = os.environ.get("APP_LEVEL_ALLOWED_HOSTS")
    if allowed_hosts:
        hosts = [
            item.strip() for item in allowed_hosts.split(",") if item.strip()
        ]
        if not hosts:
            raise ValueError("APP_LEVEL_ALLOWED_HOSTS must contain a host.")
        mcp.settings.transport_security.allowed_hosts = hosts
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
