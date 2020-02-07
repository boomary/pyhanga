# PyHanga
Custom Python-based CloudFormation Command Line Interface (CLI)

## Introduction

PyHanga is a basic CloudFormation CLI for maintaining AWS CloudFormation stacks. 

I, as the author of PyHanga, first developed this CLI just to be my personal tool for managing CloudFormation stacks. I used AWS Management Console (the web UI) and the official AWS CLI tool a lot before starting to script PyHanga. 

AWS Management Console is cool. But it is somehow a pain when you want to rerun a CloudFormation template multiple times with updated code, tags, or parameters. 

The official AWS CLI is great enough to manage CloudFormation stacks. It does have a CloudFormation command like the *deploy* command which meets my basic requirements. So what? I just want to have fun by creating another custom CLI with options that I will be familiar with. Hence, I first created a large python script for my own greed. 

Later, I learned that there is the Click package which can be used to build a better CLI. After the Click package was applied to my custom CLI, I migrated PyHanga sourcecode to GitHub and named the tool "Hanga" and later "PyHanga". 

## Prerequisites

PyHanga is coded with Python 3 and it uses Boto3 and Click packages. You shall check the *setup.py* file in this repo to see any additional required packages to be added in future.

You should know CloudFormation. If you want to learn about CloudFormation, you have good [documentation from AWS](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) to start with.

Befoer using PyHanga, you must have an AWS CLI profile ready for accessing AWS APIs. See https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html for more information about AWS CLI and how a profile (including credentials and config files) can be configured.  

## How to install

Just run the pip command:

```
    pip install pyhanga
```

Or the following one for installing Pyhanga into the user directory. 

```
    pip install pyhanga --user
```

And use the following --upgrade for upgrading the package.

```
    pip install pyhanga --user --upgrade
```

## Quick Tour

PyHanga CLI has the following basic structure:
```
    pyhanga [OPTIONS] [COMMAND] [COMMAND-OPTIONS] ...
```

To see commands and options available 
```
    pyhanga --help
```

Here is the output of the above command:
```
Usage: pyhanga [OPTIONS] COMMAND [ARGS]...

Options:
  --version           Show pyhanga version
  -p, --profile TEXT  AWS CLI profile  [required]
  -r, --region TEXT   Working region
  --help              Show this message and exit.

Commands:
  cost        Estimate monthly cost of a stack
  create      Create a new stack with a change set
  delete      Delete a stack
  devents     Describe events of a stack
  dresource   Describe a resource of a stack
  dstack      Describe a stack
  list        List stacks
  lresources  List resources of a stack
  protect     Enable a stack to be protected from termination
  update      Update an existing stack with a change set
  upload      Upload a file to a bucket
```

You see that there are several useful commands for managing CloudFormation stacks, e.g., *create*, *update*, and *delete* commands for creating, updating, and deleting a stack, respectively.

Aah ... **do not forget that** before you execute any PyHanga command, you need a valid AWS CLI profile ready. You can specify a profile with -p (--profile) option right after the *pyhanga* main command. Say, you have a profile called *devprofile*. Then, you can use this profile like this:

```
    pyhanga -p devprofile ...
```

Ahem, don't type '...' and enter. You won't get anything useful. It's just an example. Instead of typing '...', you specify a PyHanga command and its options. 

If you don't specify a profile, it implies that you use the default profile (e.g., the[default] profile usually specified in /.aws/credentials). 

As you know, AWS manages resources accross AWS Regions. You should specifiy the AWS Region that you want to manage CloudFormation with the -r (--region) option. The option requires a valid AWS Region code (e.g., ap-southeast-2 for Sydney and us-east-1 for North Virginia). This following link would be helpful for you: https://docs.aws.amazon.com/general/latest/gr/rande.html  

Let's say you want to manage a CloudFormation stack with *devprofile* profile in Tokyo region (i.e., ap-northeast-1). You specify the -p and -r options together as follows:

```
    pyhanga -p devprofile -r ap-northeast-1 ...
```

If you don't specify the region, the default region configured for your active profile is used (e.g., usually the region configured in /.aws/config).

Now let's review how a command is invoked.


Each PyHanga command provides basic help information, for example,
```
    pyhanga lresources --help
```

And the output looks like this:
```
Usage: pyhanga lresources [OPTIONS]

  List resources of a stack

Options:
  -m, --max-items INTEGER         Maximum number of resources to be returned
                                  (default: 200)
  -f, --field [ResourceType|LogicalResourceId|PhysicalResourceId|LastUpdatedTimestamp|ResourceStatus|ResourceStatusReason|DriftInformation]
                                  Field to be printed out. You can print out
                                  one or more fields:
                                  pyhanga dresources -f
                                  <field> -f <field> ...
                                  By default,
                                  ResourceType, LogicalResourceId,
                                  ResourceStatus, and Timestamp are printed
                                  out.
  -n, --name TEXT                 Stack name  [required]
  --help                          Show this message and exit.
```


Based on the above help info, you must specify all options with **[required]**. For the *list* command, there is only one required option, i.e., -n (or --name). Let's play with this option.

```
    pyhanga lresources -n mystack
```

Then, the command will return resources managed by the given stack name. 

Some option can be specified more than once. For exampole, the *list* command has the -f (or --field) option. Let's see how we can display only LogicalResourceId and then ResourceStatus of each stack. 

```
    pyhanga lresources -n mystack -f logicalresourceid -f ResourceStatus
```

See? ... the *field* option does not require a case-sensitive value. 

An option of some command allows to provide a pair of values. This command is *list* and the option is -m (--match-name). You can use this *list* command to search for stack names. For example, you want to find stacks containing "server" keyword in their name. You shall execute the following command:

```
    pyhanga list -m contains server
```

In addition to *contains*, you can use *startswith* or *endswith* for searching for stack names starting with or ending with a specified keyword. 

If you want to find stacks containing "server" in their names with UPDATE_ROLLBACK_COMPLETE or UPDATE_COMPLETE status, you shall add --match-status (-s) option and run the following command: 

```
    pyhanga list -m contains server -s update_rollback_complete -s update_complete
```

Next, let's create a stack. Say, we have a YAML CloudFormation template file, named mystack.yaml. We also have JSON files for paramterizing and tagging the stack, named mystack-params.json and mystack-tags.json. And, we will upload the template to an S3 bucket, named pyhanga-bucket-1234 (keep in mind the bucket name must be globally unique). A PyHanga command for creating this CloudFormation stack given the files is like this:

```
    pyhanga create -n mystack -t mystack.yaml -u -b pyhanga-bucket-1234 --params mystack-params.json --tags mystack-tags.json
```

The options used in the above command instructs PyHanga to "create a stack with name (-n) *mystack* using parameters (--params) from *mystack-params.json*, tags (--tags) from *mystack-tags.json*, and template file (-t) *mystack.yaml* that will be uploaded (-u) to the S3 bucket *pyhanga-bucket-1234*". If you prefer a less complicated command, you shall run the following one:

```
    pyhanga create -n mystack -b pyhanga-bucket-1234 -u -d
```

With -d (--default), you tell PyHanga that you want to use default file names. Default files are known by PyHanga that the template file, parameter file, and tage file are named {stackname}.yaml, {stackname}-params.json, and {stackname}-tags.json, respectively. And in our example, the stack name is *mystack* and we prepare all files meeting the default file names.

That's all for this quick tour.

## Author
Sivadon Chaisiri (aka javaboom, boomary)

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
