# Research Packet: TED and TEDx canonical evidence for Daniel Cerezo

This packet enriches the existing TED/TEDx references for Daniel Cerezo with verifiable metadata (timestamps, duration, subtitle availability) and includes newly discovered canonical appearances. Note that upload dates have been removed as they do not accurately reflect event-delivery dates.

## Review Table

| ID | Type | Title | Notes / Action |
|---|---|---|---|
| `tedx-poverty-2014-yt` | Video | ¿Qué es la pobreza? | **Baseline Enrichment.** Enriched metadata (duration: 1083s). EN/ES captions available. Duplicate/enrichment of `tedx-poverty-2014`. |
| `tedx-inclusion-2021-yt` | Video | La hipocresía de la inclusión social | **Baseline Enrichment.** Found canonical YouTube URL (VUI0K4rIZU0). Duplicate/enrichment of `tedx-inclusion-2021`. |
| `tedx-poverty-eldorado-2015` | Video | ¿Qué es la pobreza? (Eldorado) | **New Reference Hypothesis.** Hypothesized syndicated/re-uploaded version of the 2014 talk. Duration matches exactly (1083s), but confidence is medium as duration alone cannot prove identical performance without footage review. Duplicate of `tedx-poverty-2014` (unconfirmed). |
| `ted-ed-poverty-2016` | Video | Qué es la pobreza (TED-Ed) | **New Reference.** Animated video by TED-Ed based on his ideas. Duration 914s. EN/ES captions available. Not a direct recording of Daniel. |

## Proposed Website Uses

1.  **Reference Enrichment:** Update the main `catalog.json` with accurate YouTube video durations and subtitles availability to improve accessibility context on the website.
2.  **New Resource:** The TED-Ed video (`ted-ed-poverty-2016`) provides an alternative, animated format for his ideas which might be useful for a wider or younger demographic under the `creative-technology` or `social-impact` tags.

## Limitations and Notes

- **Rights Status:** All items are strictly `reference_only`. According to TED's usage policy, downloading and rehosting is not permitted without explicit licensing, so no local media has been downloaded.
- **YouTube Metadata limitations:** TED's official speaker pages lack raw duration metrics, which are easier to retrieve via YouTube canonical links. Upload dates from YouTube do not represent the event date, so they have been omitted.
- **Subtitle Availability:** Subtitles were checked dynamically and may change.

## Verification Commands

To validate the schemas:

```bash
node --test tests/*.test.cjs
python3 -c "import json; json.load(open('inbox/media/media-research-2026-10-12/r08/findings.json'))"
python3 -c "import json; json.load(open('inbox/media/media-research-2026-10-12/r08/search-log.json'))"
```
