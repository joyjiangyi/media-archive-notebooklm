---
name: notebooklm-media
description: Import public video, podcast, audio, web, and text sources into Google NotebookLM and generate source-grounded structured notes. Use when a user asks to add media to NotebookLM, analyze a video or podcast with NotebookLM, turn a media link into notes, or recover from an unsupported media URL by using an extracted audio URL or text fallback.
---

# NotebookLM Media

Use the `notebooklm` CLI supplied by the open-source `notebooklm-py` project. This skill does not bundle, fork, or modify that project.

## Setup

```bash
python3 -m pip install "notebooklm-py[browser]"
notebooklm login
notebooklm auth check
notebooklm list --json
```

Treat authentication files as secrets. Never print or package them.

## Import Ladder

Use explicit notebook IDs in every automation command.

1. Choose an existing notebook only when its title clearly matches the topic. Otherwise create one:
   `notebooklm create "Media Archive — <topic>" --json`
2. Try the canonical public page:
   `notebooklm source add "<URL>" --notebook <NB_ID> --json`
3. For a rejected podcast page, try its public audio URL.
4. If both fail, write confirmed metadata and show notes to a temporary UTF-8 Markdown file, then add that file.
5. Record the resulting `source_id` and route used.
6. Poll with `notebooklm source list --notebook <NB_ID> --json` until the source is `ready`; use a bounded wait and report timeout.

## Analysis

Use the video's structure for a single episode unless the user requests another structure:

```text
核心主题
分章节概要（每章节时间段）
3-5 个关键观点
可行动建议
适合关联的知识库标签
要求：不要编造来源之外的事实、数据或引语。
```

Only add chapter time ranges when the imported source contains verifiable timestamps. Use:

```bash
notebooklm ask "<GROUNDED_PROMPT>" --notebook <NB_ID> -s <SOURCE_ID> --json
```

Require the answer to separate direct source content from inference and to state whether it relied on a transcript, indexed page text, audio, or show notes.

If `ask` fails, inspect without deleting anything:

```bash
notebooklm source list --notebook <NB_ID> --json
notebooklm source fulltext <SOURCE_ID> --notebook <NB_ID> --json
```

## Autonomy

Run auth-check, list, create, source-add, source-list, fulltext, and ordinary ask commands without extra confirmation. Ask before login, generation commands that may take substantial time, downloads that write artifacts, or any delete command.

## Result

Return the notebook ID, source ID, import route, processing status, analysis, and limitations. Never report a source as ready or analyzed unless the command output confirms it.

See [references/troubleshooting.md](references/troubleshooting.md) for recovery steps.
