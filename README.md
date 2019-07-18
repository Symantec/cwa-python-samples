# CWA Python Samples

[![Symantec](https://img.shields.io/badge/tag-symantec-yellow.svg)](https://www.symantec.com/)
[![CWA](https://img.shields.io/badge/tag-cwa-yellow.svg)](https://www.symantec.com/products/cloud-workload-protection)
[![Python](https://img.shields.io/badge/language-python-blue.svg)](https://www.python.org/)
|
[![GitHub contributors](https://img.shields.io/github/contributors/Symantec/cwa-python-samples.svg)](https://GitHub.com/Symantec/cwa-python-samples/graphs/contributors/)
|
[![GitHub issues](https://img.shields.io/github/issues/Symantec/cwa-python-samples.svg)](https://GitHub.com/Symantec/cwa-python-samples/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/Symantec/cwa-python-samples.svg)](https://GitHub.com/Symantec/cwa-python-samples/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/Symantec/cwa-python-samples.svg)](https://GitHub.com/Symantec/cwa-python-samples/pull/)

Python code samples for demonstrating usage of Symantec Cloud Workload Assurance (SCWA) RESTful API functions

-----------------------------------------------------------------------------------------------------------------------

- [CWA Python Samples](#cwa-python-samples)
  - [Postman](#postman)
  - [Setup](#setup)
  - [CHANGELOG](CHANGELOG.md)
  - [License](LICENSE)

**Scripts**

  - [Generate Auth Token](#Generate-Auth-Token)
  - [Add Account In Scan Profile](#Add-Account-In-Scan-Profile)
  - [Associate Account To Org Unit](#Associate-Account-To-Org-Unit)
  - [Create Child Org Unit Under Root OU](#Create-Child-Org-Unit-Under-Root-OU)
  - [Delete Org Unit](#Delete-Org-Unit)
  - [Get Accounts Associated With Org Unit](#Get-Accounts-Associated-With-Org-Unit)
  - [Get Events](#Get-Events)
  - [Get List Of Accounts](#Get-List-Of-Accounts)
  - [Get List Of Checks For Resoucres](#Get-List-Of-Checks-For-Resoucres)
  - [Get List Of Policies](#Get-List-Of-Policies)
  - [Get List Of Resources](#Get-List-Of-Resources)
  - [Get List Of Scan Profiles](#Get-List-Of-Scan-Profiles)
  - [Get List Of Services](#Get-List-Of-Services)
  - [Get Org Unit Hierarchy](#Get-Org-Unit-Hierarchy)
  - [Get Scan Staus Using Scan Profile ID](#Get-Scan-Staus-Using-Scan-Profile-ID)
  - [Start Scan Using Account And Policy IDs](#Start-Scan-Using-Account-And-Policy-IDs)
  - [Start Scan Using Scan ProfileID](#Start-Scan-Using-Scan-ProfileID)

-----------------------------------------------------------------------------------------------------------------------

## Postman

A Postman collection allows you to test the APIs, import this file.

Also create a new environment with the following keys and add your respective values:

`client_id` and `client_secret`.

- [CWA_REST_API_COLLECTION](CWA_REST_API_COLLECTION.postman_collection.json)

-----------------------------------------------------------------------------------------------------------------------

## Setup

Refer to Symantec CWA API documentation at: https://apidocs.symantec.com/home/SCWA

Before you get started you need a Symantec Cloud Workload Assurance Account. If you do not have one sign up for a trial account using this link, select the 'Cloud Workload Assurance' check box: https://securitycloud.symantec.com/cc/#/onboard

You can also buy Cloud Workload Assurance from Amazon AWS Market Place that also includes free usage. Click this link: https://aws.amazon.com/marketplace/pp/B07JM2CFK4

After you have activated your account, completed AWS or Azure Connection with periodic sync interval; you are ready to start using these samples.
First step is to Create API access keys. After login to CWA console, go to 'Settings' page and click on 'API Keys' tab

Copy following API secret keys for your CWA tenant ID information and secure them

`Customer ID: SEJ*#########################7788`

`Domain ID: Dq*####################6Yh`

`Client ID: O***#####################y988`

`Client Secret Key: t##################################`

-----------------------------------------------------------------------------------------------------------------------

**Code Files**

-----------------------------------------------------------------------------------------------------------------------
## Generate Auth Token
[cwa_generateAuthToken.py](cwa_generateAuthToken.py)

Script to generate Authentication token which will be be used for subsequent API calls.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_token_based_authentication_service

Usage: 
> `python cwa_generateAuthToken.py`

Sample:
>  `python cwa_generateAuthToken.py`

-----------------------------------------------------------------------------------------------------------------------
## Add Account In Scan Profile
[cwa_addAccountInScanProfile.py](cwa_addAccountInScanProfile.py)

This API service is used to add accounts in an existing scan profile. Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_addaaccountforprofile

Usage: 
> `python cwa_addAccountInScanProfile.py`

Sample:
>  `python cwa_addAccountInScanProfile.py`

-----------------------------------------------------------------------------------------------------------------------

## Associate Account To Org Unit
[cwa_associateAccountToOrgUnit.py](cwa_associateAccountToOrgUnit.py)

This API service is used to associate accounts to an organization unit. Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_addaaccountforprofile

Usage: 
> `python cwa_associateAccountToOrgUnit.py`

Sample:
>  `python cwa_associateAccountToOrgUnit.py`

-----------------------------------------------------------------------------------------------------------------------

## Create Child Org Unit Under Root OU
[cwa_createChildOrgUnitUnderRootOU.py](cwa_createChildOrgUnitUnderRootOU.py)

This API service is used to create an organization unit. Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_createchildorgunit

Usage: 
> `python cwa_createChildOrgUnitUnderRootOU.py`

Sample:
>  `python cwa_createChildOrgUnitUnderRootOU.py`

-----------------------------------------------------------------------------------------------------------------------

## Delete Org Unit
[cwa_deleteOrgUnit.py](cwa_deleteOrgUnit.py)

*Desc*

Usage: 
> `python cwa_deleteOrgUnit.py`

Sample:
>  `python cwa_deleteOrgUnit.py`

-----------------------------------------------------------------------------------------------------------------------

## Get Accounts Associated With Org Unit
[cwa_getAccountsAssociatedWithOrgUnit.py](cwa_getAccountsAssociatedWithOrgUnit.py)

This API service retrieves a list of accounts associated with an organization unit. Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getassociatedaccounts

Usage: 
> `python cwa_getAccountsAssociatedWithOrgUnit.py`

Sample:
>  `python cwa_getAccountsAssociatedWithOrgUnit.py`

-----------------------------------------------------------------------------------------------------------------------

## Get Events
[cwa_getEvents.py](wa_getEvents.py)

Script to get events that are generated due to misconfigurations of AWS/Azure resources as per policy or checks.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_get_event_details

Usage: 
> `python cwa_getEvents.py`

Sample:
>  `python cwa_getEvents.py`

-----------------------------------------------------------------------------------------------------------------------
## Get List Of Accounts
[cwa_getListofAccounts.py](cwa_getListofAccounts.py)

Script to get the list of all available AWS and Azure accounts in the cloud infrastructure.
Refer to CWA REST API at https://apidocs.symantec.com/home/sCWA#_getaccounts

Usage: 
> `python cwa_getListofAccounts.py`

Sample:
>  `python cwa_getListofAccounts.py`

-----------------------------------------------------------------------------------------------------------------------
## Get List Of Checks For Resoucres
[cwa_getListofChecksForResoucres.py](cwa_getListofChecksForResoucres.py)

Script to get the list of checks along with the check details for the AWS and Azure resources' id you provide.
Refer to CWA REST API at https://apidocs.symantec.com/home/sCWA#_getchecksforservice

Usage: 
> `python cwa_getListofChecksForResoucres.py`

Sample:
>  `python cwa_getListofChecksForResoucres.py`

-----------------------------------------------------------------------------------------------------------------------
## Get List Of Policies
[cwa_getListofPolicies.py](cwa_getListofPolicies.py)

Script to get the list of all the existing policies. This includes policy information such as policy id and policy name.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getpolicies

Usage: 
> `python cwa_getListofPolicies.py`

Sample:
>  `python cwa_getListofPolicies.py`

-----------------------------------------------------------------------------------------------------------------------
## Get List Of Resources
[cwa_getListofResources.py](cwa_getListofResources.py)

Script to get the list of resources for the service id you provide. Following are the services ID that are currently supported by CWA for AWS and Azure:

```
ServiceID:ServiceType:Cloud Provider

1:VPC:AWS
2:IAM Users:AWS
3:IAM Password Policy:AWS
4:VPC Security Groups:AWS
5:Simple Notification Service:AWS
6:CloudWatch:AWS
7:CloudTrail:AWS
8:IAM Encryption Keys:AWS
9:IAM:AWS
10:AWS Config:AWS
11:IAM Policies:AWS
12:S3:AWS
13:EC2 Elastic Block Store:AWS
14:EC2 Load Balancers:AWS
15:IAM and ACM Certificates:AWS
16:RDS:AWS
17:CloudFront:AWS
18:Amazon Redshift:AWS
19:RDS Event subscription:AWS
20:EC2:AWS
21:AMIs:AWS
22:AWS Account Settings:AWS
23:Simple Queue Service:AWS
24:VPC Network ACLs:AWS
25:VPC Subnets:AWS
26:CloudFormation:AWS
27:Virtual Networks:AZURE
28:Virtual Machines:AZURE
29:Subnets:AZURE
30:IAM Roles:AWS
```

Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getserviceresources

Usage: 
> `python cwa_getListofResources.py`

Sample:
>  `python cwa_getListofResources.py`

-----------------------------------------------------------------------------------------------------------------------
## Get List Of Scan Profiles
[cwa_getListofScanProfiles.py](cwa_getListofScanProfiles.py)

Script to get the list of existing scan profiles.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getscanprofiles 

Usage: 
> `python cwa_getListofScanProfiles.py`

Sample:
>  `python cwa_getListofScanProfiles.py`

-----------------------------------------------------------------------------------------------------------------------
## Get List Of Services
[cwa_getListofServices.py](cwa_getListofServices.py)

Script to get the list of available services along with service details such as service name, service id, region, and cloud provider.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getservices 

Usage: 
> `python cwa_getListofServices.py`

Sample:
>  `python cwa_getListofServices.py`

-----------------------------------------------------------------------------------------------------------------------

## Get Org Unit Hierarchy
[cwa_getOrgUnitHierarchy.py](cwa_getOrgUnitHierarchy.py)

This API service retrieves the list of organization units with hierarchical structure. Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getorgunithierarchy

Usage: 
> `python cwa_getOrgUnitHierarchy.py`

Sample:
>  `python cwa_getOrgUnitHierarchy.py`

-----------------------------------------------------------------------------------------------------------------------

## Get Scan Staus Using Scap Profile ID
[cwa_getScanStausUsingScapProfileID.py](cwa_getScanStausUsingScapProfileID.py)

This API service retrieves the status of the job associated to the scan profile ID that you provide. Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getjobstatus

Provide a `SCAN_PROFILE_ID`.

Usage: 
> `python cwa_getScanStausUsingScapProfileID.py -param ??`

Sample:
>  `python cwa_getScanStausUsingScapProfileID.py #`

-----------------------------------------------------------------------------------------------------------------------
## Start Scan Using Account And Policy IDs
[cwa_startScanUsingAccountAndPolicyIDs.py](cwa_startScanUsingAccountAndPolicyIDs.py)

Script that lets you start a scan immediately for the given policy id and Account ID. The script returns the scan profile id.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_startscan 

Usage: 
> `python cwa_startScanUsingAccountAndPolicyIDs.py`

Sample:
>  `python cwa_startScanUsingAccountAndPolicyIDs.py`

-----------------------------------------------------------------------------------------------------------------------
## Start Scan Using Scan ProfileID
[cwa_startScanUsingScanProfileID.py](cwa_startScanUsingScanProfileID.py)

Script that lets you to start scan using a scan profile id.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_startscanforprofile 

Usage: 
> `python cwa_startScanUsingScanProfileID.py`

Sample:
>  `python cwa_startScanUsingScanProfileID.py`

-----------------------------------------------------------------------------------------------------------------------

## Change Log

See [CHANGELOG](CHANGELOG.md).

-----------------------------------------------------------------------------------------------------------------------

## License

See [License](LICENSE).
