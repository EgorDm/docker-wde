import click

from wde.cli import prelude

cli = click.CommandCollection(sources=[prelude])

if __name__ == '__main__':
    cli()
