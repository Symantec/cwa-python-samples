#!/usr/bin/env python
#################################################################################################################
# Copyright 2018 Symantec Corporation. All rights reserved.
# Script to get Events
# You need to provide Client ID and Client Secret Key in config.ini file under Credentials sections, to generate
#  auth token.
# These keys can be found on CWA customer portal, once you are logged in navigate to Settings->API Keys
# The config file must be in the same directory as of the script.
#
# !!!Usage!!!: Update value of  variable scan_profile_id a valid value,
# ( tip!! this can be get from script cwa_getListofScanProfiles.py)
#
# then execute script python
# python cwa_startScanUsingScanProfileID.py
# On success, this script will produce success status of scan
#################################################################################################################
import json
import requests
import configparser
import os
import logging
from pathlib import Path

# create logger
logger = logging.getLogger("cwa_startScanUsingScanProfileID")
logger.setLevel(logging.INFO)

# create console handler (ch) and set level tstart_scan_using_scan_profile_ido debug
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
GET_SCAN_PROFILES_URL = 'GetScanProfilesUrl'
CONFIG_URL_SECTION = 'RequestUrl'

# Getting current working directory
Current_Working_Dir = os.getcwd()

logger.info("cwa_startScanUsingScanProfileID: Current working Directory is " + Current_Working_Dir)
logger.info("cwa_startScanUsingScanProfileID: Checking if config file present in current directory")

config_file = Path(Current_Working_Dir+'/config.ini')

# Checking if config file present
if not config_file.is_file():
    logger.error("cwa_startScanUsingScanProfileID: File config.ini not found in current working directory, "
                 "place config.ini fle in directory \n " + Current_Working_Dir)
    exit()
else :
    logger.info("cwa_startScanUsingScanProfileID: Configfile found in directory " + Current_Working_Dir)


# Creating http request and headers

auth_headers = {}
access_token: None
authurl: None
scan_profiles_url: None
x_epmp_customer_id:  None
x_epmp_domain_id: None
scan_profile_id = "DUMMY SCAN PROFILE" # Place a valid scan profile ID here
start_scan_url: None


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
            print("access_token :: " + access_token)
            print("customer_id :: " + x_epmp_customer_id)
            print("domain_id :: " + x_epmp_domain_id)
            token_cust_domain_id = True
        else:
            logger.error("get_authentication_token(): Response from http auth not received status code is " + str(auth_response.status_code))

    except Exception as ex:
        logger.error("get_authentication_token(): Exception occurred while hitting http request to generate token" + str(ex))
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
        global scan_profiles_url
        scan_profiles_url = config.get(CONFIG_URL_SECTION, GET_SCAN_PROFILES_URL)
        if client_id == "" or client_secret == "" or authurl == "" or scan_profiles_url == "":
            logger.error("set_request_headers(): One or more values empty in config_file")
            return headers_got_set
        else:
            global start_scan_url
            start_scan_url = scan_profiles_url + "/" + scan_profile_id + "/startscan"
            set_request_headers.auth_request['client_id'] = client_id
            set_request_headers.auth_request['client_secret'] = client_secret
            auth_headers['Content-type'] = 'application/json'
            headers_got_set = True

    except Exception as ex:
        logger.error("set_request_headers(): Exception occurred while reading values from config file " + str(ex))
    return headers_got_set


def start_scan_using_scan_profile_id():
    global auth_headers
    start_scan_using_scan_profile_id.start_scan_request = {}
    auth_headers['Authorization'] = access_token
    auth_headers['x-epmp-customer-id'] = x_epmp_customer_id
    auth_headers['x-epmp-domain-id'] = x_epmp_domain_id

    try:
        logger.info("start_scan_using_scan_profile_id(): Hitting http request to start scan ")
        request_json = json.dumps(start_scan_using_scan_profile_id.start_scan_request )
        start_scan_response = requests.put(start_scan_url, data=request_json, headers=auth_headers)
        if start_scan_response.status_code == 200:
            logger.info("start_scan_using_scan_profile_id: scan started successfully http response code " +
                        str(start_scan_response.status_code))
        else:
            logger.error("start_scan_using_scan_profile_id(): request failed to start scan, status code is " +
                         str(start_scan_response.status_code))
    except Exception as ex:
        logger.error("start_scan_using_scan_profile_id(): Exception occurred while starting scan " + str(ex))


if set_request_headers():
    if get_authentication_token():
        start_scan_using_scan_profile_id()



