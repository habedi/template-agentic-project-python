"""Starts the local Llama.cpp OpenAI-compatible HTTP server."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from agents.config import DEFAULT_LLM_FILE, DEFAULT_MODEL_DIR


def detect_cuda_available() -> bool:
    """Checks whether an NVIDIA GPU with CUDA drivers is available."""
    try:
        res = subprocess.run(
            ["nvidia-smi", "-L"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return res.returncode == 0 and len(res.stdout.strip()) > 0
    except FileNotFoundError:
        return False


def find_model_path(model_dir: Path, filename: str) -> Path | None:
    """Locates the GGUF model in the given directory or any of its subdirectories."""
    direct = model_dir / filename
    if direct.is_file():
        return direct
    matches = list(model_dir.glob(f"**/{filename}"))
    if matches:
        return matches[0]
    # Check for any .gguf file in the model directory
    any_gguf = list(model_dir.glob("**/*.gguf"))
    if any_gguf:
        return any_gguf[0]
    return None


def run_server(
    model_path: Path,
    host: str = "127.0.0.1",
    port: int = 8000,
    context_size: int = 8192,
    gpu_layers: int = -1,
    model_alias: str = "google/gemma-4-12B",
) -> None:
    """Launches the Llama.cpp server for the given GGUF model.

    Args:
        model_path: Absolute or relative path to the GGUF file.
        host: Host IP to bind to.
        port: Port number.
        context_size: Context window in tokens.
        gpu_layers: GPU layers to offload (-1 for all, 0 for CPU).
        model_alias: Name alias exposed on the OpenAI endpoints.
    """
    cuda_available = detect_cuda_available()
    layers = gpu_layers if (cuda_available and gpu_layers != 0) else 0

    print("=" * 60)
    print("🦙 Starting llama.cpp Server")
    print(f"Model File:  {model_path}")
    print(f"Model Alias: {model_alias}")
    print(f"Endpoint:    http://{host}:{port}/v1")
    print(f"Context:     {context_size} tokens")
    print(f"GPU Layers:  {layers} (CUDA available: {cuda_available})")
    print("=" * 60)

    # If native llama-server binary is present on PATH, prefer it
    native_llama_server = shutil.which("llama-server")
    if native_llama_server:
        print(f"Using native binary: {native_llama_server}")
        cmd = [
            native_llama_server,
            "-m",
            str(model_path),
            "--host",
            host,
            "--port",
            str(port),
            "-c",
            str(context_size),
            "-ngl",
            str(layers),
            "-a",
            model_alias,
        ]
    else:
        # Fallback to python -m llama_cpp.server
        print("Using llama-cpp-python server...")
        cmd = [
            sys.executable,
            "-m",
            "llama_cpp.server",
            "--model",
            str(model_path),
            "--model_alias",
            model_alias,
            "--host",
            host,
            "--port",
            str(port),
            "--n_ctx",
            str(context_size),
            "--n_gpu_layers",
            str(layers),
        ]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nStopping llama.cpp server.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the local Llama.cpp server for google/gemma-4-12B."
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=DEFAULT_MODEL_DIR,
        help=f"Directory containing the GGUF file (default: {DEFAULT_MODEL_DIR})",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=DEFAULT_LLM_FILE,
        help=f"GGUF filename (default: {DEFAULT_LLM_FILE})",
    )
    parser.add_argument(
        "--model-path",
        type=Path,
        default=None,
        help="Direct path to GGUF model file (overrides --model-dir)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("LLAMA_HOST", "127.0.0.1"),
        help="Host address to bind (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("LLAMA_PORT", "8000")),
        help="Port number to bind (default: 8000)",
    )
    parser.add_argument(
        "--context-size",
        type=int,
        default=int(os.getenv("CONTEXT_SIZE", "8192")),
        help="Context window size in tokens (default: 8192)",
    )
    parser.add_argument(
        "--gpu-layers",
        type=int,
        default=int(os.getenv("GPU_LAYERS", "-1")),
        help="Number of GPU layers to offload (-1 for all, 0 for CPU)",
    )
    parser.add_argument(
        "--model-alias",
        type=str,
        default=os.getenv("MODEL_ALIAS", "google/gemma-4-12B"),
        help="Model alias exposed by server (default: google/gemma-4-12B)",
    )

    args = parser.parse_args()

    model_file = args.model_path or find_model_path(args.model_dir, args.filename)
    if not model_file or not model_file.is_file():
        print(f"Error: Model not found at '{args.model_dir / args.filename}'", file=sys.stderr)
        print("Please download the model first with:", file=sys.stderr)
        print("    make download-model", file=sys.stderr)
        sys.exit(1)

    run_server(
        model_path=model_file,
        host=args.host,
        port=args.port,
        context_size=args.context_size,
        gpu_layers=args.gpu_layers,
        model_alias=args.model_alias,
    )


if __name__ == "__main__":
    main()
