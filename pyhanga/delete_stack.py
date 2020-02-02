__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"

import sys
import os
import random
import time

import click
import boto3
import botocore

from . import _session
from . import pyhanga_constants as const
from . import pyhanga_util as util
from .list_resources import _list_resources

@click.option('--name', '-n',
                required=True,
                type=click.STRING,
                help='Stack name')

@click.option('--yes', '-y',
                help='(NOT RECOMMEND!) Proceed the stack update without prompting',
                is_flag=True)  

@click.command(name='delete')
def delete_stack(name, yes):
    """
    Delete a stack
    """    
    try:
        deleteAction = False

        _list_resources(name, 
                        [const.RESOURCE_TYPE, const.LOGICAL_RESOURCE_ID],
                        const.MAX_RESOURCES_STACK)

        if not yes:
            click.secho('WARNING: The above resources of the stack will be deleted and unrecoverable if they are unprotected with RETAIN.', fg=const.FG_WARN)
        
        # If --yes flag is not specified, prompt the confirmation question.
        if not yes: 
            yes = util.query_yes_no('\nDo you want to execute this change set?', 'no')

        if not yes:
            click.secho('You have aborted this change set.', fg=const.FG_INF) 
        else:
            _session.cf.delete_stack(StackName=name)
            deleteAction = True
            eResponse = _wait_for_done_deletion(name)
            if eResponse != const.DELETE_COMPLETE:
                click.secho('The stack was unsuccessfully deleted with this status: %s!' % eResponse, fg=const.FG_ERROR)
            else:
                click.secho('The stack has been deleted!', fg=const.FG_INF)                
    except botocore.exceptions.ClientError as error:
        if deleteAction and str(error.response['Error']['Code']) == 'ValidationError' and str(error.response['Error']['Message']).endswith('does not exist'):
            click.secho('The stack has been deleted!', fg=const.FG_INF)  
        else:
            util.handleClientError(error)

def _wait_for_done_deletion(name):  
    click.secho('Please wait while the stack is being deleted...', fg=const.FG_INF)

    eResponse = const.DELETE_IN_PROGRESS
    response = None   
    running_time = 0
    anim_index = 0
    
    while eResponse == const.DELETE_IN_PROGRESS:

        print(const.ANIM_STRING[anim_index % const.ANIM_LEN], end="\r")   
        
        if running_time % const.DELAY_TIME_FOR_DESCRIBE_CHANGE_SET == 0.0:
            response = _session.cf.describe_stacks(StackName=name) 
            response = response[const.STACKS][0]
            eResponse = response[const.STACK_STATUS]
   
        anim_index += 1
        time.sleep(const.DELAY_TIME_FOR_ANIMATION)
        running_time += const.DELAY_TIME_FOR_ANIMATION

    return eResponse

