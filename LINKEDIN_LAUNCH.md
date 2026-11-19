# LinkedIn Launch Document

## App-level: A Key-Free MCP Workflow for App Requirements and Device Discovery

**Project:** [github.com/EthYusuf/app-level](https://github.com/EthYusuf/app-level)

**License:** MIT

**Format:** Model Context Protocol (MCP) server with local stdio and optional Streamable HTTP transport

---

## The idea

Choosing a device for an app or game often means piecing together information from several places: publisher support pages, app-store listings, benchmark discussions, and product listings. Minimum requirements can be confused with recommended specifications, while marketplace listings may omit the exact model or configuration that matters.

AI assistants can make this research easier to organize, but only when their answers are grounded in sources. They should not guess a GPU, promise a frame rate, or call a device compatible simply because a search snippet looks plausible.

**app-level** is a small, open-source MCP project designed to help structure that research. It gives an MCP-capable assistant focused search links for application requirements and device listings, then lets the assistant's own browsing tools do the source review.

The project is intentionally transparent about its boundary: **the MCP server generates links; it does not fetch or verify live search results.** A connected assistant needs web access to open those links and produce a sourced report. Without browsing, it can still return the links, but it cannot perform live research.

## A simple, two-stage workflow

### 1. Find the requirements

Call `research_app_requirements` with an app or game name and a target platform. The tool prepares Google and Bing links for:

- Official minimum system requirements.
- Low-settings and performance information.
- App-store or publisher listings.

For example:

```text
research_app_requirements(
  app_name="Minecraft: Java Edition",
  platform="computer"
)
```

The assistant can then open relevant sources, identify the exact edition and platform, and report only the specifications those sources actually state. Minimum and recommended requirements should remain separate, and uncertain or unavailable details should be labeled as unknown.

### 2. Explore device listings

Once the requirements have been verified, call `search_trendyol_devices` with the known device category and useful constraints:

```text
search_trendyol_devices(
  search_terms="RTX 4060",
  device_type="laptop",
  minimum_ram_gb=16,
  minimum_storage_gb=512,
  budget_try=50000
)
```

The tool returns a direct Trendyol search link and Google/Bing links for Trendyol listings. If the assistant can browse, it can inspect candidate product pages and compare the exact model, listed specifications, seller, and current price against the sourced app requirements.

The result is a research path, not an automatic buying recommendation. A product listing can be incomplete or change after it has been found, so the exact configuration and seller details still need to be checked before purchase.

## Why make it key-free?

Many search-backed integrations ask every user to create and manage a separate search API key. That can add setup friction, quota considerations, and another service to configure.

app-level takes a lighter approach: it generates links to public search pages and does not send queries to a search API itself. There is no Brave Search account, API key, or paid search service required for the MCP server.

This design also makes the responsibility clear:

1. **app-level prepares the search links.**
2. **The MCP host or assistant opens them**, if it has browsing capability.
3. **The assistant cites the pages it actually reviewed.**
4. **The user confirms time-sensitive product details** on the listing page.

The browser or host still communicates with whichever sites the user opens. “Key-free” does not mean “offline,” and it does not mean that search providers never receive a query.

## Built around evidence, not guesses

The project includes reusable agent skills to encourage careful research:

- **App Requirements Research** prioritizes official publisher and store sources, distinguishes minimum from recommended requirements, and asks the assistant not to invent hardware specifications or FPS estimates.
- **Device Shortlist** turns sourced requirements into cautious search criteria and asks the assistant to verify the exact product configuration before comparing it.

These are workflow instructions, not a guarantee that every AI host will follow them perfectly. The MCP tools themselves make no compatibility verdict. Any final assessment should link its technical claims to the source pages that support them.

The project also keeps its limitations visible:

- It does not scrape search or marketplace pages.
- It does not use a private Trendyol API or bypass access controls.
- It does not retrieve inventory, live prices, or product specifications.
- It does not guarantee app compatibility, performance, resolution, or FPS.
- Search results and product listings can be incomplete or out of date.

## For MCP users and builders

The server is written in Python and can run locally over **stdio** with an MCP client that supports local servers. It also supports **Streamable HTTP** for MCP clients that connect to a remote endpoint. A remote deployment needs to be hosted and exposed securely over HTTPS; a local `localhost` address is not reachable by an internet-hosted assistant.

MCP transport support and web browsing are separate capabilities. Connecting an assistant to the remote MCP endpoint gives it access to these tools, but the assistant also needs its own browsing/search capability to open the generated links. Support and setup vary between AI products.

The implementation was validated with local MCP protocol sessions over both stdio and Streamable HTTP, along with Python syntax and lint checks. That validates the server interaction; it does not claim that a third-party GPT product has been connected or that live search results have been verified.

The repository is public and MIT-licensed. Developers can inspect the Python server and Markdown skill files, adapt the query strategy, or use the workflow as a starting point for their own MCP projects.

## What comes next

The current version focuses on a deliberately small, understandable workflow: requirement discovery links, marketplace discovery links, and guidance for source-aware reporting. Future improvements should preserve that clarity—for example, better structured platform-specific query presets or optional, clearly disclosed search-provider integrations.

Any richer search integration should make its data source, API requirements, rate limits, and verification behavior explicit. The central goal remains the same: help an assistant move from “what does this app require?” to “which device listings should I inspect?” without presenting an unverified guess as a fact.

## Get involved

Explore the source, read the setup guide, and try the tools with an MCP client that supports them:

**Repository:** [github.com/EthYusuf/app-level](https://github.com/EthYusuf/app-level)

**License:** MIT

**Core tools:** `research_app_requirements` · `search_trendyol_devices`

Feedback, issue reports, and practical examples from different MCP clients can help make the setup and research workflow more useful to the community.

---

## Ready-to-publish LinkedIn post

I’m sharing **app-level**, a small open-source MCP project for researching app requirements and finding device listings to review.

The workflow is simple:

1. Generate focused search links for an app’s official system requirements and low-settings guidance.
2. Verify those sources with an MCP-connected assistant that has web access.
3. Use the confirmed requirements to create a Trendyol device search and compare the exact product listings.

There’s **no Brave Search API key or paid search service** to configure. The MCP server creates Google, Bing, and Trendyol links; it does not fetch pages, scrape listings, or claim that a device is compatible. Live research depends on the browsing capabilities of the MCP host, and prices and specifications should always be confirmed on the product page.

The repository includes two MCP tools, reusable research skills, local stdio and Streamable HTTP transports, and an MIT license.

If you’re building with MCP or exploring practical AI research workflows, I’d love your feedback:

https://github.com/EthYusuf/app-level

#MCP #OpenSource #AI #Python #ModelContextProtocol
