#!/usr/bin/env python3
#
# This example uses ENV variables to gather input from the user
# The .meta-cnc file defines 3 input variables:
# USERNAME, PASSWORD, SECRET
# This script shows how to obtain the values entered from the user
#
import json
import os
import sys

from skilletlib.exceptions import LoginException
from skilletlib.exceptions import SkilletLoaderException
from skilletlib.panoply import Panoply

# each variable will be present in the environ dict on the 'os' module
username = os.environ.get('TARGET_USERNAME', 'admin')
password = os.environ.get('TARGET_PASSWORD', '')
ip = os.environ.get('TARGET_IP', '')
config_source = os.environ.get('CONFIG_SOURCE', 'candidate')

snippets = list()

try:
    device = Panoply(hostname=ip, api_username=username, api_password=password, debug=False)

    if config_source == 'specific':
        config_version = os.environ.get('CONFIG_VERSION', '-1')
        previous_config = device.get_configuration(config_source=config_version)
        latest_config = device.get_configuration(config_source='running')
    elif config_source == 'candidate':
        previous_config = device.get_configuration(config_source='running')
        latest_config = device.get_configuration(config_source='candidate')
    else:
        # use previous config by default
        previous_config = device.get_configuration(config_source='-1')
        latest_config = device.get_configuration(config_source='running')

    snippets = device.generate_skillet_from_configs(previous_config, latest_config)

    if len(snippets) == 0 and config_source == 'candidate':
        print('No Candidate Configuration can be found to use to build a skillet!')
        sys.exit(2)

    print(json.dumps(snippets, indent=2))
    sys.exit(0)

except SkilletLoaderException as se:
    print('Error Executing Skillet')
    print(se)
    sys.exit(1)
except LoginException as le:
    print('Error Logging into device')
    print(le)
    sys.exit(1)

