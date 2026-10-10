-include .env

# Variables
PYTHON       ?= python3
PIP          ?= pip3
DEP_MNGR     ?= uv
DOCS_DIR     ?= docs
AGENTS_DIR   ?= agents
MODEL_DIR    ?= .models/llm/gemma-4-12B
ADK_WEB_PORT ?= 8081

# Hardware Acceleration: Auto-detect NVIDIA CUDA on Linux
CUDA        ?= $(shell if [ "$$(uname -sm)" = "Linux x86_64" ] && nvidia-smi -L >/dev/null 2>&1 && which nvcc >/dev/null 2>&1; then echo 1; else echo 0; fi)
UV_EXTRA    ?= --extra $(if $(filter 1,$(CUDA)),cuda,cpu) --extra dev

ifeq ($(CUDA),1)
export CMAKE_ARGS ?= -DGGML_CUDA=ON -DGGML_NATIVE=OFF
endif

# Directories and files to clean
CACHE_DIRS  = .mypy_cache .pytest_cache .ruff_cache .adk
COVERAGE    = .coverage htmlcov coverage.xml
DIST_DIRS   = dist junit
TMP_DIRS   = site

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show help messages for all available targets
	@grep -E '^[a-zA-Z_-]+:.*## .*$$' Makefile | \
	awk 'BEGIN {FS = ":.*## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Setup and Installation
.PHONY: setup
setup: install ## Install system dependencies and sync project environment

.PHONY: install
install: ## Sync Python dependencies with uv
	$(DEP_MNGR) sync $(UV_EXTRA)

# Local Model Management (using Llama.cpp)
.PHONY: download-model
download-model: ## Download the default model from Hugging Face
	$(DEP_MNGR) run python scripts/download_model.py

.PHONY: serve
serve: ## Start the local Llama.cpp OpenAI-compatible server for the default model
	$(DEP_MNGR) run python scripts/serve_llama.py

# Agent Execution and Development
.PHONY: run
run: ## Run interactive CLI with default assistant agent (connects to local Llama.cpp)
	$(DEP_MNGR) run adk run $(AGENTS_DIR)/assistant

.PHONY: run-workflow
run-workflow: ## Run interactive CLI with the multi-agent research workflow
	$(DEP_MNGR) run adk run $(AGENTS_DIR)/workflow

.PHONY: web
web: ## Launch the ADK web interface server
	$(DEP_MNGR) run adk web --port $(ADK_WEB_PORT) $(AGENTS_DIR)

.PHONY: eval
eval: ## Run agent evaluation against evaluation sets
	$(DEP_MNGR) run adk eval $(AGENTS_DIR)/assistant $(AGENTS_DIR)/assistant/evals/assistant.evalset.json

# Quality and Testing
.PHONY: test
test: ## Run unit and integration tests
	$(DEP_MNGR) run pytest

.PHONY: lint
lint: ## Run linter checks
	$(DEP_MNGR) run ruff check --fix

.PHONY: format
format: ## Format code
	$(DEP_MNGR) run ruff format

.PHONY: typecheck
typecheck: ## Typecheck code
	$(DEP_MNGR) run mypy .

.PHONY: setup-hooks
setup-hooks: ## Install Git hooks (pre-commit and pre-push)
	$(DEP_MNGR) run pre-commit install --hook-type pre-commit
	$(DEP_MNGR) run pre-commit install --hook-type pre-push
	$(DEP_MNGR) run pre-commit install-hooks

.PHONY: test-hooks
test-hooks: ## Test Git hooks on all files
	$(DEP_MNGR) run pre-commit run --all-files

# Documentation
.PHONY: docs
docs: ## Build documentation
	$(DEP_MNGR) run mkdocs build

# Build and Publish
.PHONY: build
build: ## Build distributions
	$(DEP_MNGR) build

.PHONY: publish
publish: build ## Publish to PyPI (requires PYPI_TOKEN)
	$(DEP_MNGR) publish $(if $(PYPI_TOKEN),--token $(PYPI_TOKEN),)

# Maintenance
.PHONY: clean
clean: ## Remove caches and build artifacts
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf $(CACHE_DIRS) $(COVERAGE) $(DIST_DIRS) $(TMP_DIRS)

.PHONY: clean-models
clean-models: ## Remove downloaded local GGUF models
	rm -rf .models
