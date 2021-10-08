# gen

Custom site generator for [donm.cc](https://donm.cc/).

## Python setup notes

Install [`pyenv`](https://github.com/pyenv/pyenv) to manage Python versions.

1. `brew install pyenv`
2. `brew install pyenv-virtualenv` for creating virtualenvs.
3. Add `PYENV_ROOT` env variable and `pyenv` to `PATH` to your shell's startup scrips.
4. Add `eval "$(pyenv init -)"` to your startup scripts.
5. Add `eval "$(pyenv virtualenv-init -)"` to your startup scripts.
6. `pyenv install 3.10.0` to install a recent Python version.
7. `pyenv virtualenv 3.10.0 gen-venv` to create a virtualenv for this project.
8. Edit the `gen/.python-version` file, setting the version to `gen-venv`.
9. In PyCharm's *Preferences* dialog, select 
    *Project: Gen | Python Interpreter* in the tree of options and choose  
    `gen-venv` as the Python version.
