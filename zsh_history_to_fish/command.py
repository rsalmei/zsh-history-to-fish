import os
from contextlib import contextmanager

import click

from . import __description__

ZSH_HISTORY = '~/.zsh_history'
FISH_HISTORY = '~/.local/share/fish/fish_history'
DIM, Z, BLUE, YELLOW = '\033[2m', '\033[0m', '\033[94m', '\033[93m'


def history(input):
    with open(input, 'rb') as _in:
        buf = ''
        for line in _in:
            line = line.replace(b'\xe2\x80\x83\xb4', b'-').decode('utf-8').strip()
            if line.endswith('\\'):
                buf += line[:-1] + '\\n'
                continue

            if not buf:
                yield line
                continue

            yield buf + line
            buf = ''


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
        print(f'No file was written')
        return

    with open(output_file, 'a') as out:
        yield lambda x: out.write(x)
    print(f'\nFile "{output_file}" wrote successfully')


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
            command_fish, changed = converter(command_zsh)
            time = meta.split(':')[1].strip()
            command_history = f'- cmd: {command_fish}\n   when: {time}\n'
            display(command_zsh, command_fish, changed)
            writer(command_history)
