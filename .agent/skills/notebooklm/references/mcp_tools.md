# NotebookLM MCP Tools Reference

This document outlines the native Model Context Protocol (MCP) tools provided by the `notebooklm-mcp` server. 
These tools should be used directly when interacting with Google NotebookLM instead of standalone scripts.

## Automatic Token & Session Management
You do NOT need to extract session IDs or CSRF tokens manually. The server automatically:
1. Reloads cookies from disk (`nlm login`)
2. Extracts session tokens when needed
3. Refreshes tokens on expiration
If a tool fails with `401 Unauthorized` or auth errors, prompt the user to run `nlm login` in their terminal.

## Available MCP Tools

### Notebook Management
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `notebook_list` | List all available notebooks | `max_results` (optional) |
| `notebook_create` | Create a new notebook | `title` (optional) |
| `notebook_get` | Get details and sources for a notebook | `notebook_id` (required) |
| `notebook_describe` | Get an AI-generated summary of the notebook | `notebook_id` (required) |
| `notebook_rename` | Change the title of a notebook | `notebook_id`, `new_title` |
| `notebook_delete` | Permanently delete a notebook | `notebook_id`, `confirm=True` |

### Query & Chat
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `notebook_query` | Ask the AI questions grounded in notebook sources | `notebook_id`, `query`, `source_ids`, `conversation_id` |
| `chat_configure` | Configure how the AI responds (e.g. style/length) | `notebook_id`, `goal`, `response_length`, `custom_prompt` |

### Source Management
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `source_add` | Add a web URL, text, GDrive doc, or file to a notebook | `notebook_id`, `source_type` (url/text/drive/file), `url`/`text`/`file_path`/`document_id` |
| `source_describe` | Get AI summary and keywords for a single source | `source_id` |
| `source_get_content` | Retrieve raw text from a source (no AI) | `source_id` |
| `source_list_drive` | Check freshness of Google Drive sources | `notebook_id` |
| `source_sync_drive` | Sync outdated Google Drive sources | `source_ids`, `confirm=True` |
| `source_delete` | Remove a source from the notebook | `source_id`, `confirm=True` |

### Research & Discovery
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `research_start` | Discover web/Drive sources | `query`, `source` (web/drive), `mode` (fast/deep) |
| `research_status` | Poll the progress of a research task | `notebook_id`, `task_id` |
| `research_import` | Import the discovered sources into the notebook | `notebook_id`, `task_id` |

### Studio Content Generation (Artifacts)
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `studio_create` | Start generation of audio, video, slides, reports, etc. | `notebook_id`, `artifact_type`, *type_specific_options*, `confirm=True` |
| `studio_status` | Check generation status and get download URLs | `notebook_id` |
| `studio_delete` | Remove generated artifacts from the studio | `notebook_id`, `artifact_id`, `confirm=True` |
| `download_artifact` | Download completed artifacts (JSON/MP4/MP3/Markdown/etc) | `notebook_id`, `artifact_type`, `output_path` |
| `export_artifact` | Export tabular data to Google Sheets & reports to Docs | `notebook_id`, `artifact_id`, `export_type` (docs/sheets) |

### Notes
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `note_create` | Create a new note | `notebook_id`, `content`, `title` (opt) |
| `note_list` | List notes | `notebook_id` |
| `note_update` | Modify a note | `notebook_id`, `note_id`, `content`/`title` |
| `note_delete` | Delete a note | `notebook_id`, `note_id`, `confirm=True` |

### Sharing & Collaboration
| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `notebook_share_status` | Get sharing status and list collaborators | `notebook_id` |
| `notebook_share_public` | Enable/disable public link access | `notebook_id`, `is_public` (bool) |
| `notebook_share_invite` | Invite a user via email as viewer/editor | `notebook_id`, `email`, `role` |

## Crucial Restrictions
- Tools marked with `confirm=True` perform **irreversible operations** (Deletions, Overwrites). Always ensure the user intends for this to happen.
- Content generation (`studio_create`, `research_start`) is **asynchronous**. You must poll `studio_status` or `research_status` until it finishes before downloading or importing.
