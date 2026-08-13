---
name: xiaoyuzhou-media
description: Extract public Xiaoyuzhou podcast episode metadata, show notes, statistics, and the direct public audio URL from xiaoyuzhoufm.com episode links. Use whenever a user provides a Xiaoyuzhou episode URL and asks to fetch the podcast link, audio link, metadata, archive it, add it to NotebookLM, or turn it into notes.
---

# Xiaoyuzhou Media

Extract public episode data without login by parsing the page's JSON-LD and Next.js data. Do not bypass paywalls, private episodes, access controls, or platform restrictions.

## Extract

Run:

```bash
python3 scripts/extract_xiaoyuzhou.py "https://www.xiaoyuzhoufm.com/episode/<ID>"
```

For a compact human-readable card:

```bash
python3 scripts/extract_xiaoyuzhou.py "<URL>" --format markdown
```

The script returns the canonical episode URL, title, podcast, author, publication time, duration, cover, show notes, public audio URL, and available public counts.

## Handoff

When `$notebooklm-media` is installed:

1. Try the canonical episode URL.
2. If NotebookLM rejects the page, add `audio_url`.
3. If the audio URL fails, save the extracted metadata and description as UTF-8 Markdown and add the file.
4. Preserve the original episode URL in the final note regardless of import route.

## Validation

- Accept only `xiaoyuzhoufm.com` and `www.xiaoyuzhoufm.com` URLs.
- Treat absent fields as unavailable; never infer metrics.
- Prefer JSON-LD for portable episode metadata and Next.js data for richer optional fields.
- If both payloads are absent, return an error explaining that the page structure may have changed.
- Never download the audio unless the user explicitly requests it and has the right to do so.

See [references/fields.md](references/fields.md) for field provenance.
