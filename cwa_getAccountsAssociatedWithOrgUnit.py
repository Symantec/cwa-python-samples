#!/usr/bin/env python
#################################################################################################################
# Copyright 2019 Symantec Corporation. All rights reserved.
# Script to get Events
# You need to provide Client ID and Client Secret Key in config.ini file under Credentials sections, to generate
#  auth token.
# These keys can be found on CWA customer portal, once you are logged in navigate to Settings->API Keys
# The config file must be in the same directory as of the script.
# python cwa_getAccountsAssociatedWithOrgUnit.py
# On success, this script will delete specified org unit.
# for rest of the request.
# You need to provide a list of comma seperated org units at line 68 
# for example ["ORGUNIT_ID1","ORGUNIT_ID2"]
# Sample output of script will be 
#* Account ACCOUNTID1 associated with org unit BcKKbRAsi9w
#* Account ACCOUNTID2 associated with org unit BcKKbRAsi9w
#################################################################################################################
import json
import requests
import configparser
import os
import logging
from pathlib import Path

# create logger
logger = logging.getLogger("cwa_getAccountsAssociatedWithOrgUnit")
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
ORG_UNIT_URL = 'OrgUnitUrl'

# Getting current working directory
Current_Working_Dir = os.getcwd()

logger.info("cwa_getAccountsAssociatedWithOrgUnit: Current working Directory is " + Current_Working_Dir)
logger.info("cwa_deleteOrgUnit: Checking if config file present in current directory")

config_file = Path(Current_Working_Dir + '/config.ini')

# Checking if config file present
if not config_file.is_file():
    logger.error("cwa_getAccountsAssociatedWithOrgUnit: File config.ini not found in current working directory,"
                 "place config.ini ""fle in directory \n " + Current_Working_Dir)
    exit()
else:
    logger.info("cwa_getAccountsAssociatedWithOrgUnit: Configfile found in directory " + Current_Working_Dir)

# Creating http request and headers


auth_headers = {}
access_token = None
authurl = None
x_epmp_customer_id = None
x_epmp_domain_id = None
org_unit_ids = ["xrIV6PoURw-BcKKbRAsi9w"]

if not org_unit_ids:
    logger.error("Provide org unit ids as value of variable, \"org_unit_id\" "
                 " at line 68 , for example [\"ORGUNIT_ID1\",\"ORGUNIT_ID2\"]")
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
        global orgunit_url
        orgunit_url = config.get(CONFIG_URL_SECTION, ORG_UNIT_URL)
        if client_id == "" or client_secret == "" or authurl == "" or orgunit_url == "":
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


def get_associated_account(orgunit):
    global auth_headers
    if len(orgunit) != 0:
        get_associated_accounts_url = orgunit_url + "/" + orgunit + "/accounts"
        auth_headers['Authorization'] = access_token
        auth_headers['x-epmp-customer-id'] = x_epmp_customer_id
        auth_headers['x-epmp-domain-id'] = x_epmp_domain_id
        try:
            logger.info("get_associated_account(): Hitting http request to get accounts associated with org unit " + orgunit)
            response = requests.get(get_associated_accounts_url, headers=auth_headers)
            response_json = json.loads(response.text)
            if response.status_code == 200:
                records = response_json["results"]
                if records:
                    for record in records:
                       print("* Account "+ record["id"] + " associated with org unit " + orgunit)
                else:
                    logger.info("No accounts are associated with org unit " + orgunit)
            if response.status_code == 404:
                error_message = response_json["statusDetailedMessage"]
                logger.error("Incorrect orgunit id was supplied, " + error_message)
        except Exception as ex:
            logger.error("get_associated_account(): Exception occurred while getting accounts associated with "
                         "ou  " + orgunit + " " + str(ex))
    else:
        logger.error("get_associated_account(): Null or blank org unit id was entered. ")
if set_request_headers():
    if get_authentication_token():
       for orgunit in org_unit_ids:
            get_associated_account(orgunit)
