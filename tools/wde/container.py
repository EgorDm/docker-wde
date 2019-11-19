import os
import subprocess
from typing import Optional, Union

import click

from wde import config, utils


def get_path(subdir=None) -> str:
    ret = f'/home/{config.get().DEV_USER}'

    if subdir is not None:
        ret = os.path.join(ret, subdir)

    return ret


def translate_path(root, container_root, path) -> Optional[str]:
    rel = utils.get_relative_path(root, path)

    if rel is None:
        return None

    return os.path.join(container_root, rel)


def translate_path_mounted(path) -> Optional[str]:
    rel = translate_path(config.get().DOMAIN_PATH, get_path('domains'), path)
    if rel is not None: return rel
    return None


def get_ip(name: str) -> Optional[str]:
    return exec(name, ['hostname', '-i'], use_mounted=False)


def get_status(name: str) -> Optional[str]:
    return utils.command(['docker', 'ps', f"--filter=name={name}", '--format', "'{{.Status}}'"])


def exec(name: str, cmd: Union[list, str], user: str = None, capture: bool = True, shell=False,
         require_mounted=False, use_mounted=True) -> Optional[str]:
    if type(cmd) is str: shell = True

    final_cmd = ['docker', 'exec', '-it', '-e', 'TERM=xterm-256color']
    if user is not None:
        final_cmd += ['-u', user]
    rel = translate_path_mounted(os.getcwd())
    if rel is not None and use_mounted:
        final_cmd += ['-w', rel]
    elif require_mounted:
        click.echo('You must be in a mounted folder to do that!')
        exit(1)

    final_cmd.append(name)

    if shell:
        final_cmd += ['bash', '-c', cmd]
    else:
        final_cmd += cmd

    return utils.command(final_cmd, capture=capture)
