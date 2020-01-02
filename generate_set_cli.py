# 12-19-19 nembery@paloaltonetworks.com
import os

from skilletlib import Panoply

config_source = os.environ.get('skillet_source', 'online')

if config_source == 'offline':
    # grab our two configs from the environment
    base_config_path = os.environ.get('BASE_CONFIG', '')
    latest_config_path = os.environ.get('LATEST_CONFIG', '')

    with open(base_config_path, 'r') as bcf:
        base_config = bcf.read()

    with open(latest_config_path, 'r') as lcf:
        latest_config = lcf.read()

    p = Panoply()
else:
    # each variable will be present in the environ dict on the 'os' module
    username = os.environ.get('TARGET_USERNAME', 'admin')
    password = os.environ.get('TARGET_PASSWORD', '')
    ip = os.environ.get('TARGET_IP', '').strip()
    from_candidate = os.environ.get('FROM_CANDIDATE', 'True')

    p = Panoply(hostname=ip, api_username=username, api_password=password, debug=False)
    if from_candidate == 'True' or from_candidate is True:
        base_config = p.get_configuration(config_source='running')
        latest_config = p.get_configuration(config_source='candidate')
    else:
        base_config = p.get_configuration(config_source='baseline')
        latest_config = p.get_configuration(config_source='running')

cli_diffs = p.generate_set_cli_from_configs(base_config, latest_config)

for i in cli_diffs:
    print(i)
