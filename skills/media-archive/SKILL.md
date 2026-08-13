---
name: media-archive
description: Archive public video and podcast URLs into grounded Markdown notes with optional NotebookLM analysis. Use when a user asks to save, archive, summarize, analyze, or make notes from YouTube, Bilibili, Xiaohongshu, Xiaoyuzhou, RSS podcast, or other public media links. Coordinate $xiaoyuzhou-media for Xiaoyuzhou extraction and $notebooklm-media for NotebookLM import and analysis when those skills are installed.
---

# Media Archive

Turn a public media URL into a portable, source-grounded Markdown archive. Keep the workflow storage-neutral: never assume a personal Obsidian vault, Notion database, folder, or notebook.

## Workflow

1. Classify the source as `video` or `podcast`.
2. Resolve short links and collect confirmed metadata.
3. For Xiaoyuzhou, invoke `$xiaoyuzhou-media` and preserve the canonical episode URL, audio URL, show notes, duration, and publication time.
4. Invoke `$notebooklm-media` when NotebookLM is installed and authenticated.
5. If the original URL is rejected by NotebookLM, try the extracted public audio URL. If that fails, add a UTF-8 text or Markdown file containing confirmed metadata and show notes.
6. Write the final note using [references/note-template.md](references/note-template.md).
7. Report degraded steps explicitly. Never invent a transcript, timestamp, quote, metric, or speaker.

## Source Priority

Prefer evidence in this order:

1. Transcript or captions supplied by the platform
2. NotebookLM indexed full text
3. Publisher show notes with real timestamps
4. Public page metadata

Label conclusions based only on show notes as `基于 Show Notes`.

## NotebookLM Analysis Prompt

Ask in Chinese unless the user requests another language:

```text
请根据已导入来源生成中文深度笔记。必须包含：
1. 一句话核心主题
2. 分章节概要；只有来源含真实时间戳时才使用时间戳
3. 3–5 个关键观点，每个观点注明依据
4. 可执行建议
5. 适合继续追问的 5 个问题
6. 来源局限

不得补写来源中没有的事实、数字、人物、引语或时间戳。只有 Show Notes 时，明确标注“基于 Show Notes”。
```

## Output Contract

Always provide:

- canonical source URL
- media type and platform
- confirmed metadata
- NotebookLM notebook and source IDs when available
- import route: `original_url`, `audio_url`, `text_fallback`, or `not_run`
- a Markdown note path or the complete Markdown note
- limitations and failed steps

## Safety

- Process only public sources or sources the user is authorized to use.
- Do not print cookies, browser profiles, auth JSON, session files, or tokens.
- Do not redistribute downloaded media unless the user has rights to do so.
- Do not imply that NotebookLM output is a verified transcript.
- Ask before deleting notebooks, sources, or local files.
