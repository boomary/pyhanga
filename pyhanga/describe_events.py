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
                     'pyhanga devents -f <field> -f <field> ...\n'
                     'By default, ResourceType, LogicalResourceId, ResourceStatus, and Timestamp are printed out.',
                default = const.DEFAULT_DEVENTS_FIELDS,
                multiple=True,
                type=click.Choice(const.STACK_EVENT_FIELDS, case_sensitive=False))

@click.option('--max-items', '-m',
                help='Maximum number of events to be returned (default: 1)\n',
                default = 1,
                type=int)

@click.command(name='devents')
def describe_events(name, field, max_items):
    """
    Describe events of a stack
    """
    _describe_events(name, field, max_items)

def _describe_events(name, field, max_items):
     nextToken = 'null'
     count_results = 0
     
     while True and count_results < max_items:
          try:
               response = _session.cf.describe_stack_events(StackName=name, NextToken=nextToken)
          except botocore.exceptions.ClientError as error:
               util.handleClientError(error)
          # except:
          #     click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
          #     sys.exit(const.ERC_OTHERS)  
          
          field = util.recaseTuple(field, const.STACK_EVENT_FIELDS)
          
          json = response[const.STACK_EVENTS]

          for event in json:
               if count_results >= max_items:
                    break

               iField = iter(field)
               row = event[next(iField)]

               for i in iField:
                    value = event.get(i)
                    col = str(value) if value else const.NULL
                    row = row + const.DELIM + col 
               count_results += 1
               click.echo(row)

          nextToken = response.get(const.NEXT_TOKEN)
          if nextToken is None:
               break
     
     click.secho('\nTotal number of events returned:', fg=const.FG_INF)
     click.echo(count_results)