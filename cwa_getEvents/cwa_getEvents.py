#!/usr/bin/env python
#
# Copyright 2017 Symantec Corporation. All rights reserved.
# You may need to import dependent packages , request and configparser.
#
import sys
if sys.version_info[0] < 2 or sys.version_info[1] < 7:
    print("You must have python 2.7 or above to execute the script. Current version is "+str(sys.version_info[0]) +"."+str(sys.version_info[1]))
    exit()
import json
import requests
import configparser
import os
import logging
from datetime import datetime, timedelta
import time

CUSTOMER_ID = 'CUSTOMER_ID'
DOMAIN_ID = 'DOMAIN_ID'
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
PROXY_STATUS = 'PROXY_STATUS'
PROTOCOL = 'PROTOCOL'
PROXY_HOST = 'HOST'
PROXY_USER_NAME = 'USER_NAME'
PROXY_PASSWORD = 'PASSWORD'
PROXY_PORT = 'PROXY_PORT'
logger = logging.getLogger("cwa_getEvents")
# Getting current working directory
Current_Working_Dir = os.getcwd()
logger.info("cwa_getEvents: Current working Directory is " + Current_Working_Dir)
logger.info("cwa_getEvents: Checking if config file present in current directory")


CONFIG_INI = os.path.join(Current_Working_Dir, 'ScwaGetEventsConfig.ini')
STATUS_INI = os.path.join(Current_Working_Dir, 'ScwaGetEventsStatus.status')
PAGE_SIZE = 100
RETRY_COUNT = 3
STATUS_DATES_SECTION = 'ScwaGetEventsDates'
CONFIG_CREDS_SECTION = 'Credentials'
CONFIG_EVENTS_SECTION = 'Events'
CONFIG_PROXY_SECTION = 'Proxy'
START_DATE = 'startDate'
EVENT_TYPE_FILTER = 'EventTypeFilter'
GET_EVENTS_FROM_DAYS = 'GetEventsFromDays'
SCWP_API_KEYS_REALM = "ScwaApiKeyCreds"

scwaAuthUrl = 'https://scwp.securitycloud.symantec.com/dcs-service/dcscloud/v1/oauth/tokens'
getScwaEventsUrl = 'https://scwp.securitycloud.symantec.com/dcs-service/dcscloud/v1/event/query'

authHeaders = {'Content-type': 'application/json'}
authRequest = {}
eventDatetime = ''
proxy = {}
proxyStatus = "disabled"
update_status_file = True
getScwaEventsRequest = {'pageSize': PAGE_SIZE, 'order': 'ASCENDING', 'searchFilter': {}, 'displayLabels': 'false'}


def setupLogging(
        default_path='logging.json',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def updateStatusIniFile():
    config = configparser.RawConfigParser()
    config.add_section(STATUS_DATES_SECTION)
    config.set(STATUS_DATES_SECTION, START_DATE, eventDatetime)
    with open(STATUS_INI, 'w') as configfile:
        config.write(configfile)


def getCreds():
    Config = configparser.ConfigParser()
    Config.read(CONFIG_INI)
    return {'clientId': Config.get(CONFIG_CREDS_SECTION, CLIENT_ID),
            'clientSecretKey': Config.get(CONFIG_CREDS_SECTION, CLIENT_SECRET)}

def authenticate():
    for retry in range(RETRY_COUNT):
        authRequestJson = json.dumps(authRequest)
        if proxyStatus.lower() == "enabled":
            authResponse = requests.post(scwaAuthUrl, data=authRequestJson, headers=authHeaders, proxies=proxy, verify=False)
        else:
            authResponse = requests.post(scwaAuthUrl, data=authRequestJson, headers=authHeaders, verify=False)
        if authResponse.status_code != requests.codes.ok:
            if retry >= RETRY_COUNT:
                authResponse.raise_for_status()
            time.sleep(retry * 60)
            continue
        else:
            break
    accessToken = authResponse.json()['access_token']
    authHeaders['Authorization'] = 'Bearer ' + accessToken


try:
    # setupLogging()
    Config = configparser.ConfigParser()
    Config.read(CONFIG_INI)
    proxyStatus = Config.get(CONFIG_PROXY_SECTION, PROXY_STATUS)
    if proxyStatus.lower() == "enabled":
        proxy_protocol = Config.get(CONFIG_PROXY_SECTION, PROTOCOL)
        proxy_host = Config.get(CONFIG_PROXY_SECTION, PROXY_HOST)
        proxy_user = Config.get(CONFIG_PROXY_SECTION, PROXY_USER_NAME)
        proxy_password = Config.get(CONFIG_PROXY_SECTION, PROXY_PASSWORD)
        proxy_port = Config.get(CONFIG_PROXY_SECTION, PROXY_PORT)
        if proxy_protocol == "" or proxy_host == "" or proxy_user == "" or proxy_password == "" or proxy_port == "":
            logging.error("You have kept proxy enabled in config.ini file, please provide values for proxy PROTOCOL, "
                          "HOST, USER_NAME, PASSWORD, PROXY_PORT under \"Proxy\" section in "+CONFIG_INI + " file.")
            update_status_file = False
            exit(1)
        else:
            proxy[proxy_protocol] = proxy_protocol + "://" + proxy_user + ":" + proxy_password + "@" + proxy_host + ":" + proxy_port
    customerId = Config.get(CONFIG_CREDS_SECTION, CUSTOMER_ID)
    domainId = Config.get(CONFIG_CREDS_SECTION, DOMAIN_ID)
    creds = getCreds()
    clientId = creds.get('clientId')
    clientSecret = creds.get('clientSecretKey')
    eventTypeFilterConfig = Config.get(CONFIG_EVENTS_SECTION, EVENT_TYPE_FILTER)

    authHeaders['x-epmp-customer-id'] = customerId
    authHeaders['x-epmp-domain-id'] = domainId
    authRequest['client_id'] = clientId
    authRequest['client_secret'] = clientSecret

    statusIni = configparser.ConfigParser()
    statusIni.read(STATUS_INI)
    startDate = statusIni.get(STATUS_DATES_SECTION, START_DATE)
    getEventsFromDays = Config.getint(CONFIG_EVENTS_SECTION, GET_EVENTS_FROM_DAYS)
    if (startDate is None) or (startDate == ""):
        startDate = (datetime.today() - timedelta(days=getEventsFromDays)).isoformat()
    else:
        if startDate.endswith('Z'):
            startDate = (datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(milliseconds=1)).isoformat()
        else:
            startDate = (datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S.%f') + timedelta(milliseconds=1)).isoformat()

    eventTypes = eventTypeFilterConfig.strip().split(',')
    eventTypesWithQuotes = ','.join('\"{0}\"'.format(eventType) for eventType in eventTypes)
    eventTypeFilter = 'type_class IN [' + eventTypesWithQuotes + ']'

    getScwaEventsRequest['startDate'] = startDate
    getScwaEventsRequest['endDate'] = datetime.now().isoformat()
    getScwaEventsRequest['additionalFilters'] = eventTypeFilter
    eventDatetime = startDate

    pageNumber = 0
    while True:
        getScwaEventsRequest['pageNumber'] = pageNumber
        getScwaEventsRequestJson = json.dumps(getScwaEventsRequest)
        if proxyStatus.lower() == "enabled":
            scwaEventsResponse = requests.post(getScwaEventsUrl, data=getScwaEventsRequestJson, headers=authHeaders, proxies=proxy,verify=False)
        else:
            scwaEventsResponse = requests.post(getScwaEventsUrl, data=getScwaEventsRequestJson, headers=authHeaders, verify=False)

        if scwaEventsResponse.status_code == 401:
            authenticate()
            if proxyStatus.lower() == "enabled":
                scwaEventsResponse = requests.post(getScwaEventsUrl, data=getScwaEventsRequestJson, headers=authHeaders,
                                                   proxies=proxy,  verify=False)
            else:
                scwaEventsResponse = requests.post(getScwaEventsUrl, data=getScwaEventsRequestJson, headers=authHeaders, verify=False)

        if scwaEventsResponse.status_code != requests.codes.ok:
            scwaEventsResponse.raise_for_status()

        scwaEventsJson = scwaEventsResponse.json()
        scwaEvents = scwaEventsJson['result']
        totalScwaEvents = scwaEventsJson['total']

        if totalScwaEvents == 0:
            break

        for scwaEvent in scwaEvents:
            print(json.dumps(scwaEvent))
            print('\n')
            sys.stdout.flush()
            eventDatetime = scwaEvent['time']

        pageNumber += 1
except:
    raise
finally:
    updateStatusIniFile()
