#!/usr/bin/env bash
python -m ruff check .
python -m black .
python -m pyright
