"""MCP tools for researching app requirements and compatible devices."""

from __future__ import annotations

import json
import os
from typing import Any, Literal
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from mcp.server.fastmcp import FastMCP

SERVER_NAME = "app-level"
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
TRENDYOL_SEARCH_URL = "https://www.trendyol.com/sr"
MAX_RESULTS_LIMIT = 10

mcp = FastMCP(SERVER_NAME)


def _validate_search_options(max_results: int) -> None:
    if not 1 <= max_results <= MAX_RESULTS_LIMIT:
        raise ValueError(f"max_results must be between 1 and {MAX_RESULTS_LIMIT}.")


def _search_web(query: str, max_results: int) -> list[dict[str, str]]:
    api_key = os.environ.get("BRAVE_SEARCH_API_KEY")
    if not api_key:
        raise RuntimeError(
            "BRAVE_SEARCH_API_KEY is not set. Add a Brave Search API key "
            "to enable web research."
        )

    params = urlencode(
        {
            "q": query,
            "count": max_results,
            "country": "TR",
            "search_lang": "tr",
            "safesearch": "moderate",
        }
    )
    request = Request(
        f"{BRAVE_SEARCH_URL}?{params}",
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
            "User-Agent": "app-level-mcp/1.0",
        },
    )

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(
            f"Brave Search returned HTTP {exc.code}; check the API key and quota."
        ) from exc
    except URLError as exc:
        raise RuntimeError(f"Brave Search request failed: {exc.reason}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Brave Search returned an invalid JSON response.") from exc

    web_results = payload.get("web", {}).get("results", [])
    results: list[dict[str, str]] = []
    for item in web_results[:max_results]:
        url = item.get("url")
        title = item.get("title")
        if not isinstance(url, str) or not url.startswith("https://"):
            continue
        if not isinstance(title, str):
            continue
        description = item.get("description", "")
        results.append(
            {
                "title": title,
                "url": url,
                "description": description
                if isinstance(description, str)
                else "",
            }
        )
    return results


@mcp.tool()
def research_app_requirements(
    app_name: str,
    platform: Literal["auto", "mobile", "computer"] = "auto",
    max_results: int = 5,
) -> dict[str, Any]:
    """Find sourced minimum requirements and low-settings information for an app or game.

    Returns web search result snippets and source links for manual verification;
    it does not invent or guarantee hardware requirements.
    """
    app_name = app_name.strip()
    if not app_name:
        raise ValueError("app_name must not be empty.")
    if len(app_name) > 120:
        raise ValueError("app_name must be 120 characters or fewer.")
    _validate_search_options(max_results)

    platform_query = {
        "auto": "PC Windows Android iOS",
        "mobile": "Android iOS",
        "computer": "PC Windows",
    }[platform]
    query = (
        f'"{app_name}" {platform_query} minimum system requirements '
        '"lowest settings" recommended hardware'
    )
    return {
        "app_name": app_name,
        "platform": platform,
        "query": query,
        "sources": _search_web(query, max_results),
        "notice": (
            "Search snippets are leads, not verified specifications. Open the "
            "sources and prefer the app publisher's official requirements."
        ),
    }


@mcp.tool()
def search_trendyol_devices(
    search_terms: str,
    device_type: Literal["phone", "laptop"] = "phone",
    minimum_ram_gb: int | None = None,
    minimum_storage_gb: int | None = None,
    budget_try: int | None = None,
    max_results: int = 5,
) -> dict[str, Any]:
    """Search Trendyol for devices using requirement-derived terms and constraints.

    Search results are third-party listings; confirm current price, exact model,
    specifications, and seller details on Trendyol before making a decision.
    """
    search_terms = search_terms.strip()
    if not search_terms:
        raise ValueError("search_terms must not be empty.")
    if len(search_terms) > 160:
        raise ValueError("search_terms must be 160 characters or fewer.")
    _validate_search_options(max_results)
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
    query = f"site:trendyol.com {terms}"
    return {
        "marketplace": "Trendyol",
        "search_terms": terms,
        "search_url": marketplace_url,
        "sources": _search_web(query, max_results),
        "notice": (
            "Listings and snippets can be stale or incomplete. Verify the exact "
            "model, seller, price, and specifications on the linked product page."
        ),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
