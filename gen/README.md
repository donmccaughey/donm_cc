# gen

Custom site generator for [donm.cc](https://donm.cc/).

## Python setup notes

Install [`pyenv`](https://github.com/pyenv/pyenv) to manage Python versions.

1. `brew install pyenv`
1. `brew install pyenv-virtualenv` for creating virtualenvs.
1. Add `PYENV_ROOT` env variable and `pyenv` to `PATH` to your shell's startup scrips.
1. Add `eval "$(pyenv init -)"` to your startup scripts.
1. Add `eval "$(pyenv virtualenv-init -)"` to your startup scripts.
1. `pyenv install 3.9.4` to install a recent Python version.
1. `pyenv virtualenv 3.9.4 gen-venv` to create a virtualenv for this project.
1. Edit the `gen/.python-version` file, setting the version to `gen-venv`.
1. Select the `gen-venv` Python version in PyCharm's *Project: Gen | Python Interpreter* dialog.
