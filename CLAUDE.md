# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangChain/LangGraph agent practice project (repo: `LangchainAgent`, formerly `ClaudeAgentSDK`). Numbered lessons in `lessons/` build up an agent over an Excel BOM workbook: model, messages, tools, agent, memory, hooks, MCP server/client, role-based access, and a Streamlit UI.

## Running the Project

```bash
pip install -r requirements.txt
python lessons/08c_secure_agent.py   # CLI chat with login
streamlit run lessons/08d_app.py     # web chat
```

Secrets live in `source/.env` (git-ignored); user credentials in `users.json` (git-ignored, create with `python lessons/users.py`).

## Project Structure

- `lessons/` — numbered lesson scripts plus helpers (`bom_tools.py`, `access.py`, `users.py`)
- `source/` — BOM workbook and `.env`
- `.claude/settings.json` — Project-scoped Claude Code configuration (permissions, environment variables, hooks)

## Git Workflow

The project tracks configuration and learning progress in git. Key notes:
- Current branch: `main` (primary branch)
- All changes should be committed with descriptive messages
- The `.claude/settings.json` file is committed so Claude Code settings persist across environments

## Configuration

Project-scoped settings are already configured in `.claude/settings.json`:
- **Permissions:** git and npm operations, file read/write/edit, glob and grep
- **Environment variables:** `DEBUG=false`, `NODE_ENV=development`
- **Hooks:** PostToolUse hooks configured for Write/Edit operations

Future instances can extend these settings as the project grows.
