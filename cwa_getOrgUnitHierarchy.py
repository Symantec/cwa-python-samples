#!/usr/bin/env python
#################################################################################################################
# Copyright 2019 Symantec Corporation. All rights reserved.
# Script to get Events
# You need to provide Client ID and Client Secret Key in config.ini file under Credentials sections, to generate
#  auth token.
# These keys can be found on CWA customer portal, once you are logged in navigate to Settings->API Keys
# The config file must be in the same directory as of the script.
# python cwa_getOrgUnitHierarchy.py
# On success, this script gives org units of account ids and their names.
# for rest of the request.
# Sample output of the script will be:- 
#root org unit id is BcKKbRAsi9w
#
#* Org unit BcKKbRAsi9w have following child/children ou associated with it 
#	1.) Org Unit name:->OU1NAME  Org Unit id:->pisKsXtuqA
#	2.) Org Unit name:->OU2NAME  Org Unit id:->TpmJpZK57g
#	3.) Org Unit name:->OU3NAME Org Unit id:->0Y59ZbCQ
#
#* Org unit pisKsXtuqA have following child/children ou associated with it 
#	1.) Org Unit name:->CHILD1NAME Org Unit id:->VDUq4JuNQ
#
#################################################################################################################
import json
import requests
import configparser
import os
import logging
from pathlib import Path

# create logger
logger = logging.getLogger("cwa_getOrgUnitHierarchy")
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

logger.info("cwa_getOrgUnitHierarchy: Current working Directory is " + Current_Working_Dir)
logger.info("cwa_getOrgUnitHierarchy: Checking if config file present in current directory")

config_file = Path(Current_Working_Dir + '/config.ini')

# Checking if config file present
if not config_file.is_file():
    logger.error("cwa_getListofAccounts: File config.ini not found in current working directory, place config.ini "
                 "fle in directory \n " + Current_Working_Dir)
    exit()
else:
    logger.info("cwa_getListofAccounts: Configfile found in directory " + Current_Working_Dir)

# Creating http request and headers


auth_headers = {}
access_token = None
authurl = None
x_epmp_customer_id = None
x_epmp_domain_id = None
dict_parent_child = {}


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
        logger.info("generateAuthToken: Parsing and reading values from config files")
        config = configparser.ConfigParser()
        config.read(config_file)
        client_id = config.get(CONFIG_CREDS_SECTION, CLIENT_ID)
        client_secret = config.get(CONFIG_CREDS_SECTION, CLIENT_SECRET)
        global authurl
        authurl = config.get(CONFIG_URL_SECTION, AUTHURL)
        global orgunit_url
        orgunit_url = config.get(CONFIG_URL_SECTION, ORG_UNIT_URL)
        if client_id == "" or client_secret == "" or authurl == "" or orgunit_url == "":
            logger.error("generateAuthToken: One or more values empty in config_file")
            return headers_got_set
        else:
            set_request_headers.auth_request['client_id'] = client_id
            set_request_headers.auth_request['client_secret'] = client_secret
            auth_headers['Content-type'] = 'application/json'
            headers_got_set = True

    except Exception as ex:
        logger.error("generateAuthToken: Exception occurred while reading values from config file " + str(ex))
    return headers_got_set


def get_org_units():
    global auth_headers
    auth_headers['Authorization'] = access_token
    auth_headers['x-epmp-customer-id'] = x_epmp_customer_id
    auth_headers['x-epmp-domain-id'] = x_epmp_domain_id
    org_units_collected = True
    try:
        logger.info("get_org_units(): Hitting http request to get org unit hierarchy ")
        orgUnit_response = requests.get(orgunit_url, headers=auth_headers)
        if orgUnit_response.status_code == 200:
            logger.info("get_org_units(): got org units successfully ")
            orgUnit_response_json = json.loads(orgUnit_response.text)
            print("root org unit id is " + orgUnit_response_json["id"])
            iterate_child(orgUnit_response_json)
        else:
            logger.error("get_org_units(): Error occurred while getting org units,"
                         "status code is " + str(orgUnit_response.status_code))
    except Exception as ex:
        org_units_collected = False
        logger.error("get_org_units(): Exception occurred while getting org units  " + str(ex))
    return org_units_collected

def iterate_child(orgUnit_response_json):

    i = 0
    length = len(orgUnit_response_json["org_units"])
    try:
        while i < length:
            dict_parent_child.setdefault(orgUnit_response_json["org_units"][i]["props"]['cwa-parent-ou'], []).append(
                "Org Unit name:->"+orgUnit_response_json["org_units"][i]["name"] + " "
                + "Org Unit id:->" + orgUnit_response_json["org_units"][i]["id"])
            if "org_units" in orgUnit_response_json["org_units"][i]:
                iterate_child(orgUnit_response_json["org_units"][i])
            i += 1
    except Exception as ex:

        logger.error("Exception occurred while iterating org units " + str(ex))


def display_org_units(dict_parent_child):
    if dict_parent_child:
        for parent_ou in dict_parent_child:
            print("\n* Org unit " + parent_ou + " have following child/children ou associated with it ")
            j = 0
            bullet = 1
            while j < len(dict_parent_child[parent_ou]):
                print("\t" +str(bullet) + ".) " + dict_parent_child[parent_ou][j])
                j += 1
                bullet += 1


if set_request_headers():
    if get_authentication_token():
        logger.info("Iterating org units")
        if get_org_units():
            display_org_units(dict_parent_child)
