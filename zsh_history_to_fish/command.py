import os
import sys
from contextlib import contextmanager
import subprocess
from itertools import starmap

import click

from . import __description__

ZSH_HISTORY_FILE = '~/.zsh_history'
FISH_HISTORY_FILE = '~/.local/share/fish/fish_history'
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
    stream = map(lambda x: x.split(maxsplit=2)[1:], read_history(input_file))
    yield from filter(lambda x: len(x) > 1, stream)


def naive_zsh_to_fish(cmd):
    result = cmd \
        .replace(' && ', '&&') \
        .replace('&&', '; and ') \
        .replace(' || ', '||') \
        .replace('||', '; or ')
    return result


def display_changed(zsh, fish):
    if zsh != fish:
        return f'{DIM}zsh {Z}: {zsh}\n' \
               f'{DIM}fish{Z}: {YELLOW}{fish}{Z}'


@contextmanager
def writer_factory(output_file, dry_run):
    if dry_run:
        yield lambda x: None
        print(f'No file has been written.')
        return

    with open(output_file, 'a') as out:
        yield lambda x: out.write(x)
    print(f'\nFile "{output_file}" has been written successfully.')


@click.command(help=__description__)
@click.version_option()
@click.argument('input_file', type=click.Path(exists=True), required=False,
                default=os.path.expanduser(ZSH_HISTORY_FILE))
@click.option('--output_file', '-o', type=click.Path(),
              default=os.path.expanduser(FISH_HISTORY_FILE),
              help='Optional output, will append to fish history by default')
@click.option('--dry-run', '-d', is_flag=True, help='Do not write anything to filesystem')
@click.option('--no-convert', '-n', is_flag=True, help='Do not naively convert commands')
def exporter(input_file, output_file, dry_run, no_convert):
    print('ZSH history to Fish')
    print('===================')
    print(f'{DIM}input {Z}: {BLUE}{input_file}{Z} ({YELLOW}naive-convert={not no_convert}{Z})')
    print(f'{DIM}output{Z}: {BLUE}{"dry run mode" if dry_run else output_file}{Z}')

    converter = (lambda x: x) if no_convert else naive_zsh_to_fish
    changed = []
    with writer_factory(output_file, dry_run) as writer:
        for i, (timestamp, command_zsh) in enumerate(parse_history(input_file)):
            command_fish = converter(command_zsh)
            fish_history = f'- cmd: {command_fish}\n  when: {timestamp}\n'
            writer(fish_history)
            if command_zsh != command_fish:
                changed.append((command_zsh, command_fish))
            if i % 1000 == 0:
                print('.', end='')
                sys.stdout.flush()
        print(f'\nProcessed {BLUE}{i + 1}{Z} commands.')
    if changed:
        print('Converted commands:\n', '\n'.join(starmap(display_changed, changed)), sep='')
