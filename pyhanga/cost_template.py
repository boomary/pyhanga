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
from .deploy_stack import _formUrl_and_upload

@click.option('--template', '-t',
                help='Stack template',
                type=click.STRING)

@click.option('--bucket', '-b',
                help='S3 bucket',
                required=True)

@click.option('--object-prefix', '-o',
                help='S3 object prefix (i.e., directory)\n'
                        'By default, the prefix is empty (i.e., root the bucket).',
                default='')

@click.option('--params', '--parameters', 
                help='Parameter file',
                default=None)

@click.option('--upload', '-u',
                help='Upload the template file to the bucket prefix',
                default=False,
                is_flag=True)  

@click.command(name='cost')
def cost_template(template, bucket, object_prefix, params, upload):
    """
    Estimate monthly cost of a stack
    """  

    templateUrl = _formUrl_and_upload(template, bucket, object_prefix, upload)
    if params is not None:
        baseName = os.path.basename(params)        
        paramList = util.getJsonDataFromFile(params, baseName)
        click.secho('Use the parameter file: %s' % baseName, fg=const.FG_INF)
    else:
        paramList = list()

    try:
        eResponse = _session.cf.estimate_template_cost(TemplateURL=templateUrl,
                                                        Parameters=paramList)  
        url = eResponse.get(const.URL)
        click.secho('\nThe estimated montly cost can be found at the following URL:', fg=const.FG_INF)              
        click.echo(url)
    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)

