---
name: media-archive
description: "Run JioJioJoy's Xiaoyuzhou-to-NotebookLM archive workflow: fetch the user's recent 30-day Xiaoyuzhou listening history through an installed xiaoyuzhou-history skill, ask the user which episodes to process, import the confirmed episode links into NotebookLM for grounded Chinese analysis, and compile Markdown notes for Obsidian. Use when the user says 清理小宇宙最近听过的播客, asks to process recent Xiaoyuzhou history, or asks to archive a public video or podcast link with NotebookLM."
---

# Media Archive

Use the workflow demonstrated in JioJioJoy's NotebookLM tutorial. The default Xiaoyuzhou-history route is:

```text
recent 30-day history -> user confirmation -> NotebookLM analysis -> Markdown -> Obsidian
```

Media Archive supports both video and podcast sources. The tutorial's recent-history route is the default batch podcast demonstration; the single-link route below remains the entry point for public videos and individual podcast episodes.

## Context and token advantage

For long videos and podcasts, do not paste a complete transcript into the current Agent conversation by default. Add the media to NotebookLM as an independent source, ask targeted questions against that source, and return only the analysis or excerpts needed for the task. This reduces long-text occupation of the active Agent context and leaves more of the available Token budget for analysis, judgment, and final output. Do not promise a fixed percentage of savings; the result depends on source length, query design, and the Agent environment.

Read [references/video-prompts.md](references/video-prompts.md) when the user wants the tutorial's original wording. Do not paraphrase a prompt labeled as video-original.

## Prerequisites

Before the first run, verify rather than assume:

1. A trusted `xiaoyuzhou-history` skill or equivalent history-fetching tool is installed.
2. The user has completed its phone/verification-code login flow.
3. `notebooklm` is installed and `notebooklm auth check` confirms valid authentication.
4. The target Obsidian vault or output folder is known and writable.

If a prerequisite is missing, stop at that step and guide the user. Never expose, echo, store, or commit a phone number, verification code, cookie, session file, browser profile, token, or NotebookLM auth file.

## Recent-history workflow

### 1. Fetch candidates

Invoke the installed `xiaoyuzhou-history` capability and request the user's listening records from the most recent 30 days. Prefer completed/listened episodes if the tool distinguishes states.

Normalize only confirmed fields:

- episode title
- podcast title
- listened or completed time
- canonical episode URL
- duration or progress when supplied by the tool

### 2. Mandatory confirmation gate

Present a numbered candidate list and ask which episodes to process. Accept numbers, titles, URLs, `all`, or an explicit exclusion list.

Do not import, analyze, download, or write notes for any episode until the user explicitly confirms the selection. Unselected episodes end at the list stage.

### 3. Import the confirmed episodes

For every confirmed episode, invoke `$notebooklm-media` with the canonical episode URL and the analysis structure from the video's single-episode prompt:

1. 核心主题
2. 分章节概要（仅当来源里有真实时间戳时写时间段）
3. 3–5 个关键观点
4. 可行动建议
5. 适合关联的知识库标签

Enforce the video's source constraint exactly: `不要编造来源之外的事实、数据或引语。`

Use bounded waits. Report processing failures per episode and continue with the other confirmed items unless the failure affects authentication or every item.

### 4. Compile Markdown

Create one index note plus one note per successfully analyzed episode using [references/note-template.md](references/note-template.md). The index must contain:

- run date and requested range
- confirmed episode count
- successful, failed, and skipped episodes
- links to each episode note
- a cross-episode synthesis only when supported by the analyses

### 5. Save to Obsidian

Write only to the user's confirmed vault/folder. If no destination is known, provide or save a portable Markdown bundle in a neutral output folder and ask where it should be placed. Never invent a personal vault path.

Report created paths and failed items. Ask before overwriting existing notes.

## Single-link workflow

When the user supplies one video or podcast URL instead of requesting recent history:

1. Classify it as `video` or `podcast`.
2. For a Xiaoyuzhou episode, optionally invoke `$xiaoyuzhou-media` for confirmed metadata and a compatibility fallback.
3. Invoke `$notebooklm-media` with the original URL first.
4. Write a source-grounded note using the same analysis framework and source constraint.
5. Report the actual import route and limitations.

## Optional NotebookLM artifacts

Generate an infographic, slides, or an Audio Overview only after the user asks. These tasks can take time and may create downloads, so confirm the destination before downloading an artifact.

## Output contract

Always return:

- requested date range and candidate count for history mode
- the user's confirmed selection
- canonical URLs and confirmed metadata
- NotebookLM notebook/source identifiers when available
- success, failure, and skipped status per episode
- Markdown/Obsidian output paths
- source limitations and any degraded steps

Never claim an episode was completed, imported, ready, analyzed, or written unless the corresponding tool output confirms it.
