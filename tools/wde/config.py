import os, click
from dotenv import load_dotenv

ROOT_FOLDER = os.getenv('ROOT_FOLDER', os.path.expanduser('~/.config/wde'))
CONFIG = None


class Config():
    __slots__ = [
        'ROOT_FOLDER',
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


def get() -> Config:
    global CONFIG
    if CONFIG is None: CONFIG = Config()
    return CONFIG


def load(cfg: Config, root=None) -> Config:
    if root is None: root = ROOT_FOLDER

    if not os.path.exists(root):
        click.echo('Root folder does not exitst. Run `wde install` first.', err=True)
        exit(1)

    cfg.ROOT_FOLDER = root
    cfg.DEV_USER = os.getenv('DEV_USER', 'magnetron')
    cfg.DB_USER = os.getenv('DB_USER', 'magnetron')
    cfg.DB_PASSWORD = os.getenv('DB_PASSWORD', 'magnetron')
    cfg.PHP_VERSION = os.getenv('PHP_VERSION', '7.1')
    cfg.DOMAIN_SUFFIX = os.getenv('DOMAIN_SUFFIX', 'dev')
    cfg.DOMAIN_PATH = os.getenv('DOMAIN_PATH', '7.1')
    cfg.WDE_NAME = f'wde-{cfg.PHP_VERSION}'
    cfg.DB_NAME = 'db'

    global CONFIG
    CONFIG = cfg

    return cfg


def load_env(root):
    env_path = os.path.join(root, '.env')

    if not os.path.exists(env_path):
        click.echo('Env file does not exist. Run `wde install` first.', err=True)
        exit(1)

    load_dotenv(env_path)
