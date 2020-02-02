__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"


import sys

import click
import boto3
import botocore

from . import _session
from . import pyhanga_constants as const
from . import pyhanga_util as util
from .describe_stack import _describe_stack

@click.option('--name', '-n',
                required=True,
                help='Stack name\n'
                        'If only this option is used, the command shows the current termination protection status of the stack.')

@click.option('--enable/--disable', '-e/-d',
                help='Enable/disable the termination protection',
                default=None,
                is_flag=True)             

@click.command(name='protect')
def protect_stack(name, enable):
    """
    Enable a stack to be protected from termination 
    """    

    click.secho('Current termination protection status: ', fg='green')  
    status = str(_describe_stack(name, 
            tuple([const.ENABLE_TERMINATION_PROTECTION])))

    if enable is None:
        click.secho(const.INF_NOTHING_TO_CHANGE, fg=const.FG_INF)
    else:  
        senable = str(enable)
        
        if (status in senable):
            click.secho(const.INF_NOTHING_TO_CHANGE, fg=const.FG_INF)
        else:
            try:
                _session.cf.update_termination_protection(StackName=name,
                                                        EnableTerminationProtection=enable)
                click.secho('The new termination protection status:', fg='green')
                click.echo(enable)
            except botocore.exceptions.ClientError as error:
                util.handleClientError(error)
            # except:
            #     click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
            #     sys.exit(const.ERC_OTHERS)      