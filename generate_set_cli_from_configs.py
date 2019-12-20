# 12-19-19 nembery@paloaltonetworks.com
from skilletlib import Panoply
import os
import sys
import re
from xml.etree import ElementTree
from lxml import etree

# grab our two configs from the environment
base_config_path = os.environ.get('BASE_CONFIG', '/Users/nembery/Downloads/sdwan_stage1.xml')
latest_config_path = os.environ.get('LATEST_CONFIG', '/Users/nembery/Downloads/sdwan_final_test.xml')

with open(base_config_path, 'r') as bcf:
    base_config = bcf.read()

with open(latest_config_path, 'r') as lcf:
    latest_config = lcf.read()

p = Panoply()

cli_diffs = p.generate_set_cli_from_configs(base_config, latest_config)

for i in cli_diffs:
    print(i)
