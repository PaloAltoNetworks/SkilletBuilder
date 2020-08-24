#!/usr/bin/env python3
# Tool to Generate an Ansible Playbook from a set of Configuration diffs between Running and Candidate config,
# or the running and baseline config
# nembery - 082420

import os
import sys

from skilletlib import Panoply
from skilletlib import SkilletLoader
from skilletlib.exceptions import LoginException
from skilletlib.exceptions import SkilletLoaderException

# Grab our PAN-OS target authentication from the environment
username = os.environ.get('TARGET_USERNAME', 'admin')
password = os.environ.get('TARGET_PASSWORD', '')
ip = os.environ.get('TARGET_IP', '')
from_candidate = os.environ.get('FROM_CANDIDATE', 'False')

# check if we should generate the skillet from the candidate of the running config
fc = False if from_candidate == 'False' else True

snippets = list()

try:
    device = Panoply(hostname=ip, api_username=username, api_password=password, debug=False)
    snippets = device.generate_skillet(from_candidate=fc)

except SkilletLoaderException as se:
    print('Error Executing Skillet')
    print(se)
    sys.exit(1)
except LoginException as le:
    print('Error Logging into device')
    print(le)
    sys.exit(1)

# check we actually have some diffs
if len(snippets) == 0:
    print('No Diffs found between these two configs')

    sys.exit(2)

# SkilletLoader is used to... Load Skillets
skillet_loader = SkilletLoader()

# create_skillet will return a Skillet Object from the metadata dictionary passed in.
# in this case, we create a minimal metadata dict and pass it in to create a simple 'template' skillet
# a template skillet is a nice wrapper around the jinja engine
template_skillet = skillet_loader.create_skillet(
    {'type': 'template',
     'snippets': [
         {'name': 'template', 'file': './ansible_pb_template.j2'}
     ]
     }
)

# to execute this skillet, create the context object which includes any variables found in the template file
context = dict()
context['snippets'] = snippets
context['playbook_name'] = 'Auto Generated PAN-OS Playbook'
# execute the template skillet and get the returned output
output = template_skillet.execute(context)

# template skillets add the 'template' attribute into the output which contains the rendered template
# print it out for the user
print(output['template'])

# later gator
sys.exit(0)
