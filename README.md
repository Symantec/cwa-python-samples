# cwa-python-samples
Python code samples for demonstrating usage of Symantec Cloud Workload Assurance (SCWA) RESTful API functions

Refer to Symantec CWA API documentation at: https://apidocs.symantec.com/home/SCWA

Before you get started you need a Symantec Cloud Workload Assurance Account. If you do not have one sign up for a trial account using this link, select the 'Cloud Workload Assurance' check box: https://securitycloud.symantec.com/cc/#/onboard

You can also buy Cloud Workload Assurance from Amazon AWS Market Place that also includes free usage. Click this link: https://aws.amazon.com/marketplace/pp/B07JM2CFK4

After you have activated your account, completed AWS or Azure Connection with periodic sync interval; you are ready to start using these samples.
First step is to Create API access keys. After login to CWA console, go to 'Settings' page and click on 'API Keys' tab

Copy following API secret keys for your CWA tenant ID information and secure them

Customer ID: SEJ*#########################7788

Domain ID: Dq*####################6Yh

Client ID: O***#####################y988

Client Secret Key: t##################################

-----------------------------------------------------------------------------------------------------------------------
Code Files

-----------------------------------------------------------------------------------------------------------------------
cwa_generateAuthToken.py

Script to generate Authentication token which will be be used for subsequent API calls.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_token_based_authentication_service

-----------------------------------------------------------------------------------------------------------------------
cwa_getEvents.py

Script to get events that are generated due to misconfigurations of AWS/Azure resources as per policy or checks.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_get_event_details

-----------------------------------------------------------------------------------------------------------------------
cwa_getListofAccounts.py

Script to get the list of all available AWS and Azure accounts in the cloud infrastructure.
Refer to CWA REST API at https://apidocs.symantec.com/home/sCWA#_getaccounts

-----------------------------------------------------------------------------------------------------------------------
cwa_getListofChecksForResoucres.py

Script to get the list of checks along with the check details for the AWS and Azure resources' id you provide.
Refer to CWA REST API at https://apidocs.symantec.com/home/sCWA#_getchecksforservice

-----------------------------------------------------------------------------------------------------------------------
cwa_getListofPolicies.py

Script to get the list of all the existing policies. This includes policy information such as policy id and policy name.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getpolicies

-----------------------------------------------------------------------------------------------------------------------
cwa_getListofResources.py

Script to get the list of resources for the service id you provide. Following are the services ID that are currently supported by CWA for AWS and Azure:

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

Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getserviceresources

-----------------------------------------------------------------------------------------------------------------------
cwa_getListofScanProfiles.py

Script to get the list of existing scan profiles.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getscanprofiles 

-----------------------------------------------------------------------------------------------------------------------
cwa_getListofServices.py

Script to get the list of available services along with service details such as service name, service id, region, and cloud provider.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_getservices 

-----------------------------------------------------------------------------------------------------------------------
cwa_startScanUsingAccountAndPolicyIDs.py

Script that lets you start a scan immediately for the given policy id and Account ID. The script returns the scan profile id.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_startscan 

-----------------------------------------------------------------------------------------------------------------------
cwa_startScanUsingScanProfileID.py

Script that lets you to start scan using a scan profile id.
Refer to CWA REST API at https://apidocs.symantec.com/home/SCWA#_startscanforprofile 

-----------------------------------------------------------------------------------------------------------------------
