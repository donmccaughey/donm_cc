# gen

Custom site generator for [donm.cc](https://donm.cc/).

## Python setup notes

Install [`pyenv`](https://github.com/pyenv/pyenv) to manage Python versions.

1. `brew install pyenv`
2. `brew install pyenv-virtualenv` for creating virtualenvs.
3. Add `PYENV_ROOT` env variable and `pyenv` to `PATH` to your shell's startup scrips.
4. Add `eval "$(pyenv init -)"` to your startup scripts.
5. Add `eval "$(pyenv virtualenv-init -)"` to your startup scripts.
6. `pyenv versions` to list installed Python versions.
7. `pyenv install 3.10.0` to install a recent Python version.
8. `pyenv virtualenv 3.10.0 gen-venv` to create a virtualenv for this project.
9. Edit the `gen/.python-version` file, setting the version to `gen-venv`.
10. In PyCharm's *Preferences* dialog, select 
     *Project: Gen | Python Interpreter* in the tree of options and choose  
     `gen-venv` as the Python version.

## Strip image metadata notes

Install [`ImageMagick`](https://imagemagick.org).

1. `[magick] identify -verbose PATH` to print out metadata
2. `[magick] mogrify -strip PATH` to remove unnecessary metadata

Notes on the [`-strip`](https://imagemagick.org/script/command-line-options.php#strip)
command line option.

Alternately, [ExifTool](https://exiftool.org) can do the same thing using
`exiftool -all= <path>`.

Useful discussion on removing metadata: [How can I read and remove meta (exif) 
data from my photos using the command line?][1].

[1]: https://askubuntu.com/questions/260810/how-can-i-read-and-remove-meta-exif-data-from-my-photos-using-the-command-line/968598
