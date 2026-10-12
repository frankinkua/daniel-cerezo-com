# Research Packet R12: Speaking events and programmes

## Review Table

| Item ID | Type | Title | Publisher | Published At | Rights Status | Local Path |
|---|---|---|---|---|---|---|
| `tedx-eldorado-2015` | video | ¿Qué es la pobreza? El desafío de la vida en primera persona \| Daniel Cerezo \| TEDxEldorado | TEDx Talks | 2015-09-11 | reference_only | null |
| `crea-litoral-sur-2026` | article | El poder de la cultura organizacional en la empresa agropecuaria | Región CREA Litoral Sur | 2026-06-18 | reference_only | null |

## Useful Findings
- Identified a 2015 TEDx talk in Eldorado not previously cataloged.
- Identified a very recent 2026 conference given for CREA Litoral Sur on organizational culture.

## Proposed Website Uses
- Use `tedx-eldorado-2015` in the video timeline alongside his other TED talks.
- Use `crea-litoral-sur-2026` as a reference for his ongoing corporate/organizational culture consulting work.

## Limitations
- Neither source provides openly licensed media (like public domain photos or videos), thus both are strictly kept as `reference_only`.
- We could not definitively parse structured schema dates via standard BeautifulSoup; had to rely on raw HTML text search to verify publishing dates.

## Validation Commands
```bash
python3 -m json.tool inbox/media/media-research-2026-10-12/r12/findings.json
python3 -m json.tool inbox/media/media-research-2026-10-12/r12/search-log.json
```