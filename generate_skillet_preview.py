# 12-12-19 nembery@paloaltonetworks.com
import os
import re
import sys

from lxml import etree
from skilletlib import Panoply

config_source = os.environ.get('skillet_source', 'offline')

if config_source == 'offline':
    # grab our two configs from the environment
    base_config_path = os.environ.get('BASE_CONFIG', '/Users/nembery/Downloads/iron_skillet_panos_full.xml')
    # base_config_path = os.environ.get('BASE_CONFIG', '')
    latest_config_path = os.environ.get('LATEST_CONFIG', '/Users/nembery/Downloads/running-config (16).xml')

    with open(base_config_path, 'r') as bcf:
        base_config = bcf.read()

    with open(latest_config_path, 'r') as lcf:
        latest_config = lcf.read()

    p = Panoply()
    snippets = p.generate_skillet_from_configs(base_config, latest_config)
else:
    # each variable will be present in the environ dict on the 'os' module
    username = os.environ.get('TARGET_USERNAME', 'admin')
    password = os.environ.get('TARGET_PASSWORD', '')
    ip = os.environ.get('TARGET_IP', '')
    from_candidate = os.environ.get('FROM_CANDIDATE', 'False')

    p = Panoply(hostname=ip, api_username=username, api_password=password, debug=False)
    snippets = p.generate_skillet(from_candidate=from_candidate)
    if from_candidate:
        latest_config = p.get_configuration(config_source='candidate')
    else:
        latest_config = p.get_configuration(config_source='running')

# check we actually have some diffs
if len(snippets) == 0:
    print('No Candidate Configuration can be found to use to build a skillet!')
    sys.exit(2)

latest_doc = etree.fromstring(latest_config)

print('#' * 80)
print(' ')
print('The following xpaths were found to be modified:')
print(' ')
print('-' * 80)
print(' ')
for s in snippets:
    name = s.get('name', '')
    snippet_xpath = s.get('xpath')
    full_xpath = s.get('full_xpath', '')
    print(f'<a href="#{name}">{full_xpath}</a>')
    xpath = re.sub('^/config', '.', snippet_xpath)
    # parent_element_xpath = '.' + "/".join(xpath.split('/')[:-1])
    parent_elements = latest_doc.xpath(xpath)
    if not parent_elements:
        print('something is broken here')
        continue
    parent_element = parent_elements[0]
    element_string = s.get('element', '')
    # find child element index
    index = 0
    found = False
    for child in parent_element:
        cs = etree.tostring(child).decode('UTF-8')
        cs_stripped = cs.strip()
        whitespace_match = re.search(r'(\s+)$', cs)
        if whitespace_match:
            whitespace = whitespace_match.group()
        else:
            whitespace = ''
        if element_string == cs_stripped:
            # found our child index
            found = True
            parent_element.remove(child)
            title = snippet_xpath.replace('"', "'")
            wrapped_child_element = \
                etree.fromstring(
                    f'<span id="{name}" class="text-danger" title="{title}">{element_string}{whitespace}</span>')
            parent_element.insert(index, wrapped_child_element)
            break
        index = index + 1
    if not found:
        print('did not find this, odd')

latest_config_formatted = etree.tostring(latest_doc, pretty_print=True).decode('UTF-8')
latest_config_html = latest_config_formatted.replace('<', '&lt;').replace('>', '&gt;')
fixed_config_html_1 = re.sub(r'&lt;span id="(.*?)" class="(.*?)" title="(.*?)"&gt;',
                             r'<span class="\2" id="\1" title="\3">', latest_config_html)
fixed_config_html_2 = re.sub(r'&lt;/span&gt;', r'</span>', fixed_config_html_1)

print('-' * 80)
print(fixed_config_html_2)
print('-' * 80)
print('#' * 80)

# later gator
sys.exit(0)
