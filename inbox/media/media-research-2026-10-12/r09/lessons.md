# Research Lessons (Task R09)

## Observations
When searching for a common name combined with broad terms ("Daniel Cerezo" + "entrevista" + "comunidad"), standard web search engines (DuckDuckGo, Google) frequently fail or block automated retrieval, or return sparse results. Searching directly against the Apple Podcasts API provided structured, canonical data for long-form audio interviews.

Disambiguation was necessary. Another "Daniel Cerezo" is a missionary in China (featured on several podcasts). We resolved homonyms by matching descriptions against known biographical elements like "Creer Hacer", "música", "psicólogo social", and "pobreza".

## Improved Prompt Clause
"If standard web search fails to return long-form audio interviews, directly query podcast directories (e.g., Apple Podcasts API) and aggressively filter by known organizational affiliations (like Creer Hacer) or biographical milestones to discard homonyms."
