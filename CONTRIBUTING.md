## Contribution Guidelines

Thank you for considering contributing to this project!
Contributions are always welcome and appreciated.

### How to Contribute

Check the [issue tracker](https://github.com/habedi/template-agentic-project-python/issues) to see if an issue already exists.

#### Reporting Bugs

1. Open an issue on the [issue tracker](https://github.com/habedi/template-agentic-project-python/issues).
2. Include the steps to reproduce the observed behavior, and attach relevant logs.

#### Suggesting Features

1. Open an issue on the [issue tracker](https://github.com/habedi/template-agentic-project-python/issues).
2. Describe the feature, its purpose, and potential implementation steps.

### Submitting Pull Requests

- Verify that all tests pass before submitting a pull request.
- Write a clear description of your changes and why you made them.

> [!IMPORTANT]
> By submitting a pull request, you agree to license your contributions under the project license.

### Development Workflow

#### Prerequisites

Install GNU Make if it's not already installed on your system.

```shell
## For Debian-based systems like Debian, Ubuntu, etc.
sudo apt-get install make
```

If you use Nix, start a shell with all tools ready:

```shell
nix develop
```

- Use the `make setup` command to install the development dependencies.
- Use the `make install` command to install the Python dependencies.

#### Code Style

- Use the `make format` command to format the code.

#### Running Tests

- Use the `make test` command to run the tests.

#### Running Linter Checks

- Use the `make lint` command to run the linter checks.

#### See Available Commands

- Run `make help` to see all available commands for managing different tasks.

### Code of Conduct

We adhere to the project's [Code of Conduct](CODE_OF_CONDUCT.md).
