# Daniel Cerezo — a shared human story

A Spanish-language static personal website with the user-selected sunglasses portrait, a four-chapter scroll story, Creer Hacer reference, canonical talk links and searchable media tags.

## Story and evidence

- Neighborhood → music → community → public voice. An original symbolic SVG scene changes with scroll; it is not documentary imagery.
- The first portrait is an exact crop approved by the user: the unrelated chat sidebar was removed, without AI retouching.
- `inbox/media/catalog.json` contains identity evidence, sources, dates, rights notes and image checksum.
- Earlier unsupported Villa 21-24, book and talk-title claims were removed. Conflicting neighborhood references are not converted into aliases.
- TED talks link to the original publications. No ripped footage, commercial reuse claims, autoplay or third-party tracking embeds.
- The contact action opens Daniel's public professional profile. There is no fake form submission.
- With reduced motion enabled, transitions are disabled and the illustrated story remains static; all text stays readable. No scroll hijacking.

## Local checks

```bash
node --test tests/*.test.cjs
python3 -m http.server 8080 --bind 127.0.0.1
```

Check desktop and mobile layout, all four scene states, menu keyboard behavior, accented search terms and empty results.

## Deployment and future media

The existing domain `daniel-cerezo.com` is preserved. GitHub Pages tests the site and runs `scripts/build.cjs` to publish an explicit allowlist to `_site/`. The builder refuses to overwrite an existing build.

Jules research under `inbox/media/jules-daniel/` must be reviewed before any item is promoted into the main catalogue. An official website is not evidence of photo reuse permission. Do not rehost unlicensed references.

Local fonts are DM Sans and Instrument Serif, with their SIL Open Font Licenses. User-supplied photography is not relicensed by the repository.

## Project discovery update

The media collection includes all six approved references, with TEDx, Creer Hacer and music shortcuts, shareable filters and source details. Four direct chapter controls and a scroll-animation pause button make the story user-controllable; reduced motion starts in manual mode. No new third-party media is rehosted.
