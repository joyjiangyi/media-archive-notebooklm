# Troubleshooting

| Symptom | Check | Recovery |
|---|---|---|
| Authentication error | `notebooklm auth check` | Run `notebooklm login` interactively. |
| No notebook context | Command omitted notebook ID | Add `--notebook <NB_ID>`; do not rely on shared context. |
| Source stays processing | `source list` status | Use a bounded wait, then report `pending`. |
| Page URL rejected | Source add error | Try an authorized public audio URL, then text fallback. |
| Ask returns weak detail | Inspect `source fulltext` | State the indexed-source limitation; do not invent detail. |
| Rate limit | CLI error text | Retry later once; preserve notebook and source IDs. |

The CLI uses unofficial Google NotebookLM endpoints and may break when Google changes them. Check the upstream project before changing local authentication files.
