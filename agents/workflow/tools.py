"""Tools for workflow agents."""

from typing import Any


def gather_topic_points(topic: str) -> dict[str, Any]:
    """Retrieves reference dimensions and analysis points for a topic.

    Args:
        topic: The topic or domain being researched.

    Returns:
        A dictionary with categories, key focus areas, and analysis guidelines.
    """
    cleaned_topic = topic.strip()
    return {
        "topic": cleaned_topic,
        "dimensions": [
            "Architectural patterns and best practices",
            "Performance and scalability trade-offs",
            "Ecosystem tooling and production deployment",
            "Testing, verification, and evaluation strategies",
        ],
        "status": "success",
    }
