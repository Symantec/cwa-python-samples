#!/usr/bin/env python
#################################################################################################################
# Copyright 2018 Symantec Corporation. All rights reserved.
# Script to get Events
# You need to provide Client ID and Client Secret Key in config.ini file under Credentials sections, to generate
#  auth token.
# These keys can be found on CWA customer portal, once you are logged in navigate to Settings->API Keys
# The config file must be in the same directory as of the script.
#
# !!!Usage!!!: Update values of following variables with in the script prior to execute it
#
# get_events_page_size ; get_events_page_number ; get_events_start_date ; get_events_end_date
# get_events_product_id ; get_events_service_name ; get_events_additional_filter
# then execute script python
# python cwa_getEvents.py
# On success, this script will produce json output of the events found as per the request.
# for rest of the request.
#################################################################################################################
import json
from typing import List

import requests
import configparser
import os
import logging
from pathlib import Path

# create logger
logger = logging.getLogger("cwa_getEvents")
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
GET_EVENTS_URL = 'GetEventsUrl'

# Getting current working directory
Current_Working_Dir = os.getcwd()

logger.info("cwa_getEvents: Current working Directory is " + Current_Working_Dir)
logger.info("cwa_getEvents: Checking if config file present in current directory")

config_file = Path(Current_Working_Dir+'/config.ini')

# Checking if config file present
if not config_file.is_file():
    logger.error("cwa_getEvents: File config.ini not found in current working directory, "
                 "place config.ini fle in directory \n " + Current_Working_Dir)
    exit()
else :
    logger.info("cwa_getEvents: Configfile found in directory " + Current_Working_Dir)


# Creating http request and headers

auth_headers = {}
access_token: None
authurl: None
get_events_url: None
x_epmp_customer_id:  None
x_epmp_domain_id: None

get_events_page_size = 100
get_events_page_number = 0
get_events_start_date = "2018-10-20T00:00:00.000Z"
get_events_end_date = "2018-10-27T23:59:00.000Z"
get_events_product_id = "5B5FF903-27D7-46AF-AA63-EE24D0BD41CD"
get_events_service_name = "IAM Password Policy"
get_events_additional_filter = "(product_uid='"+get_events_product_id+"') && " \
                                                                               "(service_name='"+get_events_service_name+"')"
get_events_display_labels = False




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
        global get_events_url
        get_events_url = config.get(CONFIG_URL_SECTION, GET_EVENTS_URL)
        if client_id == "" or client_secret == "" or authurl == "" or get_events_url == "":
            logger.error("set_request_headers(): One or more values empty in config_file")
            return headers_got_set
        else:
            set_request_headers.auth_request['client_id'] = client_id
            set_request_headers.auth_request['client_secret'] = client_secret
            auth_headers['Content-type'] = 'application/json'
            headers_got_set = True

    except Exception as ex:
        logger.error("generateAuthToken: Exception occurred while reading values from config file " + str(ex))
    return headers_got_set


def get_events_details():
    global auth_headers
    get_events_details.get_events_request_body = {'pageSize': get_events_page_size, 'pageNumber': get_events_page_number,
                               'startDate': get_events_start_date, 'endDate': get_events_end_date,
                               'additionalFilters': get_events_additional_filter,
                               'displayLabels': get_events_display_labels }
    auth_headers['Authorization'] = access_token
    auth_headers['x-epmp-customer-id'] = x_epmp_customer_id
    auth_headers['x-epmp-domain-id'] = x_epmp_domain_id

    try:
        logger.info("get_events_details(): Hitting http request get events details ")
        request_json = json.dumps(get_events_details.get_events_request_body)
        get_events_details_response = requests.post(get_events_url, data=request_json, headers=auth_headers)
        if get_events_details_response.status_code == 200:
            logger.info("get_events_details(): Get events successful status code "
                        + str(get_events_details_response.status_code))
            print(get_events_details_response.text)
        else:
            logger.error("get_events_details(): Failed to get data for events, status code is " +
                         str(get_events_details.status_code))
    except Exception as ex:
        logger.error("get_events_details(): Exception occurred while getting events details  " + str(ex))


if set_request_headers():
    if get_authentication_token():
        get_events_details()



