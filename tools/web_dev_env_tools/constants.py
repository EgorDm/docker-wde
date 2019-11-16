import os
from dotenv import load_dotenv
import click

ROOT_FOLDER = os.getenv('ROOT_FOLDER', '.')


def load_conf():
    env_path = f'{ROOT_FOLDER}/.env'
    if not os.path.exists(env_path):
        click.echo('Could not find .env file. Check if env var "ROOT_FOLDER" is pointing to the correct dir', err=True)
        exit(1)

    load_dotenv(env_path)


load_conf()

DEV_USER = os.getenv('DEV_USER', 'magnetron')
DB_USER = os.getenv('DB_USER', 'magnetron')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'magnetron')
PHP_VERSION = os.getenv('PHP_VERSION', '7.1')
DOMAIN_SUFFIX = os.getenv('DOMAIN_SUFFIX', 'dev')
DOMAIN_PATH = os.getenv('DOMAIN_PATH', '7.1')

WDE_NAME = f'wde-{PHP_VERSION}'
DB_NAME = 'db'

AVAILABLE_PHP_VERSIONS = ['5.6', '7.0', '7.1', '7.2', '7.3']


def get_root(subdir=None) -> str:
    ret = os.path.abspath(ROOT_FOLDER)
    if subdir is not None: ret = os.path.join(ret, subdir)
    return ret


def get_storage() -> str:
    return get_root('storage')
