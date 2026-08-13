# Field Provenance

| Output field | Preferred source | Fallback |
|---|---|---|
| title | JSON-LD `name` | Next.js episode `title` |
| published_at | JSON-LD `datePublished` | Next.js episode `pubDate` |
| duration_seconds | Next.js episode `duration` | JSON-LD `timeRequired` |
| description | JSON-LD `description` | Next.js episode `shownotes` text |
| audio_url | JSON-LD `associatedMedia.contentUrl` | Next.js `enclosure.url`, then `og:audio` |
| podcast | JSON-LD `partOfSeries.name` | Next.js podcast `title` |
| podcast_url | JSON-LD `partOfSeries.url` | Derived from Next.js podcast `pid` |
| author | Next.js podcast `author` | unavailable |
| cover_image | Next.js episode image | `og:image` |
| counts | Next.js public episode/podcast data | unavailable |

Do not treat the direct audio URL as permission to redistribute the media.
