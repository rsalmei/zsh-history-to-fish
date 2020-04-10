import os
from contextlib import contextmanager
import subprocess

import click

from . import __description__

ZSH_HISTORY = '~/.zsh_history'
FISH_HISTORY = '~/.local/share/fish/fish_history'
DIM, Z, BLUE, YELLOW = '\033[2m', '\033[0m', '\033[94m', '\033[93m'

# use zsh itself to read history file, since it is not utf-8 encoded.
# suggested in https://github.com/rsalmei/zsh-history-to-fish/issues/2
ZSH_HISTORY_READER = "zsh -i -c 'fc -R {}; fc -l -t \"%s\" 0'"


def read_history(input_file):
    command = ZSH_HISTORY_READER.format(input_file)
    p = subprocess.run(command, capture_output=True, shell=True, encoding='utf8')
    lines = p.stdout.splitlines()
    yield from map(lambda x: x.replace('\\n', '\n'), lines)


def parse_history(input_file):
    yield from map(lambda x: x.split(maxsplit=2)[1:], read_history(input_file))

def zsh_to_fish(cmd):
    result = cmd \
        .replace(' && ', '&&') \
        .replace('&&', '; and ') \
        .replace(' || ', '||') \
        .replace('||', '; or ')
    return result, cmd != result


def display(zsh, fish, changed):
    color = YELLOW if changed else BLUE
    print(f'{DIM}zsh {Z}: {zsh}\n'
          f'{DIM}fish{Z}: {color}{fish}{Z}')


@contextmanager
def output_gen(output_file, dry_run):
    if dry_run:
        yield lambda x: None
        print(f'No file has been written')
        return

    with open(output_file, 'a') as out:
        yield lambda x: out.write(x)
    print(f'\nFile "{output_file}" has been written successfully')


@click.command(help=__description__)
@click.version_option()
@click.argument('input', type=click.Path(exists=True), required=False,
                default=os.path.expanduser(ZSH_HISTORY))
@click.option('--output', '-o', type=click.Path(), help='Optional output, will append to fish history by default',
              default=os.path.expanduser(FISH_HISTORY))
@click.option('--dry-run', '-d', is_flag=True, help='Do not write anything to filesystem')
@click.option('--no-convert', '-n', is_flag=True, help='Do not naively convert commands')
def exporter(input, output, dry_run, no_convert):
    converter = (lambda x: (x, False)) if no_convert else zsh_to_fish
    with output_gen(output, dry_run) as writer:
        for line in history(input):
            meta, command_zsh = line.split(';', 1)
        for timestamp, command_zsh in parse_history(input_file):
            command_fish, changed = converter(command_zsh)
            command_history = f'- cmd: {command_fish}\n  when: {time}\n'
            display(command_zsh, command_fish, changed)
            writer(command_history)
