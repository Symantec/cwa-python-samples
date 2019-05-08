#!/usr/bin/env python
#################################################################################################################
# Copyright 2018 Symantec Corporation. All rights reserved.
# Script to get Events
# You need to provide Client ID and Client Secret Key in config.ini file under Credentials sections, to generate
#  auth token.
# These keys can be found on CWA customer portal, once you are logged in navigate to Settings->API Keys
# The config file must be in the same directory as of the script.
# python cwa_associateAccountToOrgUnit.py
# On success, this script will create a child org unit under root org unit.
# You need to provide nsame and decription of org uni tyou want to create on line 68 and 69 respectively.
#################################################################################################################
import json
import requests
import configparser
import os
import logging
from pathlib import Path

# create logger
logger = logging.getLogger("cwa_createChildOrgUnitUnderRootOU")
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

logger.info("cwa_createChildOrgUnity: Current working Directory is " + Current_Working_Dir)
logger.info("cwa_createChildOrgUnit: Checking if config file present in current directory")

config_file = Path(Current_Working_Dir + '/config.ini')

# Checking if config file present
if not config_file.is_file():
    logger.error("cwa_createChildOrgUnit: File config.ini not found in current working directory, place config.ini "
                 "fle in directory \n " + Current_Working_Dir)
    exit()
else:
    logger.info("cwa_createChildOrgUnit: Configfile found in directory " + Current_Working_Dir)

# Creating http request and headers


auth_headers = {}
access_token = None
authurl = None
x_epmp_customer_id = None
x_epmp_domain_id = None
org_unit_name = ""
org_unit_description =""
root_ou_name = "00000000-0000-0000-0000-000000000000"
root_ou_id=None

if not org_unit_name:
    logger.error("Provide a org unit name as value of variable, \"org_unit_name\" "
                 " at line 68 ")
    exit()

if not org_unit_description:
    logger.error("Provide a org unit description as value of variable, \"org_unit_description\" "
                 " at line 69 ")
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

def get_root_ou_id():
    global auth_headers
    global root_ou_id
    auth_headers['Authorization'] = access_token
    auth_headers['x-epmp-customer-id'] = x_epmp_customer_id
    auth_headers['x-epmp-domain-id'] = x_epmp_domain_id
    try:
        logger.info("get_root_ou_id(): Hitting http request to get org unit hierarchy ")
        orgUnit_response = requests.get(orgunit_url, headers=auth_headers)
        if orgUnit_response.status_code == 200:
            logger.info("get_root_ou_id(): got lsit of org units successfully ")
            orgUnit_response_json = json.loads(orgUnit_response.text)
            root_ou_id=orgUnit_response_json["id"]
        else:
            logger.error("get_root_ou_id(): Error occurred while getting org units,"
                         "status code is " + str(orgUnit_response.status_code))
    except Exception as ex:
        logger.error("get_org_units(): Exception occurred while getting org units  " + str(ex))
    return root_ou_id

def create_child_org_unit():
    global auth_headers
    url_to_create_child_ou = orgunit_url + "/" + root_ou_id + "/org_unit"
    duplicate_org_unit_error_message = "Another organizational unit with the same name already exists"
    auth_headers['Authorization'] = access_token
    auth_headers['x-epmp-customer-id'] = x_epmp_customer_id
    auth_headers['x-epmp-domain-id'] = x_epmp_domain_id
    create_child_org_unit.request_body = {

        "name": org_unit_name,
        "desc": org_unit_description
    }
    try:
        logger.info("create_child_org_unit(): Hitting http request to get org unit hierarchy ")
        request_json = json.dumps(create_child_org_unit.request_body)
        orgUnit_response = requests.post(url_to_create_child_ou, data=request_json, headers=auth_headers)
        if orgUnit_response.status_code == 200:
            orgUnit_response_json = json.loads(orgUnit_response.text)
            logger.info("create_child_org_unit(): Org unit  " + org_unit_name + " created successfully and "
                                                                                "id is " + orgUnit_response_json[
                            "id"])
        elif orgUnit_response.status_code == 400:
            orgUnit_error_response_json = json.loads(orgUnit_response.text)
            if duplicate_org_unit_error_message in orgUnit_error_response_json["message"]:
                logger.error("create_child_org_unit(): " + orgUnit_error_response_json["message"])
        else:
            logger.error("get_list_of_accounts(): Error occurred while fetching accounts, status code is " + str(
                orgUnit_response.status_code))
    except Exception as ex:
        logger.error("get_list_of_accounts(): Exception occurred while getting accounts  " + str(ex))


if set_request_headers():
    if get_authentication_token():
        if get_root_ou_id():
            create_child_org_unit()
