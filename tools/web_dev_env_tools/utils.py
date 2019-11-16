import os
import subprocess
from typing import Optional, Union

from web_dev_env_tools import constants, container


def get_rel_domain_path(path) -> Optional[str]:
    return container.translate_path(constants.DOMAIN_PATH, container.get_path('domains'), path)


def get_relative_path(root, path) -> Optional[str]:
    root = os.path.abspath(root)
    path = os.path.abspath(path)
    rel = os.path.relpath(path, root)

    if rel.startswith('..'):
        return None
    else:
        return rel


def command(cmd: Union[list, str], cwd=None, capture=True, shell=False) -> Optional[str]:
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE if capture else None,
        cwd=cwd,
        shell=shell
    )
    if capture and result.returncode == 0:
        return str(result.stdout.decode('utf-8').strip())
    elif result.returncode == 0:
        return ''
    else:
        return None
