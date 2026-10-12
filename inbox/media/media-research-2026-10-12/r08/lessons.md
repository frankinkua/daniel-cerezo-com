# Research Lessons

1.  **Extracting metadata from YouTube vs TED.com:** TED.com embeds make it difficult to programmatically extract standard duration and subtitle options using simple HTTP GET tools (often returning obfuscated or React-hydrated NEXT_DATA payload). Using `yt-dlp` to extract metadata from the canonical YouTube references provides a more reliable structure (`--dump-json`).
2.  **Identifying Syndication (Correction):** Matching video duration alone (e.g. 1083s) is insufficient to declare a talk as a syndicated copy of an original performance. It is merely a strong hypothesis. True verification requires matching transcript/footage or confirmation from the original event source.
3.  **Upload vs. Event Date:** YouTube upload dates should not be confused with or substituted for the actual date an event took place. If the event delivery date is unknown, it should remain `null` rather than using the upload timestamp.

**Improved Prompt Clause:** "When researching video talks across platforms, prioritize finding the canonical YouTube upload. Do not rely solely on duration matching to confirm syndication; label such findings as a hypothesis unless transcript/footage review confirms it. Never substitute a YouTube upload date for an unknown event delivery date."
