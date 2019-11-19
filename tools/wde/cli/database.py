from wde.cli import *
from wde import container, config
import os

@prelude.group(cls=AliasedGroup)
@click.pass_context
def db(ctx: click.Context):
    """Database commands"""
    db_ip = container.get_ip(config.get().DB_NAME)
    if db_ip is None:
        click.echo('Check if the database is running. Maybe run \'wde up\'', err=True)
        exit(1)
    ctx.obj = db_ip


@db.command('import')
@click.pass_obj
@pass_config
@click.argument('file', default='./import.sql')
def db_import(host: str, cfg: Config, file):
    """Imports given database"""
    initial_file = os.path.abspath(file)
    file = container.translate_path_mounted(file)
    if file is None:
        click.secho(f'File ({initial_file}) is not in a mounted path.', err=True)
        exit(1)

    click.secho(f'Importing file: {file}')
    container.exec(
        cfg.WDE_NAME,
        f"mysql -h {host} -uroot  -e \"GRANT ALL PRIVILEGES ON * . * TO '{cfg.DB_USER}'@'%'\"",
        shell=True, capture=False
    )

    container.exec(
        cfg.WDE_NAME,
        f"mysql -h {host} -u{cfg.DB_USER} -p{cfg.DB_PASSWORD} < {file}",
        shell=True, capture=False
    )
