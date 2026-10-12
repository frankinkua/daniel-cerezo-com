# Research Lessons

1.  **Extracting metadata from YouTube vs TED.com:** TED.com embeds make it difficult to programmatically extract standard duration and subtitle options using simple HTTP GET tools (often returning obfuscated or React-hydrated NEXT_DATA payload). Using `yt-dlp` to extract metadata from the canonical YouTube references provides a more reliable structure (`--dump-json`).
2.  **Identifying Syndication:** A talk with a different title ("¿Qué es la pobreza? El desafío de la vida en primera persona | Daniel Cerezo | TEDxEldorado") could be perceived as a new event, but by matching the duration exactly (1083s) with the `TEDxRiodelaPlata` talk, we can verify it's a reupload/syndication.

**Improved Prompt Clause:** "When researching video talks across platforms, prioritize finding the canonical YouTube upload and compare video durations to confidently deduplicate syndicated or re-branded uploads."
