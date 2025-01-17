# Cloud Tools

## Cloud Stack Template for Galahad

`galahadStack.template.yaml`

This yaml file defines the entire infrastructure for the Galahad VirtUE solution.
Use it at the console [here](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks)
or via the python aws cli.

This script should be updated as needed to include all desired starting state 
for the Galahad VirtUE solution.  It is intended to serve the majority of setup
and configuration needs for T&E and can be cloned with the specific alterations
for the T&E environment.  Leaving this original as an easy standup script for 
additional instances of the environment.

It supports a couple parameters described inline.  Of note are:
* **NameSuffix:** A simple suffix added to Virtue- for most labels of resources
to make it easy to search visually and to filter on.
* **KeyName:** The ssh key to be used for all the assets.

### Known Issues

With no fault in the design, this template has circular references between 
security groups.  AWS Cloudformation tries to strictly order creation steps by
 constructing a dependency tree.  References between entities ('!Ref' or 'Ref:'
) create such dependencies.

This will cause failures to delete the entire stack in one go from the 
aws console or python aws cli.  In general, it will throw an error that there
 are circular references and will list the components that canot be deleted. 
You need to manually remove the circular references then you will be able to 
delete the involved components.

Specifically with this script, you will have to manually prune the sec group
ingress/inbound and egress/outbound rules from the sec groups that reference
each other before you can delete the groups.  It is not known why AWS doesn't 
handle this correctly by identifying that all involved entities are to be 
deleted at the same time.

## Credential retriever

`aws_get_mfa.sh newprofilename <srcprofile>`

This script is an informal tool to generate temporary credentials for MFA 
enabled accounts, and will likely make a dev's life much easier.   

The temporary accounts can be used on the aws python cli with 
`<regular aws command> --profile=<profilename>`

It also helpfully generates a boto configuration file so that you can generate
credentials for services like excalibur while testing.  A better solution like
boto3 with automatic instance-profile credential retrieval should be used for
 the real system.

### To Use
* It is ideal to create the original account info with `aws configure` after
 installing the aws python cli.  
* Then you must edit the `.aws/credentials` file, specifically the profile
for the account you want to use to generate temporary mfa credentials, to 
include a line like `mfa_serial = arn:aws:iam::<AWS_ID>:mfa/kyle` 
including the arn of the mfa device.  You can find this arn in the 'security 
credentials' page of the IAM service on AWS (E.G. https://console.aws.amazon.com/iam/home?region=us-east-1#/users/username?section=security_credentials).
* Then run `aws_get_mfa.sh newprofilename <srcprofile>`.  If you don't provide
 srcprofile, then it will use the default.  If you do provide it then it will
 use the configured information for that profile.  Only REAL, non-temporary
accounts should be used as the srcprofile.

## AWS IAM Policies
In this directory are also policy artifacts that we are using in our dev 
testbed and that should serve as the origins for production policies.

* VirtueTester-Policy.json
  * This Policy is for the dev environment and is hardcoded to restrict actions
to a certain subnet via using a Role.  It was originally harvested from an AWS 
example and heavily modified to suit our needs specifically in our test 
environment.
* Excalibur-Service-Policy.json
  * This Policy is for the excalibur server service.  It is setup to allow 
mostly EC2 simple actions for starting and stopping new machines.  The 
intention is to have it only be allowed to start/stop **Virtues** and any
other tasks it takes on during the project.  It should be modified to suit the
 exact minimum permissions it needs to do it's job.

  * It is currently used, in combination with an instance-profile/Role to allow our
boto3 codebase to automatically obtain credentials and perform actions without
explicit configuration in our codebase or pre-placed credentials

## Debugging AWS Authorization Errors
When someone gets an error at the AWS Python CLI or AWS Web Console it will look of the form:

`A client error (UnauthorizedOperation) occurred: You are not authorized to perform this operation. Encoded authorization failure message: "EjE8j1AEXAMPLEDOwukwv5KbOS2j0jiZTslESOmbSFnqY91ElGRRQpIweQ5CQDQmaS7DBMfJDqwpZAmORTOKHgeNZdcChNCDacLE6YGEAlVyTI8yoc8Ukcb8A8q4i3ap4D0XlG4A5Izf4HGJ6VHoOYPExvwVcDyC7y8C6nDKiQxgM8nJDaxELFcgjOa4RxfsDcpPe5mONAhMc6uxV00HLV5c_dpA6Q6IJR..."`

In order to debug the problem you will need:
* Rights to the sts AWS service (by being admin you OBE this requirement)
* Access to the IAM policies managing [them](https://console.aws.amazon.com/iam/home?region=us-east-1#/policies)
* The encoded error message gobbledy-gook above
* Ideally a helper bash script like aws_decode_error.sh located adjacent to this file.

Run `aws_decode_error.sh <encoded_error_message>`.  It will spit out a pretty printed json file or the problem.  You will still need to parse the results.

If the `'explicitDeny'` field is `true`, then some part of your policy explicitly denied the action for whatever reason and you should look at `'matchedStatements'` to find out why you explicitly denied it and modify the statements or policy as desired. If `'explicitDeny'` is `false`, then you should add appropriately locked down permissions for the action held in the `'action'` field and with conditional statements that are appropriately secure based on your decision.  Existing examples of statements can be found in the policy files adjacent to this README.
