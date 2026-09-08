# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Claude Code practice project for learning Claude Code fundamentals and the Claude Agent SDK. It's intentionally minimal to focus on core concepts: file operations, git integration, and project organization.

## Running the Project

**Run the main script:**
```bash
python main.py
```

Expected output: `Hello, World!`

## Project Structure

- `main.py` — Single Python file with a `hello_world()` function demonstrating basic patterns
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
