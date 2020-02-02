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

@click.option('--field', '-f',
                help='Field to be printed out. You can print out one or more fields:\n'
                     'pyhanga list -f <field> -f <field> ...\n'
                     'By default, StackName and StackStatus are printed out.',
                default = tuple([const.STACK_NAME, const.STACK_STATUS]),
                multiple=True,
                type=click.Choice(const.STACK_SUMMARY_FILEDS, case_sensitive=False))
              

@click.option('--match-name', '-m',
                help='Search stacks based on a condition matching their name:\n'
                        'Format: pyhanga -m CHOICE VALUE\n'
                        'VALUE is the string to be searched.\n'
                        'CHOICE is a match condition type that can be contains, startswith, or endswith.\n'
                        'By default, all stack names are searched.',
                default=tuple([const.EXACTLY, const.ALL]),          
                nargs=2, type=click.Tuple([click.Choice(const.STRING_MATCH_CONDITIONS, case_sensitive=False), str]))

@click.option('--match-status', '-s',
                help='Search stacks based on a condition matching their status type\n'
                     'You can search one or more status types can be listed\n:'
                     'pyhanga list -s <type> --s <type> ...\n'
                     'By default, all status types except DELETE_COMPLETE are searched.',  
                default=const.DEFAULT_LSTACKSTATUS_FIELDS,
                multiple=True,
                type=click.Choice(const.STACK_STATUS_FILTERS, case_sensitive=False))


@click.command(name='list')
def list_stacks(field, match_name, match_status):
    """
    List stacks
    """
    _list_stacks(field, match_name, match_status)


def _list_stacks(field, match_name, match_status):
    mn_cond, mn_value = match_name

    try:
        response = _session.cf.list_stacks()
    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)
    # except:
    #     click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
    #     sys.exit(const.ERC_OTHERS)  

    count_results = 0
    json = response[const.STACK_SUMMARIES]
    match_status = util.uppercaseTuple(match_status)

    for response in json:

        stackStatus = str(response[const.STACK_STATUS])
        
        contOuterLoop = True
        for s in match_status:
            if stackStatus != s:
                continue
            else:
                contOuterLoop = False
                break
        
        if contOuterLoop:
            continue

        stackName = response[const.STACK_NAME]
        mn_cond = mn_cond.lower()
         
        if mn_cond == const.EXACTLY and mn_value == const.ALL:
            pass
        elif mn_cond == const.EXACTLY and mn_value != stackName:
            continue
        elif mn_cond == const.CONTAINS and mn_value not in stackName:
            continue
        elif mn_cond == const.STARTS_WITH and not stackName.startswith(mn_value):
            continue
        elif mn_cond == const.ENDS_WITH and not stackName.endswith(mn_value):
            continue  
        
        field = util.recaseTuple(field, const.STACK_SUMMARY_FILEDS)
        iField = iter(field)
        row = response[next(iField)]
        
        for i in iField:
            value = response.get(i)
            col = str(value) if value else const.NULL
            row = row + const.DELIM + col
        click.echo(row)
        count_results += 1
    
    click.secho('\nTotal number of stacks found:', fg=const.FG_INF)
    click.echo(count_results)