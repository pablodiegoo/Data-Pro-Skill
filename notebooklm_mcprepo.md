# GEMINI.md

## Project Overview

**NotebookLM MCP Server & CLI**

This project implements a Model Context Protocol (MCP) server **and a full-featured Command Line Interface (CLI)** that provides programmatic access to [NotebookLM](https://notebooklm.google.com). It allows AI agents, developers, and power users to interact with NotebookLM notebooks, sources, query capabilities, and **download generated artifacts** (Audio, Video, PDF, etc.).

Tested with personal/free tier accounts. May work with Google Workspace accounts but has not been tested. This project relies on internal APIs (`batchexecute` RPCs).

## Environment & Setup

The project uses `uv` for dependency management and tool installation.

### Prerequisites
- Python 3.11+
- `uv` (Universal Python Package Manager)
- Google Chrome (for automated authentication)

### Installation

**From PyPI (Recommended):**
```bash
uv tool install notebooklm-mcp-cli
# or: pip install notebooklm-mcp-cli
```

**From Source (Development):**
```bash
git clone https://github.com/YOUR_USERNAME/notebooklm-mcp.git
cd notebooklm-mcp
uv tool install .
```

## Authentication

**Preferred: Run the automated authentication CLI:**
```bash
nlm login
```
This launches Chrome, you log in, and cookies are extracted automatically. Your login is saved to a Chrome profile for future use.

**Auto-refresh (v0.1.9+):**
The server now automatically handles token expiration:
1. Refreshes CSRF tokens on expiry (immediate)
2. Reloads cookies from disk if updated externally
3. Runs headless Chrome auth if profile has saved login

If headless auth fails (Google login fully expired), you'll see a message to run `nlm login` again.

**Explicit refresh (MCP tool):**
```
refresh_auth()  # Reload tokens from disk or run headless auth
```

**Fallback: Manual extraction (if CLI fails)**
If the automated tool doesn't work, extract cookies via Chrome DevTools:
1. Open Chrome DevTools on notebooklm.google.com
2. Go to Network tab, find a batchexecute request
3. Copy the Cookie header and call `save_auth_tokens(cookies=...)`

**Environment variable (advanced):**
```bash
export NOTEBOOKLM_COOKIES="SID=xxx; HSID=xxx; SSID=xxx; ..."
```

Cookies last for weeks. The server auto-refreshes as long as Chrome profile login is valid.

## Development Workflow

### Building and Running

**Reinstalling after changes:**
Because `uv tool install` installs into an isolated environment, you must reinstall to see changes during development.
```bash
uv cache clean
uv tool install --force .
```

**Running the Server:**
**Running the Server:**
```bash
# Standard mode (stdio)
notebooklm-mcp

# Debug mode (verbose logging)
notebooklm-mcp --debug

# HTTP Server mode
notebooklm-mcp --transport http --port 8000
```

### Testing

Run the test suite using `pytest` via `uv`:
```bash
# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_api_client.py
```

## Project Structure

- `src/notebooklm_tools/`
    - `services/`: **Shared service layer (v0.3.0+)** — Business logic, validation, error handling
        - `errors.py`: Custom error hierarchy (`ServiceError`, `ValidationError`, etc.)
        - `chat.py`, `downloads.py`, `exports.py`, `notebooks.py`, `notes.py`: Domain services
        - `research.py`, `sharing.py`, `sources.py`, `studio.py`: More domain services
    - `cli/`: CLI commands and formatting (thin wrapper delegating to `services/`)
    - `mcp/`: MCP Server implementation (thin wrapper delegating to `services/`)
        - `tools/`: Modular tool definitions (one file per domain)
        - `server.py`: Slim server facade (imports tools from modules)
    - `core/client.py`: Low-level internal API calls (no business logic).
    - `core/constants.py`: Single source of truth for all API code-name mappings.
    - `core/auth.py`: Handles token validation, storage, and loading.
    - `utils/cdp.py`: Chrome DevTools Protocol for cookie extraction and headless auth.
    - `utils/`: Configuration and browser utilities
- `tests/services/`: Unit tests for all service modules (372+ tests)
- `CLAUDE.md`: Contains detailed documentation on the internal RPC IDs and protocol specifics. **Refer to this file for API deep dives.**
- `pyproject.toml`: Project configuration and dependencies.

## Key Conventions

- **Internal APIs:** This project relies on undocumented APIs. Changes to Google's internal API will break functionality.
- **RPC Protocol:** The API uses Google's `batchexecute` protocol. Responses often contain "anti-XSSI" prefixes (`)]}'`) that must be stripped.
- **Layering (v0.3.0+):** `cli/` and `mcp/` must NOT import from `core/` — delegate to `services/` instead. Services return TypedDicts and raise `ServiceError`/`ValidationError`.
- **New features:** Add low-level API in `core/client.py` → business logic in `services/*.py` → thin wrappers in `mcp/tools/*.py` and `cli/commands/*.py` → tests in `tests/services/`.
- **Constants:** All code-name mappings should be defined in `constants.py` using the `CodeMapper` class.

## Recent Additions

- **v0.3.0 Service Layer Refactor**: Introduced shared `services/` layer with 10 domain modules, eliminating duplicated logic between CLI and MCP. 372+ unit tests.
- **Skill Commands**: `nlm skill install/uninstall/list/show` for AI assistant integration
- **Cursor Support**: Added Cursor AI editor to supported skill targets
- **Verb-First Commands**: Alternative command style (`nlm install skill`, `nlm list skills`)
- **Interactive Artifact Downloads**: `download_quiz` and `download_flashcards` with JSON/Markdown/HTML formats
- **Sharing API**: `notebook_share_status`, `notebook_share_public`, `notebook_share_invite` for collaboration


---- Claude.md

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**NotebookLM MCP Server & CLI** - Provides programmatic access to NotebookLM (notebooklm.google.com) via both a Model Context Protocol server and a comprehensive command-line interface.

Tested with personal/free tier accounts. May work with Google Workspace accounts but has not been tested.

## Development Commands

```bash
# Install dependencies
uv tool install .

# Reinstall after code changes (ALWAYS clean cache first)
uv cache clean && uv tool install --force .

# Run the MCP server (stdio)
notebooklm-mcp

# Run with Debug logging
notebooklm-mcp --debug

# Run as HTTP server
notebooklm-mcp --transport http --port 8000

# Run tests
uv run pytest

# Run a single test
uv run pytest tests/test_file.py::test_function -v
```

**Python requirement:** >=3.11

## Authentication (SIMPLIFIED!)

**You only need to provide COOKIES!** The CSRF token and session ID are now **automatically extracted** when needed.

### Method 1: Chrome DevTools MCP (Recommended)

**Option A - Fast (Recommended):**
Extract CSRF token and session ID directly from network request - **no page fetch needed!**

```python
# 1. Navigate to NotebookLM page
navigate_page(url="https://notebooklm.google.com/")

# 2. Get a batchexecute request (any NotebookLM API call)
get_network_request(reqid=<any_batchexecute_request>)

# 3. Save with all three fields from the network request:
save_auth_tokens(
    cookies=<cookie_header>,
    request_body=<request_body>,  # Contains CSRF token
    request_url=<request_url>      # Contains session ID
)
```

**Option B - Minimal (slower first call):**
Save only cookies, tokens extracted from page on first API call

```python
save_auth_tokens(cookies=<cookie_header>)
```

### Method 2: Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NOTEBOOKLM_COOKIES` | Yes | Full cookie header from Chrome DevTools |
| `NOTEBOOKLM_CSRF_TOKEN` | No | (DEPRECATED - auto-extracted) |
| `NOTEBOOKLM_SESSION_ID` | No | (DEPRECATED - auto-extracted) |

### Token Expiration

- **Cookies**: Stable for weeks, but some rotate on each request
- **CSRF token**: Auto-refreshed on each client initialization
- **Session ID**: Auto-refreshed on each client initialization

When API calls fail with auth errors, re-extract fresh cookies from Chrome DevTools.

## Architecture

```
src/notebooklm_tools/
├── __init__.py          # Package version
├── services/            # Shared service layer (v0.3.0+)
│   ├── errors.py        # ServiceError, ValidationError, NotFoundError, etc.
│   ├── chat.py          # Chat/query logic
│   ├── downloads.py     # Artifact downloading
│   ├── exports.py       # Google Docs/Sheets export
│   ├── notebooks.py     # Notebook CRUD + describe
│   ├── notes.py         # Note CRUD
│   ├── research.py      # Research start/poll/import
│   ├── sharing.py       # Public link, invite, status
│   ├── sources.py       # Source add/list/sync/delete
│   └── studio.py        # Artifact creation, status, rename, delete
├── cli/                 # CLI commands and formatting (thin wrapper)
├── mcp/                 # MCP server + tools (thin wrapper)
│   ├── server.py        # FastMCP server facade
│   └── tools/           # Modular tool definitions per domain
├── core/                # Low-level API client (no business logic)
│   ├── client.py        # Internal batchexecute API calls
│   ├── constants.py     # Code-name mappings (CodeMapper class)
│   └── auth.py          # AuthManager for profile-based token caching
└── utils/
    ├── config.py        # Configuration and storage paths
    └── cdp.py           # Chrome DevTools Protocol for cookie extraction
```

**Layering Rules (v0.3.0+):**
- `cli/` and `mcp/` are thin wrappers: they handle UX concerns (prompts, spinners, JSON responses) and delegate to `services/`
- `services/` contains all business logic, validation, and error handling. Returns typed dicts.
- `cli/` and `mcp/` must NOT import from `core/` directly — always go through `services/`
- `services/` raises `ServiceError`/`ValidationError` — never raw exceptions

**Storage Structure (`~/.notebooklm-mcp-cli/`):**
```
├── config.toml                    # CLI settings (default_profile, output format)
├── aliases.json                   # Notebook aliases
├── profiles/<name>/auth.json      # Per-profile credentials and email
├── chrome-profile/                # Chrome session (single-profile/legacy)
└── chrome-profiles/<name>/        # Chrome sessions (multi-profile)
```

**Executables:**
- `nlm` - Command-line interface
- `notebooklm-mcp` - The MCP server

## MCP Tools Provided

| Tool | Purpose |
|------|---------|
| `notebook_list` | List all notebooks |
| `notebook_create` | Create new notebook |
| `notebook_get` | Get notebook details |
| `notebook_describe` | Get AI-generated summary of notebook content with keywords |
| `source_describe` | Get AI-generated summary and keyword chips for a source |
| `source_get_content` | Get raw text content from a source (no AI processing) |
| `notebook_rename` | Rename a notebook |
| `chat_configure` | Configure chat goal/style and response length |
| `notebook_delete` | Delete a notebook (REQUIRES confirmation) |
| `source_add` | Add source (url, text, drive, file) |
| `notebook_query` | Ask questions (AI answers!) |
| `source_list_drive` | List sources with types, check Drive freshness |
| `source_sync_drive` | Sync stale Drive sources (REQUIRES confirmation) |
| `source_delete` | Delete a source from notebook (REQUIRES confirmation) |
| `research_start` | Start Web or Drive research to discover sources |
| `research_status` | Check research progress and get results |
| `research_import` | Import discovered sources into notebook |
| `studio_create` | Generate unified content (audio, video, infographic, slides, etc.) |
| `download_artifact` | Download any artifact (audio, video, pdf, markdown, json) |
| `export_artifact` | Export Data Tables to Google Sheets or Reports to Google Docs |
| `studio_status` | Check studio artifact generation status |
| `studio_delete` | Delete studio artifacts (REQUIRES confirmation) |
| `notebook_share_status` | Get sharing settings and collaborators |
| `notebook_share_public` | Enable/disable public link access |
| `notebook_share_invite` | Invite collaborator by email |
| `save_auth_tokens` | Save tokens extracted via Chrome DevTools MCP |
| `refresh_auth` | Reload auth tokens or run headless auth |
| `note_create` | Create a note in a notebook |
| `note_list` | List all notes in a notebook |
| `note_update` | Update a note's content or title |
| `note_delete` | Delete a note (REQUIRES confirmation) |

**IMPORTANT - Operations Requiring Confirmation:**
- `notebook_delete` requires `confirm=True` - deletion is IRREVERSIBLE
- `source_delete` requires `confirm=True` - deletion is IRREVERSIBLE
- `source_sync_drive` requires `confirm=True` - always show stale sources first via `source_list_drive`
- All studio creation tools require `confirm=True` - show settings and get user approval first
- `studio_delete` requires `confirm=True` - list artifacts first via `studio_status`, deletion is IRREVERSIBLE
- `note_delete` requires `confirm=True` - deletion is IRREVERSIBLE

## Features NOT Yet Implemented

None - all NotebookLM features that can be accessed programmatically are implemented.

## Troubleshooting

### "401 Unauthorized" or "403 Forbidden"
- Cookies or CSRF token expired
- Re-extract from Chrome DevTools

### "Invalid CSRF token"
- The `at=` value expired
- Must match the current session

### Empty notebook list
- Session might be for a different Google account
- Verify you're logged into the correct account

### Rate limit errors
- Free tier: ~50 queries/day
- Wait until the next day or upgrade to Plus

## Documentation

### API Reference

**For detailed API documentation** (RPC IDs, parameter structures, response formats), see:

**[docs/API_REFERENCE.md](./docs/API_REFERENCE.md)**

This includes:
- All discovered RPC endpoints and their parameters
- Source type structures (URL, text, Drive)
- Studio content creation (audio, video, reports, etc.)
- Research workflow details
- Mind map generation process
- Source metadata structures

Only read API_REFERENCE.md when:
- Debugging API issues
- Adding new features
- Understanding internal API behavior

### MCP Test Plan

**For comprehensive MCP tool testing**, see:

**[docs/MCP_CLI_TEST_PLAN.md](./docs/MCP_CLI_TEST_PLAN.md)**

This includes:
- Step-by-step test cases for all 29 MCP tools and CLI commands
- Authentication and basic operations tests
- Source management and Drive sync tests
- Studio content generation tests (audio, video, infographics, etc.)
- Quick copy-paste test prompts for validation

Use this test plan when:
- Validating MCP server functionality after code changes
- Testing new tool implementations
- Debugging MCP tool issues

## Contributing

When adding new features:

1. Use Chrome DevTools MCP to capture the network request
2. Document the RPC ID in docs/API_REFERENCE.md
3. Add the param structure with comments
4. Add the low-level API method in `core/client.py`
5. Add business logic in the appropriate `services/*.py` module
6. Add a thin wrapper in `mcp/tools/*.py` (for MCP) and `cli/commands/*.py` (for CLI)
7. Write unit tests for the service function in `tests/services/`
8. Update the "Features NOT Yet Implemented" checklist
9. Add test case to docs/MCP_TEST_PLAN.md

## License

MIT License


--- Readme.md

# NotebookLM CLI & MCP Server

![NotebookLM MCP Header](docs/media/header.jpg)

[![PyPI version](https://img.shields.io/pypi/v/notebooklm-mcp-cli)](https://pypi.org/project/notebooklm-mcp-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/notebooklm-mcp-cli)](https://pypistats.org/packages/notebooklm-mcp-cli)
[![Total downloads](https://static.pepy.tech/badge/notebooklm-mcp-cli)](https://pepy.tech/projects/notebooklm-mcp-cli)
[![Python](https://img.shields.io/pypi/pyversions/notebooklm-mcp-cli)](https://pypi.org/project/notebooklm-mcp-cli/)
[![License](https://img.shields.io/pypi/l/notebooklm-mcp-cli)](https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/LICENSE)

> 🎉 **January 2026 — Major Update!** This project has been completely refactored to unify **NotebookLM-MCP** and **NotebookLM-CLI** into a single, powerful package. One install gives you both the CLI (`nlm`) and MCP server (`notebooklm-mcp`). See the [CLI Guide](docs/CLI_GUIDE.md) and [MCP Guide](docs/MCP_GUIDE.md) for full documentation.

**Programmatic access to Google NotebookLM** — via command-line interface (CLI) or Model Context Protocol (MCP) server.

> **Note:** Tested with Pro/free tier accounts. May work with NotebookLM Enterprise accounts but has not been tested.

📺 **Watch the Demos**

### MCP Demos

| **General Overview** | **Claude Desktop** | **Perplexity Desktop** | **MCP Super Assistant** |
|:---:|:---:|:---:|:---:|
| [![General](https://img.youtube.com/vi/d-PZDQlO4m4/mqdefault.jpg)](https://www.youtube.com/watch?v=d-PZDQlO4m4) | [![Claude](https://img.youtube.com/vi/PU8JhgLPxes/mqdefault.jpg)](https://www.youtube.com/watch?v=PU8JhgLPxes) | [![Perplexity](https://img.youtube.com/vi/BCKlDNg-qxs/mqdefault.jpg)](https://www.youtube.com/watch?v=BCKlDNg-qxs) | [![MCP SuperAssistant](https://img.youtube.com/vi/7aHDbkr-l_E/mqdefault.jpg)](https://www.youtube.com/watch?v=7aHDbkr-l_E) |

### CLI Demos

| **CLI Overview** | **CLI, MCP & Skills Deep Dive** | **Latest: Setup, Doctor & One-Click Install** |
|:---:|:---:|:---:|
| [![CLI Overview](https://img.youtube.com/vi/XyXVuALWZkE/mqdefault.jpg)](https://www.youtube.com/watch?v=XyXVuALWZkE) | [![CLI, MCP & Skills](https://img.youtube.com/vi/ZQBQigFK-E8/mqdefault.jpg)](https://www.youtube.com/watch?v=ZQBQigFK-E8) | [![Latest: Setup, Doctor & mcpb](https://img.youtube.com/vi/5tOUilBTJ3Q/mqdefault.jpg)](https://www.youtube.com/watch?v=5tOUilBTJ3Q) |


## Two Ways to Use

### 🖥️ Command-Line Interface (CLI)

Use `nlm` directly in your terminal for scripting, automation, or interactive use:

```bash
nlm notebook list                              # List all notebooks
nlm notebook create "Research Project"         # Create a notebook
nlm source add <notebook> --url "https://..."  # Add sources
nlm audio create <notebook> --confirm          # Generate podcast
nlm download audio <notebook> <artifact-id>    # Download audio file
nlm share public <notebook>                    # Enable public link
```

Run `nlm --ai` for comprehensive AI-assistant documentation.

### 🤖 MCP Server (for AI Agents)

Connect AI assistants (Claude, Gemini, Cursor, etc.) to NotebookLM:

```bash
# Automatic setup — picks the right config for each tool
nlm setup add claude-code
nlm setup add gemini
nlm setup add cursor
nlm setup add cline
nlm setup add antigravity
```
```

Then use natural language: *"Create a notebook about quantum computing and generate a podcast"*

## Features

| Capability | CLI Command | MCP Tool |
|------------|-------------|----------|
| List notebooks | `nlm notebook list` | `notebook_list` |
| Create notebook | `nlm notebook create` | `notebook_create` |
| Add Sources (URL, Text, Drive, File) | `nlm source add` | `source_add` |
| Query notebook (AI chat) | `nlm notebook query` | `notebook_query` |
| Create Studio Content (Audio, Video, etc.) | `nlm studio create` | `studio_create` |
| Download artifacts | `nlm download <type>` | `download_artifact` |
| Web/Drive research | `nlm research start` | `research_start` |
| Share notebook | `nlm share public/invite` | `notebook_share_*` |
| Sync Drive sources | `nlm source sync` | `source_sync_drive` |
| Configure AI tools | `nlm setup add/remove/list` | — |
| Install AI Skills | `nlm skill install/update` | — |
| Diagnose issues | `nlm doctor` | — |

📚 **More Documentation:**
- **[CLI Guide](docs/CLI_GUIDE.md)** — Complete command reference
- **[MCP Guide](docs/MCP_GUIDE.md)** — All 29 MCP tools with examples
- **[Authentication](docs/AUTHENTICATION.md)** — Setup and troubleshooting
- **[API Reference](docs/API_REFERENCE.md)** — Internal API docs for contributors

## Important Disclaimer

This MCP and CLI use **internal APIs** that:
- Are undocumented and may change without notice
- Require cookie extraction from your browser (I have a tool for that!)

Use at your own risk for personal/experimental purposes.

## Installation

> 🆕 **Claude Desktop users:** [Download the extension](https://github.com/jacob-bd/notebooklm-mcp-cli/releases/latest) (`.mcpb` file) → double-click → done! One-click install, no config needed.

Install from PyPI. This single package includes **both the CLI and MCP server**:

### Using uv (Recommended)
```bash
uv tool install notebooklm-mcp-cli
```

### Using uvx (Run Without Install)
```bash
uvx --from notebooklm-mcp-cli nlm --help
uvx --from notebooklm-mcp-cli notebooklm-mcp
```

### Using pip
```bash
pip install notebooklm-mcp-cli
```

### Using pipx
```bash
pipx install notebooklm-mcp-cli
```

**After installation, you get:**
- `nlm` — Command-line interface
- `notebooklm-mcp` — MCP server for AI assistants

<details>
<summary>Alternative: Install from Source</summary>

```bash
# Clone the repository
git clone https://github.com/jacob-bd/notebooklm-mcp-cli.git
cd notebooklm-mcp

# Install with uv
uv tool install .
```
</details>

## Upgrading

```bash
# Using uv
uv tool upgrade notebooklm-mcp-cli

# Using pip
pip install --upgrade notebooklm-mcp-cli

# Using pipx
pipx upgrade notebooklm-mcp-cli
```

After upgrading, restart your AI tool to reconnect to the updated MCP server:

- **Claude Code:** Restart the application, or use `/mcp` to reconnect
- **Cursor:** Restart the application
- **Gemini CLI:** Restart the CLI session

## Upgrading from Legacy Versions

If you previously installed the **separate** CLI and MCP packages, you need to migrate to the unified package.

### Step 1: Check What You Have Installed

```bash
uv tool list | grep notebooklm
```

**Legacy packages to remove:**
| Package | What it was |
|---------|-------------|
| `notebooklm-cli` | Old CLI-only package |
| `notebooklm-mcp-server` | Old MCP-only package |

### Step 2: Uninstall Legacy Packages

```bash
# Remove old CLI package (if installed)
uv tool uninstall notebooklm-cli

# Remove old MCP package (if installed)
uv tool uninstall notebooklm-mcp-server
```

### Step 3: Reinstall the Unified Package

After removing legacy packages, reinstall to fix symlinks:

```bash
uv tool install --force notebooklm-mcp-cli
```

> **Why `--force`?** When multiple packages provide the same executable, `uv` can leave broken symlinks after uninstalling. The `--force` flag ensures clean symlinks.

### Step 4: Verify Installation

```bash
uv tool list | grep notebooklm
```

You should see only:
```
notebooklm-mcp-cli v0.2.0
- nlm
- notebooklm-mcp
```

### Step 5: Re-authenticate

Your existing cookies should still work, but if you encounter auth issues:

```bash
nlm login
```

> **Note:** MCP server configuration (in Claude Code, Cursor, etc.) does not need to change — the executable name `notebooklm-mcp` is the same.

## Uninstalling

To completely remove the MCP:

```bash
# Using uv
uv tool uninstall notebooklm-mcp-cli

# Using pip
pip uninstall notebooklm-mcp-cli

# Using pipx
pipx uninstall notebooklm-mcp-cli

# Remove cached auth tokens and data (optional)
rm -rf ~/.notebooklm-mcp-cli
```

Also remove from your AI tools:

```bash
nlm setup remove claude-code
nlm setup remove cursor
# ... or any configured tool
```

## Authentication

Before using the CLI or MCP, you need to authenticate with NotebookLM:

### CLI Authentication (Recommended)

```bash
# Auto mode: launches Chrome, you log in, cookies extracted automatically
nlm login

# Check if already authenticated
nlm login --check

# Use a named profile (for multiple Google accounts)
nlm login --profile work
nlm login --profile personal

# Manual mode: import cookies from a file
nlm login --manual --file cookies.txt

# External CDP provider (e.g., OpenClaw-managed browser)
nlm login --provider openclaw --cdp-url http://127.0.0.1:18800
```

**Profile management:**
```bash
nlm login --check                    # Show current auth status
nlm login switch <profile>           # Switch the default profile
nlm login profile list               # List all profiles with email addresses
nlm login profile delete <profile>   # Delete a profile
nlm login profile rename <old> <new> # Rename a profile
```

Each profile gets its own isolated Chrome session, so you can be logged into multiple Google accounts simultaneously.

### Standalone Auth Tool

If you only need the MCP server (not the CLI):

```bash
nlm login              # Auto mode (launches Chrome)
nlm login --manual     # Manual file mode
```

**How it works:** Auto mode launches a dedicated Chrome profile, you log in to Google, and cookies are extracted automatically. Your login persists for future auth refreshes.

For detailed instructions and troubleshooting, see **[docs/AUTHENTICATION.md](docs/AUTHENTICATION.md)**.

## MCP Configuration

> **⚠️ Context Window Warning:** This MCP provides **29 tools**. Disable it when not using NotebookLM to preserve context. In Claude Code: `@notebooklm-mcp` to toggle.

### Automatic Setup (Recommended)

Use `nlm setup` to automatically configure the MCP server for your AI tools — no manual JSON editing required:

```bash
# Add to any supported tool
nlm setup add claude-code
nlm setup add claude-desktop
nlm setup add gemini
nlm setup add cursor
nlm setup add windsurf

# Check which tools are configured
nlm setup list

# Diagnose installation & auth issues
nlm doctor
```

### Install AI Skills (Optional)

Install the NotebookLM expert guide for your AI assistant to help it use the tools effectively. Supported for **Cline**, **Antigravity**, **OpenClaw**, **Codex**, **OpenCode**, **Claude Code**, and **Gemini CLI**.

```bash
# Install skill files
nlm skill install cline
nlm skill install openclaw
nlm skill install codex
nlm skill install antigravity

# Update skills
nlm skill update
```

### Remove from a tool

```bash
nlm setup remove claude-code
```

### Using uvx (No Install Required)

If you don't want to install the package, you can use `uvx` to run on-the-fly:

```bash
# Run CLI commands directly
uvx --from notebooklm-mcp-cli nlm setup add cursor
uvx --from notebooklm-mcp-cli nlm login
```

For tools that use JSON config, point them to uvx:
```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "uvx",
      "args": ["--from", "notebooklm-mcp-cli", "notebooklm-mcp"]
    }
  }
}
```

<details>
<summary>Manual Setup (if you prefer)</summary>

**Claude Code / Gemini CLI** support adding MCP servers via their own CLI:
```bash
claude mcp add --scope user notebooklm-mcp notebooklm-mcp
gemini mcp add --scope user notebooklm-mcp notebooklm-mcp
```

**Cursor / Windsurf** resolve commands from your `PATH`, so the command name is enough:
```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "notebooklm-mcp"
    }
  }
}
```

| Tool | Config Location |
|------|-----------------|
| Cursor | `~/.cursor/mcp.json` |
| Windsurf | `~/.codeium/windsurf/mcp_config.json` |

**Claude Desktop / VS Code** may not resolve `PATH` — use the full path to the binary:
```json
{
  "mcpServers": {
    "notebooklm-mcp": {
      "command": "/full/path/to/notebooklm-mcp"
    }
  }
}
```

Find your path with: `which notebooklm-mcp`

| Tool | Config Location |
|------|-----------------|
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| VS Code | `~/.vscode/mcp.json` |

</details>

📚 **Full configuration details:** [MCP Guide](docs/MCP_GUIDE.md) — Server options, environment variables, HTTP transport, multi-user setup, and context window management.

## What You Can Do

Simply chat with your AI tool (Claude Code, Cursor, Gemini CLI) using natural language. Here are some examples:

### Research & Discovery

- "List all my NotebookLM notebooks"
- "Create a new notebook called 'AI Strategy Research'"
- "Start web research on 'enterprise AI ROI metrics' and show me what sources it finds"
- "Do a deep research on 'cloud marketplace trends' and import the top 10 sources"
- "Search my Google Drive for documents about 'product roadmap' and create a notebook"

### Adding Content

- "Add this URL to my notebook: https://example.com/article"
- "Add this YouTube video about Kubernetes to the notebook"
- "Add my meeting notes as a text source to this notebook"
- "Import this Google Doc into my research notebook"

### AI-Powered Analysis

- "What are the key findings in this notebook?"
- "Summarize the main arguments across all these sources"
- "What does this source say about security best practices?"
- "Get an AI summary of what this notebook is about"
- "Configure the chat to use a learning guide style with longer responses"

### Content Generation

- "Create an audio podcast overview of this notebook in deep dive format"
- "Generate a video explainer with classic visual style"
- "Make a briefing doc from these sources"
- "Create flashcards for studying, medium difficulty"
- "Generate an infographic in landscape orientation"
- "Build a mind map from my research sources"
- "Create a slide deck presentation from this notebook"

### Smart Management

- "Check which Google Drive sources are out of date and sync them"
- "Show me all the sources in this notebook with their freshness status"
- "Delete this source from the notebook"
- "Check the status of my audio overview generation"

### Sharing & Collaboration

- "Show me the sharing settings for this notebook"
- "Make this notebook public so anyone with the link can view it"
- "Disable public access to this notebook"
- "Invite user@example.com as an editor to this notebook"
- "Add a viewer to my research notebook"

**Pro tip:** After creating studio content (audio, video, reports, etc.), poll the status to get download URLs when generation completes.

## Authentication Lifecycle

| Component | Duration | Refresh |
|-----------|----------|---------|
| Cookies | ~2-4 weeks | Auto-refresh via headless Chrome (if profile saved) |
| CSRF Token | ~minutes | Auto-refreshed on every request failure |
| Session ID | Per MCP session | Auto-extracted on MCP start |

**v0.1.9+**: The server now automatically handles token expiration:
1. Refreshes CSRF tokens immediately when expired
2. Reloads cookies from disk if updated externally
3. Runs headless Chrome auth if profile has saved login

You can also call `refresh_auth()` to explicitly reload tokens.

If automatic refresh fails (Google login fully expired), run `nlm login` again.

## Troubleshooting

### `uv tool upgrade` Not Installing Latest Version

**Symptoms:**
- Running `uv tool upgrade notebooklm-mcp-cli` installs an older version (e.g., 0.1.5 instead of 0.1.9)
- `uv cache clean` doesn't fix the issue

**Why this happens:** `uv tool upgrade` respects version constraints from your original installation. If you initially installed an older version or with a constraint, `upgrade` stays within those bounds by design.

**Fix — Force reinstall:**
```bash
uv tool install --force notebooklm-mcp-cli
```

This bypasses any cached constraints and installs the absolute latest version from PyPI.

**Verify:**
```bash
uv tool list | grep notebooklm
# Should show: notebooklm-mcp-cli v0.1.9 (or latest)
```


## Limitations

- **Rate limits**: Free tier has ~50 queries/day
- **No official support**: API may change without notice
- **Cookie expiration**: Need to re-extract cookies every few weeks

## Contributing

See [CLAUDE.md](CLAUDE.md) for detailed API documentation and how to add new features.

## Vibe Coding Alert

Full transparency: this project was built by a non-developer using AI coding assistants. If you're an experienced Python developer, you might look at this codebase and wince. That's okay.

The goal here was to scratch an itch - programmatic access to NotebookLM - and learn along the way. The code works, but it's likely missing patterns, optimizations, or elegance that only years of experience can provide.

**This is where you come in.** If you see something that makes you cringe, please consider contributing rather than just closing the tab. This is open source specifically because human expertise is irreplaceable. Whether it's refactoring, better error handling, type hints, or architectural guidance - PRs and issues are welcome.

Think of it as a chance to mentor an AI-assisted developer through code review. We all benefit when experienced developers share their knowledge.

## Credits

Special thanks to:
- **Le Anh Tuan** ([@latuannetnam](https://github.com/latuannetnam)) for contributing the HTTP transport, debug logging system, and performance optimizations.
- **David Szabo-Pele** ([@davidszp](https://github.com/davidszp)) for the `source_get_content` tool and Linux auth fixes.
- **saitrogen** ([@saitrogen](https://github.com/saitrogen)) for the research polling query fallback fix.
- **VooDisss** ([@VooDisss](https://github.com/VooDisss)) for multi-browser authentication improvements.
- **codepiano** ([@codepiano](https://github.com/codepiano)) for the configurable DevTools timeout for the auth CLI.
- **Tony Hansmann** ([@997unix](https://github.com/997unix)) for contributing the `nlm setup` and `nlm doctor` commands and CLI Guide documentation.


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=jacob-bd/notebooklm-mcp-cli&type=Date)](https://star-history.com/#jacob-bd/notebooklm-mcp-cli&Date)

## License

[MIT License](LICENSE)