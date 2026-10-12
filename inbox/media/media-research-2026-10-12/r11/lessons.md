# Research Lessons (R11)

- General searches for the subject's name plus "music" often returned completely unrelated artists on iTunes and generic search due to the commonality of the name or simply lack of published musical tracks under his own name.
- Web scraping YouTube search results via standard `urllib.request` fails because YouTube requires JavaScript rendering or API access, returning unparsed polymer data. It is better to use APIs like iTunes Search for podcasts to find verified audio interviews.
- The iTunes Podcast API proved very effective for finding original audio interviews and event records where the subject discusses his work.

**Improved Prompt Clause:**
"When searching for audio or video records, prefer official podcast APIs or structured directories over raw web scraping of video platforms which often block automated tools, and verify the subject's identity in the interview context to avoid homonyms."
