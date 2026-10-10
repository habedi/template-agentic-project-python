# AGENTS.md

Guidance for coding agents working on this repository.
It covers what cannot be read off the code.
For the layout, run `ls`; for the build targets, run `make help`; for dependencies, read `pyproject.toml`; for agent architecture, read `README.md`.

## Mission

This repository is a template for developing AI agents in Python using the Google Agent Development Kit (ADK).
It defaults to local model execution with Google Gemma 4 on Llama.cpp. Priorities, in order:

1. Correctness and reliable agent execution.
2. Local-first privacy and offline capability using Llama.cpp.
3. Clean structure with Google ADK conventions.
4. Maintainable, tested code with complete test coverage.
5. Cross-platform support across Linux, macOS, and Windows.

## Core Rules

- Prefer small, focused changes over large refactoring.
- Add comments only when they clarify non-obvious behavior.
- Do not add features, error handling, or abstractions beyond what the task needs.
- Do not push, tag, or release. Prepare the change and leave the remote to the maintainer.

## Writing Style

These guidelines apply to code comments, documentation pages, commit messages, and chat.

- Write in plain English with short sentences and everyday words. No colorful adjectives ("parser", not "robust parser").
- No em dashes. Restructure the sentence or use a semicolon.
- No colons in the middle of a sentence in new prose. A colon that introduces a code block or a list is fine. Reword existing text only when touching
  it anyway.
- Do not write that something "lives under" or "lives in" a path. Write "is in" or "is defined in".
- Oxford commas in inline lists.
- Headings in Title Case; minor words (a, an, the, and, but, or, for, in, on, at, to, by, of) stay lowercase unless first. Capitalize only the first
  part of a hyphenated compound ("Tail-call Detection").
- List items: sentence-case lead-in, never bold ("Upvalue capture: ..." not "**Upvalue Capture**: ..."). Prefer noun phrases for checklist items.
- Capitalize proper nouns (Python, Google, ADK, Gemma, Llama.cpp, Nix) and nothing else mid-sentence.
- Complete sentences, no made-up words or abbreviations, participial phrases only sparingly.

## Conventions

- Python 3.11 or later. Uv manages dependencies and environments.
- Ruff enforces code formatting and lint rules; `make lint` checks them and `make format` applies them.
- Mypy enforces static type annotations; `uv run mypy agents tests` runs type checks.
- Python names use `snake_case` for functions, methods, and variables, and `PascalCase` for classes. Agent directories use `snake_case`.
- Nix flake is in `flake.nix` and provides development tools and dynamic library paths.

## Architecture Rules

Agents are built with the Google Agent Development Kit (ADK) and are defined in `agents/`. The backend and model configuration is in
`agents/config.py`. Rules that the types do not enforce:

- Local inference runs through Llama.cpp via `scripts/serve_llama.py`. The local server exposes an OpenAI-compatible API on
  `http://127.0.0.1:8001/v1`.
- Model normalization routes local Gemma models through `openai/` so LiteLLM targets the local server without external API calls.
- Agent tools are defined as standalone Python functions with complete type hints and docstrings. ADK derives function schemas from docstrings and
  signatures.
- Multi-agent pipelines use `SequentialAgent` or `ParallelAgent` orchestrators with `LlmAgent` leaf nodes.
- Environment configuration is read through `.env` with fallbacks defined in `agents/config.py`. Never hardcode host addresses, ports, or API keys in
  agent logic.
- Agent session state uses ADK session services. Local development defaults to in-memory or `.adk` session storage.

## Validation

Run the narrowest target while iterating (`uv run pytest tests/test_assistant.py` for a single test file) and `make test` plus `make lint` before
declaring done.

Where tests go:

- `tests/test_assistant.py` for assistant agent behaviors and tools.
- `tests/test_workflow.py` for multi-agent sequential pipeline execution.
- `tests/test_tools.py` for standalone tool execution and edge cases.
- `tests/test_discovery.py` for ADK agent loading and schema registration.
- `tests/test_scripts.py` for helper scripts such as model download and server CLI options.
- `evalsets/` for ADK evaluation sets.

Prefer targeted assertions per case over broad output comparisons, and keep tests deterministic.

## Documentation

- `agents/__init__.py` and agent definitions form the template code. Keep docstrings current.
- `docs/` is the MkDocs site and `README.md` is the front page. A change visible to users updates the page that describes it, and stale text found
  along the way is fixed in the same patch.
- Every command and code sample in the documentation must work. Check it before committing.

## Review and Commit Hygiene

- Review output lists only `P0` (incorrect behavior, broken build or tests) and `P1` (likely bug, missing validation, platform handling) issues, each
  as severity, `file:line`, issue, why it matters, and the fix direction. No style-only feedback, no praise.
- One logical change per commit. A PR description states the behavioral change, the tests added, and whether it was verified interactively.
