__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"


import sys
import json

import click

from . import pyhanga_constants as const
from botocore.exceptions import ClientError

def recaseTuple(torigin, ldesire):
    mUpperDesire = map(lambda x:x.upper(), ldesire)
    lUpperDesire = list(mUpperDesire)
    lorigin = list(torigin)
    for i in range(len(lorigin)):
        lorigin[i] = ldesire[lUpperDesire.index(lorigin[i].upper())]
    
    return tuple(lorigin)

def uppercaseTuple(torigin):
    mUpperOrigin = map(lambda x:x.upper(), torigin)
    return tuple(mUpperOrigin)

def reformS3Prefix(prefix):
    if prefix == '/':
        prefix = ''
    
    if prefix.startswith('/'):
        prefix = prefix[1:]
    
    if not prefix.endswith('/') and prefix != '':
        prefix = prefix + '/'
    
    return prefix


def getJsonDataFromFile(sJson, baseName):
    try:
        with open(sJson, 'r') as fJson:
            text = fJson.read()
            jsonData = json.loads(text)  
    except FileNotFoundError:
        handleFileNotFound(sJson)
    except json.decoder.JSONDecodeError: 
        click.secho(const.ERM_JSON_INVALID % baseName, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_FILE_NOTFOUND)    
    return jsonData                 

def handleFileNotFound(file):
        click.secho('%s: %s' % (const.ERM_FILE_NOTFOUND, file), bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_FILE_NOTFOUND)    

def handleClientError(error):
    errorCode = str(error.response['Error']['Code'])
    errorMessage = str(error.response['Error']['Message'])
    showMessage = ''
    exitCode = 100
    
    if errorCode == 'ValidationError' and errorMessage.endswith('does not exist'):
        showMessage = 'The stack does not exist.'
    elif errorCode == 'ValidationError' and errorMessage.endswith('TerminationProtection is enabled'):
        showMessage = 'This stack cannot be deleted because it is protected with TerminationProtection.'
    elif errorCode == 'InsufficientCapabilitiesException' and errorMessage.endswith('[CAPABILITY_IAM]'):
        showMessage = 'This stack requires [CAPABILITY_IAM]. Specify --iam option to enable [CAPABILITY_IAM].'
    elif errorCode == 'InsufficientCapabilitiesException' and errorMessage.endswith('[CAPABILITY_NAMED_IAM]'):
        showMessage = 'This stack requires [CAPABILITY_NAMED_IAM]. Specify --iam option to enable [CAPABILITY_NAMED_IAM].'
    else:
        showMessage = error.response['Error']['Code'] + ' ' + error.response['Error']['Message'] 
                                
    click.secho('%s' % showMessage, bg=const.BG_ERROR, fg=const.FG_ERROR)   
    sys.exit(exitCode)


# Credit: http://code.activestate.com/recipes/577058/
def query_yes_no(question, default="no"):
    valid = {"yes": True, "y": True, "yes": True,
             "no": False, "n": False}
    if default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write('Please respond with \'yes\' or \'no\'\n')



