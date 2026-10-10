"""Download script for local GGUF models from Hugging Face."""

import argparse
import sys
from pathlib import Path

from agents.config import DEFAULT_LLM_FILE, DEFAULT_LLM_REPO, DEFAULT_MODEL_DIR
from huggingface_hub import hf_hub_download

DEFAULT_REPO = DEFAULT_LLM_REPO
DEFAULT_FILE = DEFAULT_LLM_FILE
DEFAULT_DIR = DEFAULT_MODEL_DIR


def download_model(repo_id: str, filename: str, target_dir: Path) -> Path:
    """Downloads a GGUF model file from Hugging Face if not already present.

    Args:
        repo_id: The Hugging Face model repository ID.
        filename: The GGUF filename within the repository.
        target_dir: The local directory to store the model.

    Returns:
        The path to the downloaded GGUF file.
    """
    target_path = target_dir / filename
    if target_path.is_file():
        print(f"Model already present at {target_path} (skipping download).")
        return target_path

    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {filename} from {repo_id} to {target_dir}...")
    downloaded_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=str(target_dir),
    )
    print(f"Model successfully saved to {downloaded_path}")
    return Path(downloaded_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download GGUF model files for local Llama.cpp inference."
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=DEFAULT_REPO,
        help=f"Hugging Face repository ID (default: {DEFAULT_REPO})",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=DEFAULT_FILE,
        help=f"GGUF filename to download (default: {DEFAULT_FILE})",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=DEFAULT_DIR,
        help=f"Local target directory (default: {DEFAULT_DIR})",
    )

    args = parser.parse_args()
    try:
        download_model(repo_id=args.repo, filename=args.file, target_dir=args.dir)
    except Exception as exc:
        print(f"Error downloading model: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
