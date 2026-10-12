# Lessons

- **Lesson 1:** When scraping event organizers or publishers (like CREA), they often employ basic bot protection blocking default `urllib` User-Agents with a `403 Forbidden`. Rather than aggressively bypassing this, we should respect the response, document the access limitation, and seek permitted alternative sources if necessary.
- **Lesson 2:** A video upload date does not establish an event-delivery date. Unless an organizer event programme is cited, the exact delivery date remains unknown.

## Improved Prompt Clause
"If standard web fetching tools return 403 Forbidden, document the access limitation and seek permitted alternative sources instead of aggressively bypassing it. Do not conflate video upload dates with event delivery dates."
