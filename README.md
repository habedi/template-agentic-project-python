<div align="center">
  <picture>
    <img alt="Agentic Project Template" src="docs/assets/images/logo.svg" height="25%" width="25%">
  </picture>
<br>

<h2>Agentic Project Template</h2>

[![Tests](https://img.shields.io/github/actions/workflow/status/habedi/template-agentic-project-python/tests.yml?label=tests&style=flat&labelColor=333333&logo=github&logoColor=white)](https://github.com/habedi/template-agentic-project-python/actions/workflows/tests.yml)
[![Python Version](https://img.shields.io/badge/python-%3E=3.11-3776ab?style=flat&labelColor=333333&logo=python&logoColor=white)](https://github.com/habedi/template-agentic-project-python)
[![Engine](https://img.shields.io/badge/engine-llama.cpp%20%28CUDA%2FCPU%29-orange?style=flat&labelColor=333333)](https://github.com/ggerganov/llama.cpp)
[![Default Model](https://img.shields.io/badge/default--model-google%2Fgemma--4--12B-34A853?style=flat&labelColor=333333)](https://huggingface.co/google/gemma-4-12B-it-qat-q4_0-gguf)
[![License](https://img.shields.io/badge/license-MIT-3776ab?style=flat&labelColor=333333)](LICENSE)

</div>

---

This repository is a starter template for building AI agents with the [Google Agent Development Kit](https://github.com/google/adk-python) (ADK) in
Python.

---

### Prerequisites

- Python, Version 3.11 or later.
- Uv Python package manager.
- An NVIDIA GPU (optional).

---

### Quickstart

#### 1. Setup

```bash
# Clone the repository
git clone https://github.com/habedi/template-agentic-project-python.git
cd template-agentic-project-python

# Configure environment variables
cp env.example .env

# Optionally, use the Nix development environment
nix develop

# Install dependencies (auto-detects CUDA on Linux x86_64 or installs CPU wheels)
make install
```

#### 2. Download Model

```bash
# Download the default model into .models/llm/
make download-model

# Start the Llama.cpp server in a separate terminal
make serve
```

The server exposes the (OpenAI-compatible) API at `http://127.0.0.1:8000/v1`.

#### 3. Run Agents

```bash
# Interactive terminal chat with the assistant agent
make run

# Run the multi-agent research workflow
make run-workflow

# Launch the ADK web interface
make web
```

The web interface runs at `http://127.0.0.1:8080`.

> [!NOTE]
> You can customize the model and endpoints in `.env` without modifying the code.

---

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to make a contribution.

### License

This template is licensed under the MIT License ([LICENSE](LICENSE) or https://opensource.org/licenses/MIT)

### Acknowledgements

* The logo is from [SVG Repo](https://www.svgrepo.com/svg/452634/ai) with some modifications.
