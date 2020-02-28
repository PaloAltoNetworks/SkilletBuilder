#!/usr/bin/env python3
#
# Executes a basic skillet from the ENV variable 'SKILLET_CONTENT' useful for testing
#
import html
import os
import sys
import oyaml
import json

from skilletlib.exceptions import LoginException
from skilletlib.exceptions import SkilletLoaderException
from skilletlib import Panos
from skilletlib import SkilletLoader
from skilletlib.skillet.panos import PanosSkillet
from skilletlib.skillet.base import Skillet

source = os.environ.get('source', 'online')

config = ''
device = None

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

skillet_content_raw = os.environ.get('SKILLET_CONTENT', '')
debug = os.environ.get('DEBUG', False)

# because we are passing this value around, we may need to unescape it here
skillet_content = html.unescape(skillet_content_raw)

sl = SkilletLoader()
# get the full contents of the environment to initialize the skillet context
try:

    context = dict()
    context['config'] = config

    # create the skillet definition from the 'skillet_content' dict we got from the environ
    skillet_dict_raw = oyaml.safe_load(skillet_content)

    # use skilletLoader to normalize the skillet definition and fix common config file errors
    skillet_dict = sl.normalize_skillet_dict(skillet_dict_raw)
    skillet_dict['snippet_path'] = '.'

    # create the skillet object from the skillet dict
    if skillet_dict.get('type') == 'panos':
        skillet: PanosSkillet = PanosSkillet(skillet_dict, device)
    else:
        skillet: Skillet = sl.create_skillet(skillet_dict)

    # ensure all our variables from the environment / outer context is copied in and ready to go
    skillet.update_context(os.environ)
    # execute the skillet and return the results to us
    results = skillet.execute(context)

    print()
    print('=' * 137)
    print()
    print('Execution Results:')
    print()
    print('=' * 137)
    print()
    # in this case, just print them out for the user
    if skillet.type == 'pan_validation':
        print(json.dumps(results, indent="  "))
    else:
        print(results)

    if debug:
        print('='*137)
        print()
        print('Skillet Content:')
        print()
        print('='*137)
        print()
        print(skillet_content)
        print('='*137)
        print()
        print('Full Context:')
        print()
        print('='*137)
        print()
        for i in skillet.context:
            if i == 'config':
                continue
            item = json.dumps(skillet.context[i], indent="  ")
            print(f'{i} = {item}\n')
        print('=' * 137)

    sys.exit(0)

except SkilletLoaderException as se:
    print('Error Executing Skillet')
    print(se)
    sys.exit(1)
except LoginException as le:
    print('Error Logging into device')
    print(le)
    sys.exit(1)
