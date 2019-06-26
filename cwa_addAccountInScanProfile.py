#!/usr/bin/env python
#################################################################################################################
# Copyright 2018 Symantec Corporation. All rights reserved.
# Script to get Events
# You need to provide Client ID and Client Secret Key in config.ini file under Credentials sections, to generate
#  auth token.
# These keys can be found on CWA customer portal, once you are logged in navigate to Settings->API Keys
# The config file must be in the same directory as of the script.
# python cwa_addAccountToScanProfile.py
# On success, this script will produce account ids and their names.
# for rest of the request.
# You need to provide value of "accounts_to_be_associated"  at line 68 for example ["ACCOUNT_ID1","ACCOUNT_ID2"]
# You need to provide value of "scan_profile_name"  at line 69 , with which you want to associate accounts
#################################################################################################################
import json
import requests
import configparser
import os
import logging
from pathlib import Path

# create logger
logger = logging.getLogger("cwa_AddAccountToScanProfile")
logger.setLevel(logging.INFO)

# create console handler (ch) and set level to debug
ch = logging.StreamHandler()

# create formatter
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s",
                              "%Y-%m-%d %H:%M:%S")
# add formatter to console handler
ch.setFormatter(formatter)

# add console handler to logger
logger.addHandler(ch)

# Setting variables from config.ini file
AUTHURL = 'AuthUrl'
CLIENT_ID = 'ClientId'
CLIENT_SECRET = 'ClientSecretKey'
CONFIG_CREDS_SECTION = 'Credentials'
CONFIG_URL_SECTION = 'RequestURL'
ADD_ACCOUNTS_SCANPROFILE = 'AddAccountScanProfile'

# Getting current working directory
Current_Working_Dir = os.getcwd()

logger.info("cwa_associateAccountToOrgUnit: Current working Directory is " + Current_Working_Dir)
logger.info("cwa_associateAccountToOrgUnit: Checking if config file present in current directory")

config_file = Path(Current_Working_Dir + '/config.ini')

# Checking if config file present
if not config_file.is_file():
    logger.error("cwa_associateAccountToOrgUnit: File config.ini not found in current working directory, place config.ini "
                 "fle in directory \n " + Current_Working_Dir)
    exit()
else:
    logger.info("cwa_associateAccountToOrgUnit: Configfile found in directory " + Current_Working_Dir)

# Creating http request and headers

auth_headers = {}
access_token = None
authurl = None
x_epmp_customer_id = None
x_epmp_domain_id = None
accounts_to_be_associated = {
"accountIds" :[]
}
scan_profile_name = "d"

if not scan_profile_name:
    logger.error("Provide a org unit id as value of variable, \"scan_profile_name\" "
                 " at line 71 , with which you want to associate accounts")
    exit()
if  not accounts_to_be_associated['accountIds']:
    logger.error("Provide comma delimited account ids as variable, \"accounts_to_be_associated\" "
                 " at line 70 for example [\"ACCOUNT_ID1\",\"ACCOUNT_ID2\"]")
    exit()

# Defining method to hit http request and to generate auth token


def get_authentication_token():
    token_cust_domain_id = False
    try:
        auth_request_json = json.dumps(set_request_headers.auth_request)
        logger.info("get_authentication_token(): Hitting http request to generate auth token")
        auth_response = requests.post(authurl, data=auth_request_json, headers=auth_headers)
        if auth_response.status_code == 200:
            logger.info("get_authentication_token(): auth token generated successfully, "
                        "http status code is " + str(auth_response.status_code))
            global access_token
            access_token = auth_response.json()['access_token']
            global x_epmp_customer_id
            x_epmp_customer_id = auth_response.json()['x-epmp-customer-id']
            global x_epmp_domain_id
            x_epmp_domain_id = auth_response.json()['x-epmp-domain-id']
            token_cust_domain_id = True
        else:
            logger.error("get_authentication_token(): Failed to generate auth token "
                         "received status code is " + str(auth_response.status_code))

    except Exception as ex:
        logger.error(
            "get_authentication_token(): Exception occurred while hitting http request to generate token" + str(ex))
    return token_cust_domain_id


def set_request_headers():
    set_request_headers.auth_request = {}
    headers_got_set = False
    try:
        logger.info("set_request_headers(): Parsing and reading values from config files")
        config = configparser.ConfigParser()
        config.read(config_file)
        client_id = config.get(CONFIG_CREDS_SECTION, CLIENT_ID)
        client_secret = config.get(CONFIG_CREDS_SECTION, CLIENT_SECRET)
        global authurl
        authurl = config.get(CONFIG_URL_SECTION, AUTHURL)
        global scanprofile_url
        scanprofile_url = config.get(CONFIG_URL_SECTION, ADD_ACCOUNTS_SCANPROFILE)
        if client_id == "" or client_secret == "" or authurl == "" or scanprofile_url == "":
            logger.error("set_request_headers(): One or more values empty in config_file")
            return headers_got_set
        else:
            set_request_headers.auth_request['client_id'] = client_id
            set_request_headers.auth_request['client_secret'] = client_secret
            auth_headers['Content-type'] = 'application/json'
            headers_got_set = True

    except Exception as ex:
        logger.error("set_request_headers(): Exception occurred while reading values from config file " + str(ex))
    return headers_got_set


def associate_accounts_to_scan_profile():
    global auth_headers
    url_to_create_child_ou = scanprofile_url + "/" + scan_profile_name + "/accounts"
    auth_headers['Authorization'] = access_token
    auth_headers['x-epmp-customer-id'] = x_epmp_customer_id
    auth_headers['x-epmp-domain-id'] = x_epmp_domain_id
    try:
        logger.info("associate_accounts_to_scan_profile(): Hitting http request to add scan profile")
        request_json = json.dumps(accounts_to_be_associated)
        scanProfile_response = requests.put(url_to_create_child_ou, data=request_json, headers=auth_headers)
        scanProfile_response_status= scanProfile_response.status_code
        if scanProfile_response_status != 200:
            response_json = json.loads(scanProfile_response.text)
            errorMessage= response_json['statusDetailedMessage']
            print(errorMessage)
        else:
            print("Account " + str(accounts_to_be_associated) + " successfully added to scan profile");
    except Exception as ex:
        logger.error("associate_accounts_to_scan_profile(): Exception occurred while associating account " + str(ex))


if set_request_headers():
    if get_authentication_token():
        associate_accounts_to_scan_profile()
