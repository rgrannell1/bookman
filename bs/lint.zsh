#! /usr/bin/env zsh
uv run ruff check src && uv run ruff format --check src && uv run vulture src/
