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

source = os.environ.get('source', 'online')

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

xpath = os.environ.get('xpath', "/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles")

try:

    config_doc = etree.fromstring(config)
    found = config_doc.xpath(xpath)

    if isinstance(found, list):
        if len(found) == 1:
            found_item = found.pop(0)
            if isinstance(found_item, str):
                found_str = str(found_item)
                found_obj = found_str
            else:
                found_str = etree.tostring(found_item).decode('UTF-8')
                found_obj = xmltodict.parse(found_str)
        else:
            found_obj = list()
            found_str = 'List of items:\n\n'

            for found_item in found:
                if isinstance(found_item, str):
                    found_str = f'{found_str}\n{found_item}'
                    found_obj.append(found_item)

                else:
                    found_item_str = etree.tostring(found_item).decode('UTF-8')
                    found_str = f'{found_str}\n{found_item_str}'
                    found_obj.append(xmltodict.parse(found_item_str))

    elif isinstance(found, str):
        found_obj = found
        found_str = found
    else:
        found_str = etree.tostring(found)
        found_obj = xmltodict.parse(found_str)

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
    print('=' * 137)
    print()
    print('xml:')
    print(found_str)
    print()
    print('=' * 137)
    print()
    print('json:')
    print(found_json)
    print()
    print('=' * 137)
    print()
except ValueError as ve:
    print('Could not parse config document!')
    print(ve)
    exit(1)
