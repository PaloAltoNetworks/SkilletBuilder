# 12-12-19 nembery@paloaltonetworks.com
import os
import re
import sys

from lxml import etree
from skilletlib import Panoply
from skilletlib.exceptions import LoginException
from skilletlib.exceptions import SkilletLoaderException

config_source = os.environ.get("skillet_source", "offline")

if config_source == "offline":
    # grab our two configs from the environment
    base_config_path = os.environ.get("BASE_CONFIG", "")
    latest_config_path = os.environ.get("LATEST_CONFIG", "")

    with open(base_config_path, "r") as bcf:
        base_config = bcf.read()

    with open(latest_config_path, "r") as lcf:
        latest_config = lcf.read()

    p = Panoply()
    snippets = p.generate_skillet_from_configs(base_config, latest_config)
else:
    # each variable will be present in the environ dict on the 'os' module
    username = os.environ.get("TARGET_USERNAME", "admin")
    password = os.environ.get("TARGET_PASSWORD", "")
    ip = os.environ.get("TARGET_IP", "")
    config_source = os.environ.get("CONFIG_SOURCE", "candidate")

    snippets = list()

    try:
        device = Panoply(hostname=ip, api_username=username, api_password=password, debug=False)

        if config_source == "specific":
            config_version = os.environ.get("CONFIG_VERSION", "-1")
            previous_config = device.get_configuration(config_source=config_version)
            latest_config = device.get_configuration(config_source="running")
        elif config_source == "candidate":
            previous_config = device.get_configuration(config_source="running")
            latest_config = device.get_configuration(config_source="candidate")
        else:
            # use previous config by default
            previous_config = device.get_configuration(config_source="-1")
            latest_config = device.get_configuration(config_source="running")

        snippets = device.generate_skillet_from_configs(previous_config, latest_config)

        if len(snippets) == 0 and config_source == "candidate":
            print("No Candidate Configuration can be found to use to build a skillet!")
            sys.exit(2)
        elif len(snippets) == 0:
            print(f"No changes found between {previous_config} and {latest_config}")
            sys.exit(2)

    except SkilletLoaderException as se:
        print("Error Executing Skillet")
        print(se)
        sys.exit(1)
    except LoginException as le:
        print("Error Logging into device")
        print(le)
        sys.exit(1)


latest_doc = etree.fromstring(latest_config)

print("#" * 80)
print(" ")
print("The following xpaths were found to be modified:")
print(" ")
print("-" * 80)
print(" ")
for s in snippets:
    name = s.get("name", "")
    snippet_xpath = s.get("xpath")
    full_xpath = s.get("full_xpath", "")
    print(f'<a href="#{name}">{full_xpath}</a>')
    xpath = re.sub("^/config", ".", snippet_xpath)
    # parent_element_xpath = '.' + "/".join(xpath.split('/')[:-1])
    parent_elements = latest_doc.xpath(xpath)
    if not parent_elements:
        print("something is broken here")
        continue
    parent_element = parent_elements[0]
    element_string = s.get("element", "")
    # find child element index
    index = 0
    found = False
    for child in parent_element:
        cs = etree.tostring(child).decode("UTF-8")
        cs_stripped = cs.strip()
        whitespace_match = re.search(r"(\s+)$", cs)
        if whitespace_match:
            whitespace = whitespace_match.group()
        else:
            whitespace = ""
        if element_string == cs_stripped:
            # found our child index
            found = True
            parent_element.remove(child)
            title = snippet_xpath.replace('"', "'")
            wrapped_child_element = etree.fromstring(
                f'<span id="{name}" class="text-danger" title="{title}">{element_string}{whitespace}</span>'
            )
            parent_element.insert(index, wrapped_child_element)
            break
        index = index + 1
    if not found:
        print("did not find this, odd")


def rp(match):
    return "&nsbp;" * len(match.group())


latest_config_formatted = etree.tostring(latest_doc, pretty_print=True).decode("UTF-8")
latest_config_html = latest_config_formatted.replace("<", "&lt;").replace(">", "&gt;")
fixed_config_html_1 = re.sub(
    r'&lt;span id="(.*?)" class="(.*?)" title="(.*?)"&gt;', r'<span class="\2" id="\1" title="\3">', latest_config_html
)
fixed_config_html_2 = re.sub(r"&lt;/span&gt;", r"</span>", fixed_config_html_1)

print("-" * 80)
print(fixed_config_html_2)
print("-" * 80)
print("#" * 80)

# later gator
sys.exit(0)
