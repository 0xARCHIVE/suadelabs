# Suade Labs Coding Test

## Installation

I have chosen to use `poetry` and `pyenv`. To setup and use the environment:

```shell
poetry install
poetry shell
```

This will automatically create a virtual environment and install the required dependencies.

## Usage

We can use Flask's in-built server for development purposes:

```shell
python run.py
```

I would use Gunicorn (or something similar) in production.

## Development

### Pre-commit Checks

To run them manually:

```shell
pre-commit run --all-files
```

This will run a series of linting and type-checking (`flake8`, `black`, `mypy`) and tell you what needs to be fixed. You may need to run it more than once. It will be automatically run when attempting to commit a change.

### Testing

To run tests:

```shell
pytest
```

For test coverage:

```shell
pytest --cov=app tests/
```

## General Comments

* I have deliberately tried to focus on code readability, as opposed to optimisation ("premature optimisation is the root of all evil"). The current dataset is very small once filtered by date (tens of items).
