"""Basic unit tests for roast-my-deck core logic."""

import tempfile
from pathlib import Path

from src.extractor import extract_from_text
from src.roaster import build_system_prompt, load_context


def test_build_system_prompt_returns_string_without_context() -> None:
    """build_system_prompt should return a non-empty string when context is None."""
    result = build_system_prompt(None)
    assert isinstance(result, str)
    assert len(result) > 0


def test_build_system_prompt_includes_context() -> None:
    """build_system_prompt should embed context when provided."""
    context = "Sample funded deck content."
    result = build_system_prompt(context)
    assert isinstance(result, str)
    assert context in result


def test_load_context_returns_none_when_file_missing() -> None:
    """load_context should return None for a non-existent path."""
    result = load_context("/tmp/definitely_does_not_exist_xyz.txt")
    assert result is None


def test_load_context_returns_none_for_empty_file() -> None:
    """load_context should return None when the context file is empty."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("   \n  ")
        tmp_path = f.name
    result = load_context(tmp_path)
    assert result is None
    Path(tmp_path).unlink(missing_ok=True)


def test_load_context_returns_content_when_file_exists() -> None:
    """load_context should return file content when the file has text."""
    expected = "Some funded deck context here."
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(expected)
        tmp_path = f.name
    result = load_context(tmp_path)
    assert result == expected
    Path(tmp_path).unlink(missing_ok=True)


def test_extract_from_text_returns_cleaned_string() -> None:
    """extract_from_text should return a non-empty stripped string."""
    raw = "  We are Uber for laundry.  \n  Series A ready.  "
    result = extract_from_text(raw)
    assert isinstance(result, str)
    assert "Uber for laundry" in result
    assert not result.startswith(" ")
    assert not result.endswith(" ")


def test_extract_from_text_removes_null_bytes() -> None:
    """extract_from_text should strip null bytes from input."""
    raw = "Hello\x00World"
    result = extract_from_text(raw)
    assert "\x00" not in result


def test_extract_from_text_truncates_long_input() -> None:
    """extract_from_text should truncate text beyond MAX_TEXT_LENGTH."""
    long_text = "a" * 100_000
    result = extract_from_text(long_text)
    assert len(result) <= 50_000
