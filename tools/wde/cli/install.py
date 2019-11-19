from wde.cli import *
from wde import config, utils
import os, subprocess


@prelude.command()
@click.pass_context
def install(ctx):
    """Starts the wde environment"""
    utils.cmd_expect(
        f'docker info',
        'Check if docker is installed, the service is running and you have permissions to run the docker command.'
    )

    click.secho('Installing WDE', color='white')
    if not os.path.exists(config.ROOT_FOLDER):
        click.echo(f'Cloning wde into {config.ROOT_FOLDER}')
        utils.cmd_expect(
            f'git clone https://github.com/EgorDm/docker-wde.git {config.ROOT_FOLDER}',
            'Failed cloning wde',
            hide_output=False
        )

        utils.cmd_expect(
            ['cp', '.env.example', '.env'],
            'Failed updating .env file',
            cwd=config.ROOT_FOLDER
        )

        utils.update_ini(
            'DOMAIN_PATH',
            click.prompt('Enter path for your domains folder', default=os.path.expanduser('~/domains'))
        )

    ctx.ensure_object(config.Config)
    ctx.invoke(up, build=True)
    ctx.invoke(down)

    install_script = config.get().get_root('scripts/install.sh')
    subprocess.run(
        f'sudo -S bash {install_script}',
        shell=True
    )
    click.secho('Sucessfully installed WDE', color='green')
