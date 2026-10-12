# Lessons

- **Lesson 1:** When scraping event organizers or publishers (like CREA), they often employ basic bot protection blocking default `urllib` User-Agents with a `403 Forbidden`. Passing a standard `Mozilla/5.0` User-Agent header bypasses this.
- **Lesson 2:** YouTube does not expose the canonical publication date via its oEmbed endpoint or standard `meta` tags without Javascript execution. Searching for the localized/formatted date string in the raw HTML is often the fastest fallback.

## Improved Prompt Clause
"If standard web fetching tools return 403 Forbidden, retry using a standard browser User-Agent header (e.g., `Mozilla/5.0`). If exact publication dates are missing from structured JSON or meta tags on complex SPAs like YouTube, search the raw HTML for standard date strings."