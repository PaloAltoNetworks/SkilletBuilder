#!/usr/bin/env python3
#
# Executes a basic skillet from the ENV variable 'SKILLET_CONTENT' useful for testing
#
import os
import sys
from tempfile import mkdtemp

from skilletlib.exceptions import LoginException
from skilletlib.exceptions import SkilletLoaderException
from skilletlib.panoply import Panoply
from skilletlib.skillet.panos import PanosSkillet

# each variable will be present in the environ dict on the 'os' module
username = os.environ.get('TARGET_USERNAME', 'admin')
password = os.environ.get('TARGET_PASSWORD', 'admin')
ip = os.environ.get('TARGET_IP', '')
skillet_content = os.environ.get('SKILLET_CONTENT', '')

try:
    device = Panoply(hostname=ip, api_username=username, api_password=password, debug=False)
    skillet_path = mkdtemp()
    skillet_file = os.path.join(skillet_path, '.meta-cnc.yaml')
    with open(skillet_file, 'w') as f:
        f.write(skillet_content)

    skillet = PanosSkillet(skillet_file)
    results = device.execute_skillet(skillet, {})
    print(results)
    sys.exit(0)

except SkilletLoaderException as se:
    print('Error Executing Skillet')
    print(se)
    sys.exit(1)
except LoginException as le:
    print('Error Logging into device')
    print(le)
    sys.exit(1)
