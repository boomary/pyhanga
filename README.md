# pyhanga
Custom Python-based CloudFormation Command Line Interface (CLI)

## Introduction
Pyhanga is a basic CloudFormation CLI for maintaining AWS CloudFormation stacks. The author of Pyhanga developed this CLI to be his personal tool for managing CloudFormation stacks. Before the tool, he used the official AWS CLI. The official one is great enough to manage CloudFormation templates. For the author he needed a simpler and more minimal CLI (in his own view). And, that's the beginning of Pyhanga. 

Then, he learned that there is the Click package which can be used to build a better CLI. After the Click package was applied to his custom CLI, he migrated its sourcecode to GitHub and named the tool "Hanga" and later "Pyhanga". 

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

Pyhanga CLI has the following basic structure:
```
    pyhanga [OPTIONS] [COMMAND] [COMMAND-OPTIONS] ...
```

To see commands and options available 
```
    pyhanga --help
```

The output looks like below:
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



## Author
Sivadon Chaisiri (aka javaboom, boomary)

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
