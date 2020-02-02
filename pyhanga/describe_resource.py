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

@click.option('--lid', '-l',
                required=True,
                help='Logical resource ID')

@click.option('--field', '-f',
                help='Field to be printed out. You can print out one or more fields:\n'
                     'pyhanga dresource -f <field> -f <field> ...\n'
                     'By default, ResourceType, LogicalResourceId, ResourceStatus, and Timestamp are printed out.',
                default = const.DEFAULT_RESOURCE_FIELDS,
                multiple=True,
                type=click.Choice(const.STACK_RESOURCE_FILEDS, case_sensitive=False))


@click.command(name='dresource')
def describe_resource(name, lid, field):
    """
    Describe a resource of a stack
    """
    _describe_resource(name, lid, field)

def _describe_resource(name, lid, field):
     try:
          response = _session.cf.describe_stack_resource(StackName=name, 
                                                            LogicalResourceId=lid)
     except botocore.exceptions.ClientError as error:
          util.handleClientError(error)
     # except:
     #     click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
     #     sys.exit(const.ERC_OTHERS)  
          
     field = util.recaseTuple(field, const.STACK_RESOURCE_FILEDS)
     
     resource = response[const.STACK_RESOURCE_DETAIL]
     iField = iter(field)
     row = resource[next(iField)]

     for i in iField:
          value = resource.get(i)
          col = str(value) if value else const.NULL
          row = row + const.DELIM + col 
     click.echo(row)
