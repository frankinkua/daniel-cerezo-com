# Research Lessons (R14)

## Anti-bot systems and API alternatives
Standard HTML scraping of search engines (like DuckDuckGo) for generic audio/podcast queries often hits anti-bot blocks quickly. Directly querying open platform APIs (like the iTunes/Apple Podcasts Search API `https://itunes.apple.com/search?term=Daniel+Cerezo&entity=podcastEpisode`) is a highly effective, reliable alternative that returns structured JSON.

## Homonym Disambiguation in Audio Metadata
When filtering podcast episodes, titles alone are insufficient. Examining the episode `description` text proved essential for correctly distinguishing Daniel Cerezo the social entrepreneur from "Javier Cerezo" (a Spanish legionnaire) and "P. Daniel Cerezo" (a comboniano missionary in China). Identifying anchors like "Creer Hacer", "música", or "villa" in descriptions allowed for confident verification.

## Improved Prompt Clause
"If standard web search tools return blocks or captchas when looking for audio or video, immediately pivot to querying structured platform APIs (e.g., Apple iTunes Search API). Always extract and analyze description/metadata fields to filter homonyms using known identity anchors."
