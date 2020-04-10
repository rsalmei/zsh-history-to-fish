[<img align="right" src="https://cdn.buymeacoffee.com/buttons/default-orange.png" width="217px" height="51x">](https://www.buymeacoffee.com/rsalmei)

[![PyPI version](https://img.shields.io/pypi/v/zsh-history-to-fish.svg)](https://pypi.python.org/pypi/zsh-history-to-fish/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/zsh-history-to-fish.svg)](https://pypi.python.org/pypi/zsh-history-to-fish/)
[![PyPI status](https://img.shields.io/pypi/status/zsh-history-to-fish.svg)](https://pypi.python.org/pypi/zsh-history-to-fish/)


# Bring your ZSH history to Fish shell

This is a simple tool to ease the migration from ZSH to Fish shell, without losing your hard-earned history commands.

As I was migrating myself, I've found out there's no tool to do this automatically, so I've made one for my own use.
For that, I had to search for the specifications of both history files, and ended up involved in multiple threads with the right devs to try to understand and make it work.
In the process, I've stumbled upon several people interested in a such a tool.

Well, it has worked! So I've wrapped it in a python package to make it easy to use, and now I'm sharing with anyone who may need it! It's released on PyPI.


## Get it

Just do in your zsh shell:

```bash
$ pip install zsh-history-to-fish
```


## How to use

```bash
$ zsh-history-to-fish --help
Usage: zsh-history-to-fish [OPTIONS] [INPUT]

  Bring your ZSH history to Fish shell.

Options:
  --version          Show the version and exit.
  -o, --output PATH  Optional output, will append to fish history by default
  -d, --dry-run      Do not write anything to filesystem
  -n, --no-convert   Do not naively convert commands
  --help             Show this message and exit.
```


## License
This software is licensed under the MIT License. See the LICENSE file in the top distribution directory for the full license text.


## Did you like it?

Thanks for your interest!

I wish this tool can be useful to you! :)
