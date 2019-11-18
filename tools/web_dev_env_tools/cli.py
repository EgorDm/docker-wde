import os
import subprocess

import click

from web_dev_env_tools import constants, container, utils


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.group(cls=AliasedGroup)
def core():
    constants.load_conf()


@core.command()
@click.pass_context
def install(ctx):
    """Starts the wde environment"""
    click.secho('Installing WDE', color='white')
    ctx.invoke(up, build=True)
    ctx.invoke(down)

    install_script = constants.get_root('scripts/install.sh')
    subprocess.run(
        f'sudo -S bash {install_script}',
        shell=True
    )
    click.secho('Sucessfully installed WDE', color='green')


@core.command()
@click.option('-b', '--build', 'build', default=False, is_flag=True)
def up(build):
    """Starts the wde environment"""
    cmd = ['docker-compose', 'up', '-d']
    if build: cmd.append('--build')
    utils.command(cmd, constants.ROOT_FOLDER, capture=False)


@core.command()
def down():
    """Stops the wde environment"""
    utils.command(['docker-compose', 'down'], constants.ROOT_FOLDER, capture=False)


@core.command()
@click.pass_context
def restart(ctx):
    """Restarts the wde environment"""
    ctx.invoke(down)
    ctx.invoke(up)


@core.command()
def info():
    """Shows information about the running containers"""
    info = {
        'WDE Root': constants.ROOT_FOLDER,
        'Domain folder': constants.DOMAIN_PATH,
        'Container user': constants.DEV_USER,
        'PHP Version': constants.PHP_VERSION,
        'Webserver IP': container.get_ip(constants.WDE_NAME),
        'Webserver Status': container.get_status(constants.WDE_NAME),
        'Database IP': container.get_ip(constants.DB_NAME),
        'Database Status': container.get_status(constants.DB_NAME),
        'DB Username': constants.DB_NAME,
        'DB Password': constants.DB_PASSWORD,
    }

    maxlen = max(map(len, info.keys()))
    for (k, v) in info.items():
        click.echo(click.style(k.ljust(maxlen) + ': ', fg='green') + click.style(str(v), fg='white'))


@core.command(context_settings=dict(
    ignore_unknown_options=True,
))
@click.option('-c', default=None)
@click.option('-u', '--user', default=None)
@click.argument('cmd', nargs=-1, type=click.UNPROCESSED)
def exec(c, user, cmd):
    """Executes given command in the container"""
    if c is not None:
        container.exec(constants.WDE_NAME, c, user=user, capture=False, shell=True)
    elif len(cmd) > 0:
        container.exec(constants.WDE_NAME, list(cmd), user=user, capture=False)


@core.command()
@click.option('-q', '--quiet', 'quiet', default=False, is_flag=True)
@click.argument('domain', default=os.path.basename(os.getcwd()))
def unsecure(quiet, domain):
    """Unecures given domain and removes self signed certificate from trusted"""
    domain = f'{domain}.{constants.DOMAIN_SUFFIX}'
    container.exec(constants.WDE_NAME, ['valet', 'unsecure'], capture=quiet, require_mounted=True)
    utils.command(f'certutil -d sql:$HOME/.pki/nssdb -D -n "{domain}"', shell=True, capture=True)
    utils.command(f'certutil -d $HOME/.mozilla/firefox/*.default -D -n "{domain}"', shell=True, capture=True)


@core.command()
@click.pass_context
@click.option('-q', '--quiet', 'quiet', default=False, is_flag=True)
@click.argument('domain', default=os.path.basename(os.getcwd()))
def secure(ctx, quiet, domain):
    """Secures given domain and adds self signed certificate as trusted"""
    ctx.invoke(unsecure)
    domain = f'{domain}.{constants.DOMAIN_SUFFIX}'

    container.exec(constants.WDE_NAME, ['valet', 'secure'], capture=quiet, require_mounted=True)
    cert_path = constants.get_root(f'storage/valet/certificates/{domain}.crt')
    utils.command(f'certutil -d sql:$HOME/.pki/nssdb -A -t TC -n "{domain}" -i "{cert_path}"', shell=True,
                  capture=quiet)
    utils.command(f'certutil -d $HOME/.mozilla/firefox/*.default -A -t TC -n "{domain}" -i "{cert_path}"', shell=True,
                  capture=quiet)


@core.command()
@click.pass_context
@click.argument('version')
def switchphp(ctx, version):
    """Changes the containers php version"""
    if version not in constants.AVAILABLE_PHP_VERSIONS:
        click.echo(f'Invalid version. Available options: {",".join(constants.AVAILABLE_PHP_VERSIONS)}')
        exit(1)
    ctx.invoke(down)
    utils.update_ini('PHP_VERSION', version)
    click.secho(f'Updated php version to {version}. Restarting WDE', color='white')
    constants.PHP_VERSION = version
    os.putenv('PHP_VERSION', version)
    utils.command(['docker-compose', 'up', '--build', '-d'], constants.ROOT_FOLDER, capture=False)


@core.group(cls=AliasedGroup)
@click.pass_context
def db(ctx):
    """Database commands"""
    db_ip = container.get_ip(constants.DB_NAME)
    if db_ip is None:
        click.echo('Check if the database is running. Maybe run \'wde up\'', err=True)
        exit(1)
    ctx.obj = db_ip


@db.command('import')
@click.pass_obj
@click.argument('file', default='./import.sql')
def db_import(host, file):
    """Imports given database"""
    initial_file = os.path.abspath(file)
    file = container.translate_path_mounted(file)
    if file is None:
        click.secho(f'File ({initial_file}) is not in a mounted path.', err=True)
        exit(1)

    click.secho(f'Importing file: {file}')
    container.exec(
        constants.WDE_NAME,
        f"mysql -h {host} -uroot  -e \"GRANT ALL PRIVILEGES ON * . * TO '{constants.DB_USER}'@'%'\"",
        shell=True, capture=False
    )

    container.exec(
        constants.WDE_NAME,
        f"mysql -h {host} -u{constants.DB_USER} -p{constants.DB_PASSWORD} < {file}",
        shell=True, capture=False
    )


cli = click.CommandCollection(sources=[core])

if __name__ == '__main__':
    cli()
