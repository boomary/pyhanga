# PyHanga
Custom Python-based CloudFormation Command Line Interface (CLI)

## Introduction
PyHanga is a basic CloudFormation CLI for maintaining AWS CloudFormation stacks. The author of PyHanga developed this CLI to be his personal tool for managing CloudFormation stacks. Before the tool, he used the official AWS CLI. The official one is great enough to manage CloudFormation templates. For the author he needed a simpler and more minimal CLI (in his own view). And, that's the beginning of PyHanga. 

Then, he learned that there is the Click package which can be used to build a better CLI. After the Click package was applied to his custom CLI, he migrated its sourcecode to GitHub and named the tool "Hanga" and later "PyHanga". 

## Prerequisites
- Python 3 
- Boto3
- Click

You need to have a AWS CLI profile (AWS credential and config) for accessing AWS APIs. See https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html for more information about AWS CLI and how a profile can be configured.  

## Give examples

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
  create      Create a new stack
  delete      Delete a stack
  devents     Describe events of a stack
  dresource   Describe a resource of a stack
  dstack      Describe a stack
  list        List stacks
  lresources  List resources of a stack
  protect     Enable a stack to be protected from termination
  update      Create a change set for updating an existing stack and deploy...
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

That's all for this quick tour.

## Author
Sivadon Chaisiri (aka javaboom, boomary)

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
