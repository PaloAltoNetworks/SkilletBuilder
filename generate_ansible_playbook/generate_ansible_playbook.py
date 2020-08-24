#!/usr/bin/env python3

import os
import sys

from skilletlib import Panoply
from skilletlib import SkilletLoader

# grab our two configs from the environment
base_config_path = os.environ.get('BASE_CONFIG', '')
latest_config_path = os.environ.get('LATEST_CONFIG', '')

with open(base_config_path, 'r') as bcf:
    base_config = bcf.read()

with open(latest_config_path, 'r') as lcf:
    latest_config = lcf.read()

# init the Panoply helper class, note we do not need connection information, as we only need offline mode
# to compare two configurations
p = Panoply()

# insert magic here
snippets = p.generate_skillet_from_configs(base_config, latest_config)

# check we actually have some diffs
if len(snippets) == 0:
    print('No Diffs found between these two configs')

    sys.exit(2)

skillet_loader = SkilletLoader()

# template_skillet = skillet_loader.create_skillet(template_skillet_config)
template_skillet = skillet_loader.create_skillet(
    {'snippets': [
        {'name': 'template', 'file': './ansible_pb_template.j2'}
    ]
    }
)

context = dict()
context['snippets'] = snippets
context['playbook_name'] = 'Auto Generated PAN-OS Playbook'
output = template_skillet.execute(context)

print(output['template'])

# later gator
sys.exit(0)
