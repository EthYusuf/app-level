---
name: device-shortlist
description: Turn verified app requirements into a cautious device shortlist using app-level Trendyol links and product-page evidence.
---

# Device Shortlist

Use this skill after app requirements have been verified, when someone wants candidate phones or laptops to run an app/game.

## Workflow

1. Establish the user's device category and budget. Ask when a missing choice would materially change the shortlist.
2. Use only requirements verified with `app-requirements-research` or supplied with a trustworthy source. Do not convert an unverified guess into a hard filter.
3. Call `search_trendyol_devices` with concise model/chipset terms and only the hardware constraints that are known. Do not assume desktop GPU names map directly to laptop GPU performance.
4. Open the returned Trendyol search link and candidate product pages using the host's browsing capability. If that is unavailable, provide the link and label candidates as unverified.
5. Check the exact model/SKU, CPU or chipset, GPU, RAM, storage, operating system, seller, price, and listing details on each product page. Distinguish advertised from upgradeable memory/storage.
6. Compare each candidate against every sourced minimum requirement. Mark missing or ambiguous specs as unknown rather than as a match.
7. Present a short table with product link, listed price (if currently visible), relevant specs, requirement match, and caveats. Cite product pages for listing facts and official app sources for requirements.
8. Tell the user to confirm price, stock, seller, configuration, and return terms before purchasing.

## Safety and honesty

- The MCP tool creates links only; it does not retrieve listings, prices, inventory, or product specifications.
- Search snippets are not proof that a listing meets a requirement.
- Never call a device “compatible” unless the sourced requirements and exact listed configuration support that conclusion. Prefer “appears to meet the listed minimums” and state remaining uncertainty.
- Do not imply endorsement by Trendyol, a seller, or the app publisher.

## MCP tool

`search_trendyol_devices(search_terms, device_type, minimum_ram_gb, minimum_storage_gb, budget_try)` returns a Trendyol search URL and Google/Bing links for Trendyol listings.
