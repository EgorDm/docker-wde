import os, click
from dotenv import load_dotenv
from wde.utils import asserte

EXECUTABLE = 'wde'
ROOT_FOLDER = os.getenv('ROOT_FOLDER', os.path.expanduser('~/.wde'))
CONFIG = None


class Config():
    __slots__ = [
        'ROOT_FOLDER',
        'WDE_ADDRESS',
        'DEV_USER',
        'DB_USER',
        'DB_PASSWORD',
        'PHP_VERSION',
        'DOMAIN_SUFFIX',
        'DOMAIN_PATH',
        'WDE_NAME',
        'DB_NAME',
    ]

    def __init__(self) -> None:
        super().__init__()
        load(self, None)

    def get_root(self, subdir=None):
        ret = os.path.abspath(self.ROOT_FOLDER)
        if subdir is not None: ret = os.path.join(ret, subdir)
        return ret

    def get_storage(self) -> str:
        return self.get_root('storage')

    def get_domain(self, name: str) -> str:
        return os.path.join(self.DOMAIN_PATH, name)


def get() -> Config:
    global CONFIG
    if CONFIG is None: CONFIG = Config()
    return CONFIG


def load(cfg: Config, root=None) -> Config:
    if root is None: root = ROOT_FOLDER

    asserte(os.path.exists(root), f'Root folder does not exitst. Run `{EXECUTABLE} install` first.')
    load_env(root)

    cfg.ROOT_FOLDER = root
    cfg.DEV_USER = os.getenv('DEV_USER', 'magnetron')
    cfg.WDE_ADDRESS = os.getenv('WDE_ADDRESS', '172.18.18.200')
    cfg.DB_USER = os.getenv('DB_USER', 'root')
    cfg.DB_PASSWORD = os.getenv('DB_PASSWORD', 'magnetron')
    cfg.PHP_VERSION = os.getenv('PHP_VERSION', '7.1')
    cfg.DOMAIN_SUFFIX = os.getenv('DOMAIN_SUFFIX', 'dev')
    cfg.DOMAIN_PATH = os.getenv('DOMAIN_PATH', '7.1')
    cfg.WDE_NAME = f'{EXECUTABLE}-{cfg.PHP_VERSION}'
    cfg.DB_NAME = 'db'

    global CONFIG
    CONFIG = cfg

    return cfg


def load_env(root):
    env_path = os.path.join(root, '.env')
    asserte(os.path.exists(env_path), f'Env file does not exist. Run `{EXECUTABLE} install` first.')
    load_dotenv(env_path)
