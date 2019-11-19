import click
from wde import config


class AliasedGroup(click.Group):
    def invoke(self, ctx):
        return super().invoke(ctx)

    def get_command(self, ctx: click.Context, cmd_name):
        if cmd_name != 'install':
            ctx.ensure_object(config.Config)

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


pass_config = click.make_pass_decorator(config.Config)


@click.group(cls=AliasedGroup)
@click.pass_context
def prelude(ctx):
    ctx.obj = config.get()
    pass
