---
name: app-requirements-research
description: Research an app or game's minimum device requirements using the app-level MCP search links, verify primary sources, and report uncertainty with citations.
---

# App Requirements Research

Use this skill when someone asks whether a phone or computer can run an app/game, what its minimum requirements are, or what settings to expect on low-end hardware.

## Workflow

1. Ask for the exact app/game edition and target platform if either is unclear. Use `research_app_requirements` with the exact name and the closest platform (`mobile`, `computer`, or `auto`).
2. Treat the returned URLs as search links, not as evidence. Open them with the host's browsing/search capability. If browsing is unavailable, give the links to the user and say that live source verification was not performed.
3. Prefer sources in this order:
   - Official publisher/developer support page or official system-requirements page.
   - Official app-store listing for the exact platform and edition.
   - Reputable, attributable technical documentation when official details are incomplete.
4. Confirm the exact edition, operating system, and whether a listed requirement is minimum or recommended. Keep hardware specifications tied to their source URL.
5. Report CPU, GPU, memory, storage, OS, and any documented low-settings guidance only when the source states them. Distinguish minimum from recommended.
6. If sources disagree, show the disagreement and dates/versions when available. Do not silently choose one.
7. Explain that FPS, resolution, and playable settings depend on the exact device and are not guaranteed unless a source explicitly tests that configuration.
8. Link every factual requirement to its source. State clearly when no reliable source could be verified.

## Safety and honesty

- Never invent a requirement, compatibility verdict, benchmark, or FPS estimate.
- Search snippets and generated search URLs are discovery aids, not citations; cite the opened source page.
- Do not claim to have browsed when the host provided no browsing capability.
- Do not enter personal or sensitive information into search.

## MCP tool

`research_app_requirements(app_name, platform)` returns Google and Bing links for official requirements, low-settings information, and store listings. The MCP server itself does not fetch web pages.
