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
from skilletlib import Panoply
from skilletlib import SkilletLoader
from skilletlib.skillet.panos import PanosSkillet
from skilletlib.skillet.base import Skillet

# each variable will be present in the environ dict on the 'os' module
username = os.environ.get('TARGET_USERNAME', 'admin')
password = os.environ.get('TARGET_PASSWORD', 'admin')
ip = os.environ.get('TARGET_IP', '')
skillet_content_raw = os.environ.get('SKILLET_CONTENT', '')
debug = os.environ.get('DEBUG', False)

# because we are passing this value around, we may need to unescape it here
skillet_content = html.unescape(skillet_content_raw)

# get the full contents of the environment to initialize the skillet context
try:
    panoply = Panoply(hostname=ip, api_username=username, api_password=password, debug=False)

    # every skillet needs a 'config' item in the context
    config = panoply.get_configuration()
    context = dict()
    context['config'] = config

    # create the skillet definition from the 'skillet_content' dict we got from the environ
    skillet_dict = oyaml.safe_load(skillet_content)
    skillet_dict['snippet_path'] = '.'

    # create the skillet object from the skillet dict
    if skillet_dict.get('type') == 'panos':
        skillet: PanosSkillet = PanosSkillet(skillet_dict, panoply)
    else:
        sl = SkilletLoader()
        skillet: Skillet = sl.create_skillet(skillet_dict)

    # ensure all our variables from the environment / outer context is copied in and ready to go
    skillet.update_context(os.environ)
    # execute the skillet and return the results to us
    results = skillet.execute(context)

    print()
    print('=' * 140)
    print('Execution Results:')
    print('=' * 140)
    print()
    print()
    # in this case, just print them out for the user
    if skillet.type == 'pan_validation':
        print(json.dumps(results, indent="  "))
    else:
        print(results)

    if debug:
        print('='*140)
        print('Skillet Content:')
        print(skillet_content)
        print('='*140)
        print('Full Context:')
        for i in skillet.context:
            if i == 'config':
                continue
            item = json.dumps(skillet.context[i], indent="  ")
            print(f'{i} = {item}\n')
        # print(json.dumps(skillet.context))
        print('=' * 140)

    sys.exit(0)

except SkilletLoaderException as se:
    print('Error Executing Skillet')
    print(se)
    sys.exit(1)
except LoginException as le:
    print('Error Logging into device')
    print(le)
    sys.exit(1)
