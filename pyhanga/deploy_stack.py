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
from . import upload_object

def deploy_stack(name, template, bucket, reuse, object_prefix, params, tags, upload, yes, iam, named_iam, default, isUpdated):

    if not reuse and not default and template is None:
        click.secho('Either --template (-t), or --default (-d), or --reuse (-r) option is required.', bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)   

    if not reuse and bucket is None:
        click.secho('When --template (-t) or --default (-d) option is used, --bucket (-b) option is required.', bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)  

    if not reuse and default and (template is not None or params is not None or tags is not None):
        click.secho('The --default (-d) option cannot be used with template, params, or tags option.', bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)   

    if reuse and (bucket is not None or upload or template is not None):
        click.secho('The --reuse (-r) option cannot be used with --template (-t), --bucket (-b), or --upload (-u) option.', bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_OTHERS)     
    
    if default:
        template = name + const.YAML_EXT
        params = name + '-params' + const.JSON_EXT
        tags = name + '-tags' + const.JSON_EXT    
        click.secho('Use the default file option.', fg=const.FG_INF)

    if not reuse:
        templateUrl = _formUrl_and_upload(template, bucket, object_prefix, upload)

    if params is not None:
        baseName = os.path.basename(params)        
        paramList = util.getJsonDataFromFile(params, baseName)
        click.secho('Use the parameter file: %s' % baseName, fg=const.FG_INF)
    else:
        paramList = list()
         
    if tags is not None:
        baseName = os.path.basename(tags)          
        tagList = util.getJsonDataFromFile(tags, baseName)
        click.secho('Use the tag file: %s' % baseName, fg=const.FG_INF) 
    else:
        tagList = list()           
        
    try:
        cName = name + str(random.randint(100000,999999)) # change set name
        cType = 'UPDATE' if isUpdated else 'CREATE'

        capabilities = []
        if iam:
            capabilities.append(const.CAPABILITY_IAM)
        if named_iam:
            capabilities.append(const.CAPABILITY_NAMED_IAM)

        if not reuse:
            response = _session.cf.create_change_set(StackName=name,
                                                TemplateURL=templateUrl,
                                                Capabilities=capabilities,
                                                Parameters=paramList,
                                                ChangeSetName=cName,
                                                ChangeSetType=cType,
                                                Tags=tagList)
        else:
            response = _session.cf.create_change_set(StackName=name,
                                                UsePreviousTemplate=reuse,
                                                Capabilities=capabilities,
                                                Parameters=paramList,
                                                ChangeSetName=cName,
                                                ChangeSetType=cType,
                                                Tags=tagList)            
        csId = response[const.CHANGESET_ID]
        stackId = response[const.STACK_ID]
        click.secho('\nThe following change set (ARN - name) is being created:', fg=const.FG_INF)                                                
        click.echo('%s - %s' % (csId, cName))                                                     
        click.secho('and deployed to the stack:', fg=const.FG_INF)
        click.echo(stackId)  

        response = _wait_for_created_changeset(name, cName)
        # click.echo(response)
        csExecutionStatus = response[const.CS_EXECUTION_STATUS]

        if csExecutionStatus == const.CS_AVAILABLE:
            click.secho('The change set is ready!', fg=const.FG_INF)

            # TODO: Change set results to be shown for confirmation
            _describe_changeset(name, cName, response)

            # If --yes flag is not specified, prompt the confirmation question.
            if not yes: 
                yes = util.query_yes_no('\nDo you want to execute this change set?', 'no')
            
            if not yes:
                if isUpdated:
                    _session.cf.delete_change_set(StackName=name,
                                                    ChangeSetName=cName)
                else:
                    _session.cf.delete_stack(StackName=name)
                click.secho('You have aborted this change set.', fg=const.FG_INF) 
            else:
                response = _session.cf.execute_change_set(StackName=name,
                                                    ChangeSetName=cName)  
                click.secho('The change set is being deployed.', fg=const.FG_INF)    
                eResponse = _wait_for_executed_changeset(name)  
                if (eResponse in [const.UPDATE_COMPLETE, const.IMPORT_COMPLETE, const.CREATE_COMPLETE]):
                    click.secho('\nThe executed change set was complete.', fg=const.FG_INF)
                else:
                    click.secho('\nThe executed change set got rollback with status: %s' % eResponse, fg=const.FG_ERROR)
        else:
            click.secho('Nothing to be created/updated.', fg=const.FG_INF) 

    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)
    # except:
    #     click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
    #     sys.exit(const.ERC_OTHERS)  


def _describe_changeset(name, cName, response):
    dictChanges = {const.CS_ADD: [],
                    const.CS_REMOVE: [], 
                    const.CS_MODIFY: []}
    click.echo()

    while True:
        changes = response[const.CS_CHANGES]
        for change in changes:
            rChange = change[const.CS_RESOURCE_CHANGE]
            action = rChange[const.CS_ACTION]
            resourceType = rChange[const.RESOURCE_TYPE]
            logicalResourceId = rChange[const.LOGICAL_RESOURCE_ID]
            replacement = rChange.get(const.CS_REPLACEMENT)  
            replacement = replacement if replacement is not None else 'False'
            dictChanges[action].append((resourceType, logicalResourceId, replacement))

        nextToken = response.get(const.NEXT_TOKEN)
        if nextToken is None:
            break
        else:
            response = _session.cf.describe_change_set(StackName=name,
                                                        ChangeSetName=cName,
                                                        NextToken=nextToken) 
    
    # Summary of resources
    lActions = [const.CS_ADD, const.CS_MODIFY, const.CS_REMOVE]
    pActions = ['added', 'modified', 'removed']
    sActions = ['+', '*', '-']
    for i in range(3):
        if len(dictChanges[lActions[i]]) > 0:
            sAction = sActions[i]
            click.secho('The following resources will be %s:' % pActions[i], fg=const.FG_INF) 
            for resource in dictChanges[lActions[i]]:
                resourceType, logicalResourceId, replacement = resource
                if replacement == 'False':
                    click.echo('  %s %s having ID: %s.' % (sAction, resourceType, logicalResourceId))
                elif replacement == 'True':
                    click.echo('  %s %s having ID: %s to be replaced.' % (sAction, resourceType, logicalResourceId))
                else:
                    click.echo('  %s %s having ID: %s to be conditionally replaced.' % (sAction, resourceType, logicalResourceId))


def _formUrl_and_upload(template, bucket, object_prefix, upload):
    object_prefix = util.reformS3Prefix(object_prefix)

    try:
        with open(template, 'r') as fTemplate:
            baseName = os.path.basename(fTemplate.name)
            object_key = object_prefix + baseName
            click.secho('Use the template file: %s' % baseName, fg=const.FG_INF)        
    except FileNotFoundError:
        util.handleFileNotFound(template)
    
    templateUrl = 'https://' + bucket + '.s3.amazonaws.com/' + object_key
    if (upload):
        upload_object._upload_object(bucket, object_key, os.path.abspath(template))
        click.secho('The template has been uploaded to the bucket.', fg=const.FG_INF)
    
    return templateUrl

def _wait_for_created_changeset(name, cName):   
    click.secho('Please wait while the change set is being created...', fg=const.FG_INF)

    eResponse = ''
    response = None   
    running_time = 0
    anim_index = 0
    
    while eResponse not in [const.CS_CREATE_COMPLETE, const.CS_FAILED]:
        print(const.ANIM_STRING[anim_index % const.ANIM_LEN], end="\r")   
        
        if running_time % const.DELAY_TIME_FOR_DESCRIBE_CHANGE_SET == 0.0:
            response = _session.cf.describe_change_set(StackName=name,
                                        ChangeSetName=cName) 
            eResponse = response[const.CS_STATUS]

        anim_index += 1
        time.sleep(const.DELAY_TIME_FOR_ANIMATION)
        running_time += const.DELAY_TIME_FOR_ANIMATION
    return response

def _wait_for_executed_changeset(name):  
    click.secho('Please wait while the change set is being executed...', fg=const.FG_INF)

    eResponse = ''
    response = None   
    running_time = 0
    anim_index = 0
    
    while eResponse not in [const.CREATE_COMPLETE,
                            const.UPDATE_COMPLETE,
                            const.DELETE_COMPLETE,
                            const.UPDATE_ROLLBACK_COMPLETE,
                            const.ROLLBACK_COMPLETE,
                            const.IMPORT_ROLLBACK_COMPLETE,
                            const.IMPORT_COMPLETE]:

        print(const.ANIM_STRING[anim_index % const.ANIM_LEN], end="\r")   
        
        if running_time % const.DELAY_TIME_FOR_DESCRIBE_CHANGE_SET == 0.0:
            response = _session.cf.describe_stacks(StackName=name) 
            response = response[const.STACKS][0]
            eResponse = response[const.STACK_STATUS]
   
        anim_index += 1
        time.sleep(const.DELAY_TIME_FOR_ANIMATION)
        running_time += const.DELAY_TIME_FOR_ANIMATION

    return eResponse

