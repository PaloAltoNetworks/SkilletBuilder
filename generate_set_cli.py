# 12-19-19 nembery@paloaltonetworks.com
import os
import sys

from skilletlib import Panoply
from skilletlib.exceptions import LoginException
from skilletlib.exceptions import SkilletLoaderException

config_source = os.environ.get('skillet_source', 'online')

if config_source == 'offline':
    # grab our two configs from the environment
    base_config_path = os.environ.get('BASE_CONFIG', '')
    latest_config_path = os.environ.get('LATEST_CONFIG', '')

    with open(base_config_path, 'r') as bcf:
        previous_config = bcf.read()

    with open(latest_config_path, 'r') as lcf:
        latest_config = lcf.read()

    device = Panoply()
else:
    # each variable will be present in the environ dict on the 'os' module
    username = os.environ.get('TARGET_USERNAME', 'admin')
    password = os.environ.get('TARGET_PASSWORD', '')
    ip = os.environ.get('TARGET_IP', '').strip()
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

    except SkilletLoaderException as se:
        print('Error Executing Skillet')
        print(se)
        sys.exit(1)
    except LoginException as le:
        print('Error Logging into device')
        print(le)
        sys.exit(1)

cli_diffs = device.generate_set_cli_from_configs(previous_config, latest_config)

for i in cli_diffs:
    print(i)
