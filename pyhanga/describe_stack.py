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

@click.option('--name', '-n',
                required=True,
                help='Stack name')

@click.option('--field', '-f',
                help='Field to be printed out. You can print out one or more fields:\n'
                     'pyhanga dstack -f <field> -f <field> ...\n'
                     'By default, StackName, Description, StackStatus, CreateionTime, and EnableTerrminationProtection are printed out.',
                default = const.DEFAULT_DSTACK_FIELDS,
                multiple=True,
                type=click.Choice(const.STACK_DETAIL_FILEDS, case_sensitive=False))

@click.command(name='dstack')
def describe_stack(name, field):
    """
    Describe a stack
    """
    _describe_stack(name, field)

def _describe_stack(name, field = const.DEFAULT_DSTACK_FIELDS):
    try:
        response = _session.cf.describe_stacks(StackName=name)
    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)
    # except:
    #     click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
    #     sys.exit(const.ERC_OTHERS)  

    response = response[const.STACKS][0]

    field = util.recaseTuple(field, const.STACK_DETAIL_FILEDS)
    iField = iter(field)
    row = response[next(iField)]

    for i in iField:
        value = response.get(i)
        col = str(value) if value else const.NULL
        row = row + const.DELIM + col
    click.echo(row)
    return row 
    