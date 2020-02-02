__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"


# internal packages
import sys

# 3rd-party packages
import click
import botocore

# custom packages
from . import _session
from . import list_stacks
from . import list_resources
from . import describe_stack
from . import describe_events
from . import describe_resource
from . import create_stack
from . import update_stack
from . import delete_stack
from . import protect_stack
from . import cost_template
from . import upload_object
from . import pyhanga_util as util
from . import pyhanga_constants as const

def _print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('hanga 0.9001')
    ctx.exit()

def _init_profile(ctx, param, value):
    click.echo(value)
    ctx.exit()


@click.group()
@click.option(
    '--version',
    is_flag=True,
    callback=_print_version,
    expose_value=False,
    is_eager=True,
    help='Show pyhanga version'
)

@click.option(
    '--profile', '-p',
    required=True,
    default=const.DEFAULT_PROFILE,
    help='AWS CLI profile'
)

@click.option(
    '--region', '-r',
    help='Working region'
)

def cli(profile, region):
    try:
        _session._init_session(profile, region)  
    except:
        click.secho(const.ERM_PROFILE_NOTFOUND, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_PROFILE_NOTFOUND)


cli.add_command(describe_stack.describe_stack)
cli.add_command(describe_events.describe_events)
cli.add_command(describe_resource.describe_resource)
cli.add_command(list_stacks.list_stacks)
cli.add_command(list_resources.list_resources)
cli.add_command(create_stack.create_stack)
cli.add_command(update_stack.update_stack)
cli.add_command(delete_stack.delete_stack)
cli.add_command(protect_stack.protect_stack)
cli.add_command(cost_template.cost_template)
cli.add_command(upload_object.upload_object)






