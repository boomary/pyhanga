__author__ = "Sivadon Chaisiri"
__copyright__ = "Copyright (c) 2020 Sivadon Chaisiri"
__license__ = "MIT License"

import click

from . import deploy_stack

@click.option('--name', '-n',
                required=True,
                type=click.STRING,
                help='Stack name')

@click.option('--template', '-t',
                help='Stack template',
                type=click.STRING)

@click.option('--bucket', '-b',
                help='S3 bucket')

@click.option('--reuse', '-r',
                help='Use the previous template associated with the stack',
                is_flag=True)

@click.option('--object-prefix', '-o',
                help='S3 object prefix (i.e., directory)\n'
                        'By default, the prefix is empty (i.e., root the bucket).',
                default='')

@click.option('--params', '--parameters', 
                help='Parameter file',
                default=None)

@click.option('--tags',
                help='Tag file',
                default=None)               

@click.option('--upload', '-u',
                help='Upload the template file to the bucket prefix',
                default=False,
                is_flag=True)  

@click.option('--yes', '-y',
                help='(NOT RECOMMEND!) Proceed the stack update without prompting',
                is_flag=True)  

@click.option('--iam',
                help='Enable CAPABILITY_IAM',
                default=False,
                is_flag=True)  

@click.option('--named-iam',
                help='Enable CAPABILITY_NAMED_IAM',
                default=False,
                is_flag=True)  

# @click.option('--auto-expand',
#                 help='Enable CAPABILITY_AUTO_EXPAND',
#                 default=False,
#                 is_flag=True)  

@click.option('--default', '-d',
                help='Default files to be deployed, that is,\n'
                     '  {stack name}.yaml - Template file\n'
                     '  {stack name}-params.json - parameter file\n'
                     '  {stack name}-tags.json - tag file.\n',
                default=False,
                is_flag=True)                                   

@click.command(name='update')
def update_stack(name, template, bucket, reuse, object_prefix, params, tags, upload, yes, iam, named_iam, default):
    """
    Update an existing stack with a change set
    """
    deploy_stack.deploy_stack(name, template, bucket, reuse, object_prefix, params, tags, upload, yes, iam, named_iam, default, True)    