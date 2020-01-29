#!/usr/bin/env python3
#
# Tool to explore a PAN-OS Configuration
#
import json
import os

import xmltodict
from lxml import etree
from lxml.etree import Element
from skilletlib.exceptions import LoginException
from skilletlib.exceptions import SkilletLoaderException
from skilletlib.panoply import Panos

source = os.environ.get('source', 'offline')

config = ''

if source == 'online':

    config_source = os.environ.get('config_source', 'running')
    username = os.environ.get('TARGET_USERNAME', 'admin')
    password = os.environ.get('TARGET_PASSWORD', 'admin')
    ip = os.environ.get('TARGET_IP', '')

    try:
        device = Panos(hostname=ip, api_username=username, api_password=password, debug=False)
        config = device.get_configuration(config_source=config_source)

    except SkilletLoaderException as se:
        print('Error Executing Skillet')
        print(se)
        exit(1)

    except LoginException as le:
        print('Error Logging into device')
        print(le)
        exit(1)

else:
    config = os.environ.get('config', '')

xpath = os.environ.get('xpath', '')

try:

    config_doc = etree.fromstring(config)
    found = config.doc.xpath(xpath)

    if isinstance(Element, found):
        found_txt = etree.tostring(found)
        found_obj = xmltodict.parse(found)
    else:
        found_txt = str(found)
        found_obj = found

    found_json = json.dumps(found_obj, indent='  ')

    print()
    print('=' * 137)
    print()
    print('Execution Results:')
    print()
    print('=' * 137)
    print()
    print(f'xpath: {xpath}')
    print()
    print(found_txt)
    print()
    print('=' * 137)
    print()
    print(found_json)
    print()
    print('=' * 137)
    print()
except ValueError as ve:
    print('Could not parse config document!')
    print(ve)
    exit(1)
