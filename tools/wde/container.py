import os
import subprocess
from typing import Optional, Union, List

from wde import config, utils


def get_path(subdir=None) -> str:
    ret = f'/home/{config.get().DEV_USER}'
    if subdir is not None: ret = os.path.join(ret, subdir)
    return ret


def translate_path(root, container_root, path) -> Optional[str]:
    rel = utils.get_relative_path(root, path)
    if rel is None: return None
    return os.path.join(container_root, rel)


def translate_path_mounted(path) -> Optional[str]:
    rel = translate_path(config.get().DOMAIN_PATH, get_path('domains'), path)
    if rel is not None: return rel
    return None


def get_ip(name: str) -> Optional[str]:
    return build_cmd(name, ['hostname', '-i']).exec()


def get_status(name: str) -> Optional[str]:
    return utils.command(['docker', 'ps', f"--filter=name={name}", '--format', "'{{.Status}}'"])


class Command:
    cmd: list

    def __init__(self, cmd: list) -> None:
        super().__init__()
        self.cmd = cmd

    def exec(self, capture=True) -> Optional[str]:
        for i in range(len(self.cmd)):
            if self.cmd[i] == '-it': self.cmd[i] = '-i'
        return utils.command(self.cmd, capture=capture)

    def exec_it(self) -> bool:
        return utils.command_it(self.cmd)


def build_cmd(name: str, cmd: Union[list, str], user=None, shell=False, cwd=None, req_mount=False) -> Command:
    if type(cmd) is str: shell = True

    final_cmd = ['docker', 'exec', '-it', '-e', 'TERM=xterm-256color']
    if user is not None: final_cmd += ['-u', user]

    rel = translate_path_mounted(os.getcwd() if cwd is None else cwd)
    if rel is not None: final_cmd += ['-w', rel]
    utils.asserte(not (req_mount and rel is None), 'You must be in a mounted folder to do that!')

    final_cmd.append(name)

    if shell: final_cmd += ['bash', '-i', '-c', escape_cmd(cmd)]
    else: final_cmd += cmd

    return Command(final_cmd)


def escape_cmd(cmd: Union[list, str]) -> str:
    if type(cmd) is str: return cmd

    res = []
    for t in cmd:
        t = t.replace('"', '\\"').replace('\'', '\\\'')
        if ' ' in t: t = f'\\"{t}\\"'
        res.append(t)
    return ' '.join(res)
