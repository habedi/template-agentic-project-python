"""Configuration settings for agents and model backends."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


def normalize_model_name(model_name: str) -> str:
    """Normalize the model identifier so local Llama.cpp models route through LiteLLM.

    Args:
        model_name: The requested model string.

    Returns:
        The normalized model string recognizable by ADK.
    """
    cleaned = model_name.strip()
    # Route local models through the OpenAI-compatible Llama.cpp server
    if cleaned.startswith("google/gemma-4") or cleaned.startswith("gemma-4"):
        return f"openai/{cleaned}"
    return cleaned


# The default model is google/gemma-4-12B running locally through Llama.cpp.
_RAW_MODEL_NAME: str = os.getenv("MODEL_NAME", "openai/google/gemma-4-12B")
DEFAULT_MODEL: str = normalize_model_name(_RAW_MODEL_NAME)

# The default local Llama.cpp OpenAI-compatible server endpoint.
DEFAULT_OPENAI_API_BASE: str = os.getenv("OPENAI_API_BASE", "http://127.0.0.1:8000/v1")
DEFAULT_OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "local")

# Populate environment variables expected by LiteLLM if unset.
os.environ.setdefault("OPENAI_API_BASE", DEFAULT_OPENAI_API_BASE)
os.environ.setdefault("OPENAI_BASE_URL", DEFAULT_OPENAI_API_BASE)
os.environ.setdefault("OPENAI_API_KEY", DEFAULT_OPENAI_API_KEY)

# Local GGUF model download and server settings.
DEFAULT_LLM_REPO: str = os.getenv("LLM_REPO", "google/gemma-4-12B-it-qat-q4_0-gguf")
DEFAULT_LLM_FILE: str = os.getenv("LLM_FILE", "gemma-4-12b-it-qat-q4_0.gguf")
DEFAULT_MODEL_DIR: Path = Path(os.getenv("MODEL_DIR", ".models/llm/gemma-4-12B"))
