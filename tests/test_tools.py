"""Tests for custom tools used by the agents."""

from datetime import datetime, timezone

from agents.assistant.tools import calculate, get_current_utc_time, text_statistics
from agents.workflow.tools import gather_topic_points


def test_calculate_basic_arithmetic() -> None:
    assert calculate("2 + 2") == "2 + 2 = 4"
    assert calculate("10 - 3") == "10 - 3 = 7"
    assert calculate("5 * 6") == "5 * 6 = 30"
    assert calculate("20 / 4") == "20 / 4 = 5.0"


def test_calculate_complex_expression() -> None:
    assert calculate("15 * 4 + (100 / 5)") == "15 * 4 + (100 / 5) = 80.0"
    assert calculate("2 ** 3") == "2 ** 3 = 8"
    assert calculate("10 // 3") == "10 // 3 = 3"
    assert calculate("10 % 3") == "10 % 3 = 1"


def test_calculate_division_by_zero() -> None:
    result = calculate("10 / 0")
    assert "Error: Division by zero" in result


def test_calculate_invalid_expression() -> None:
    result = calculate("__import__('os').system('ls')")
    assert "Error evaluating expression" in result


def test_get_current_utc_time() -> None:
    time_str = get_current_utc_time()
    assert "UTC" in time_str
    # Verify that the year matches the current UTC year.
    current_year = str(datetime.now(timezone.utc).year)
    assert current_year in time_str


def test_calculate_unary_operators() -> None:
    assert calculate("-5 + 10") == "-5 + 10 = 5"
    assert calculate("+7 * 2") == "+7 * 2 = 14"


def test_text_statistics() -> None:
    text = "Hello world!\nThis is a test of text statistics."
    stats = text_statistics(text)
    assert stats["word_count"] == 9
    assert stats["line_count"] == 2
    assert stats["character_count"] == len(text)


def test_gather_topic_points() -> None:
    result = gather_topic_points("AI Agent Architecture")
    assert result["status"] == "success"
    assert result["topic"] == "AI Agent Architecture"
    assert isinstance(result["dimensions"], list)
    assert len(result["dimensions"]) > 0
