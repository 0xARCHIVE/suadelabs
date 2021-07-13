# Suade Labs Coding Test

![Python >= 3.9.6](https://img.shields.io/badge/python-%3E%3D%203.9.6-blue?style=flat-square)

## General Comments

* I have worked on this little project in my free time, around quite a busy work schedule.

* I have deliberately tried to focus on code readability, as opposed to optimisation ("premature optimisation is the root of all evil"). The current dataset is very small once filtered by date (tens of items).

* My git commits are too large and infrequent, and my docstrings don't have much thought put into them. This is mainly to speed up development, in the knowledge that this is a toy app.

* I have supplied an SQLite database file for convenience (`app.db`). I've simply recreated the structure from the CSV files and imported the data.

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

### Report Endpoint

The server will be created on `127.0.0.1:8080` by default. The API has one endpoint:

```
/report/YYYY/MM/DD
```

Useful error messages are provided to the user, for example:

```javascript
{
  'error': 'Invalid date entered'
}
```

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
