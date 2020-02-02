__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"


import sys
import os

import click
import boto3
import botocore

from . import _session
from . import pyhanga_constants as const
from . import pyhanga_util as util

@click.option('--bucket', '-b',
                help='S3 bucket',
                required=True,
                type=str)

@click.option('--prefix', '-p',
                help='S3 bucket prefix',
                default='/',
                required=True,
                type=str)

@click.option('--file', '-f',
                help='File to be uploaded',
                required=True,
                type=str)

@click.command(name='upload')
def upload_object(bucket, prefix, file):
    """
    Upload a file to a bucket
    """
    _upload_object(bucket, prefix, file)
 

def _upload_object(bucket, object_key, file):

    try:
        _session.s3.meta.client.upload_file(Filename=file, 
                                            Bucket=bucket, 
                                            Key=object_key)
    except FileNotFoundError:
        click.secho(const.ERM_FILE_NOTFOUND, bg=const.BG_ERROR, fg=const.FG_ERROR)
        sys.exit(const.ERC_FILE_NOTFOUND)   
    except botocore.exceptions.ClientError as error:
        util.handleClientError(error)
    # except:
    #     click.secho(const.ERM_OTHERS, bg=const.BG_ERROR, fg=const.FG_ERROR)
    #     sys.exit(const.ERC_OTHERS)

    return object_key 
