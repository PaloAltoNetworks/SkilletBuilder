# 12-12-19 nembery@paloaltonetworks.com
from skilletlib import Panoply
import os
import sys
import re
from xml.etree import ElementTree
from lxml import etree


config_source = os.environ.get('skillet_source', 'offline')

if config_source == 'offline':
    # grab our two configs from the environment
    base_config_path = os.environ.get('BASE_CONFIG', '')
    latest_config_path = os.environ.get('LATEST_CONFIG', '')

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

latest_doc = ElementTree.fromstring(latest_config)

print('#'*80)
print(' ')
print('The following xpaths were found to be modified:')
print(' ')
print('-'*80)
print(' ')
for s in snippets:
    name = s.get('name', '')
    full_xpath = s.get('xpath')
    print(f'<a href="#{name}">{full_xpath}</a>')
    xpath = re.sub('^/config', '.', full_xpath)
    # parent_element_xpath = '.' + "/".join(xpath.split('/')[:-1])
    parent_element = latest_doc.find(xpath)
    element_string = s.get('element', '')
    # find child element index
    index = 0
    found = False
    for child in parent_element:
        cs = ElementTree.tostring(child).decode('UTF-8')
        whitespace_match = re.search(r'(\s+)$', cs)
        if whitespace_match:
            whitespace = whitespace_match.group()
        else:
            whitespace = ''
        if element_string == cs:
            # found our child index
            found = True
            parent_element.remove(child)
            title = full_xpath.replace('"', "'")
            wrapped_child_element = \
                ElementTree.fromstring(f'<span id="{name}" class="text-danger" title="{title}">{element_string}</span>{whitespace}')
            parent_element.insert(index, wrapped_child_element)
            break
        index = index + 1
    if not found:
        print('did not find this, odd')

latest_config_str = ElementTree.tostring(latest_doc).decode('UTF-8')
etree_dom_obj = etree.fromstring(latest_config_str)
latest_config_formatted = etree.tostring(etree_dom_obj, pretty_print=True).decode('UTF-8')
latest_config_html = latest_config_formatted.replace('<', '&lt;').replace('>', '&gt;')
fixed_config_html_1 = re.sub(r'&lt;span class="(.*?)" id="(.*?)" title="(.*?)"&gt;', r'<span class="\1" id="\2" title="\3">', latest_config_html)
fixed_config_html_2 = re.sub(r'&lt;/span&gt;', r'</span>', fixed_config_html_1)

print('-'*80)
print(fixed_config_html_2)
print('-'*80)
print('#'*80)

# later gator
sys.exit(0)
