"""Tests for model download and server scripts."""

from pathlib import Path
from unittest.mock import patch

from scripts.download_model import download_model
from scripts.serve_llama import detect_cuda_available, find_model_path


def test_detect_cuda_available() -> None:
    # Verify that the function executes and returns a boolean value.
    res = detect_cuda_available()
    assert isinstance(res, bool)


def test_find_model_path_nonexistent(tmp_path: Path) -> None:
    res = find_model_path(tmp_path, "model.gguf")
    assert res is None


def test_find_model_path_exists(tmp_path: Path) -> None:
    dummy_file = tmp_path / "gemma-4-12b.gguf"
    dummy_file.write_text("dummy")
    res = find_model_path(tmp_path, "gemma-4-12b.gguf")
    assert res == dummy_file


def test_download_model_already_present(tmp_path: Path) -> None:
    dummy_file = tmp_path / "model.gguf"
    dummy_file.write_text("dummy content")

    with patch("scripts.download_model.hf_hub_download") as mock_hf:
        result = download_model("repo/id", "model.gguf", tmp_path)
        assert result == dummy_file
        mock_hf.assert_not_called()
