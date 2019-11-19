from wde.cli import *
from wde.config import Config
from wde import utils, container, constants


@prelude.command()
@pass_config
@click.option('-b', '--build', 'build', default=False, is_flag=True)
def up(cfg: Config, build):
    """Starts the wde environment"""
    cmd = ['docker-compose', 'up', '-d']
    if build: cmd.append('--build')
    utils.command(cmd, cfg.ROOT_FOLDER, capture=False)


@prelude.command()
@pass_config
def down(cfg: Config):
    """Stops the wde environment"""
    utils.command(['docker-compose', 'down'], cfg.ROOT_FOLDER, capture=False)


@prelude.command()
@click.pass_context
def restart(ctx):
    """Restarts the wde environment"""
    ctx.invoke(down)
    ctx.invoke(up)


@prelude.command()
@pass_config
def info(cfg: Config):
    """Shows information about the running containers"""
    info = {
        'WDE Root': cfg.ROOT_FOLDER,
        'Domain folder': cfg.DOMAIN_PATH,
        'Container user': cfg.DEV_USER,
        'PHP Version': cfg.PHP_VERSION,
        'Webserver IP': container.get_ip(cfg.WDE_NAME),
        'Webserver Status': container.get_status(cfg.WDE_NAME),
        'Database IP': container.get_ip(cfg.DB_NAME),
        'Database Status': container.get_status(cfg.DB_NAME),
        'DB Username': cfg.DB_NAME,
        'DB Password': cfg.DB_PASSWORD,
    }

    maxlen = max(map(len, info.keys()))
    for (k, v) in info.items():
        click.echo(click.style(k.ljust(maxlen) + ': ', fg='green') + click.style(str(v), fg='white'))


@prelude.command(context_settings=dict(
    ignore_unknown_options=True,
))
@pass_config
@click.option('-c', default=None)
@click.option('-u', '--user', default=None)
@click.argument('cmd', nargs=-1, type=click.UNPROCESSED)
def exec(cfg: Config, c, user, cmd):
    """Executes given command in the container"""
    if c is not None:
        container.exec(cfg.WDE_NAME, c, user=user, capture=False, shell=True)
    elif len(cmd) > 0:
        container.exec(cfg.WDE_NAME, list(cmd), user=user, capture=False)


@prelude.command()
@click.pass_context
@pass_config
@click.argument('version')
def switchphp(ctx, cfg: Config, version):
    """Changes the containers php version"""
    if version not in constants.AVAILABLE_PHP_VERSIONS:
        click.echo(f'Invalid version. Available options: {",".join(constants.AVAILABLE_PHP_VERSIONS)}')
        exit(1)
    ctx.invoke(down)
    utils.update_ini('PHP_VERSION', version)
    click.secho(f'Updated php version to {version}. Restarting WDE', color='white')
    config.get().PHP_VERSION = version
    os.putenv('PHP_VERSION', version)
    utils.command(['docker-compose', 'up', '--build', '-d'], cfg.ROOT_FOLDER, capture=False)
