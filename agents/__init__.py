"""Agents package for Google ADK Python template."""

import logging
from importlib.metadata import PackageNotFoundError, version

from agents.config import DEFAULT_MODEL

_logger = logging.getLogger(__name__)

try:
    __version__ = version("template-agentic-project")
except PackageNotFoundError:
    __version__ = "0.1.0-alpha.1"
    _logger.debug(
        "Could not determine package version using importlib.metadata. Using default version."
    )

__all__ = ["DEFAULT_MODEL", "__version__"]
