Validation
==========

Overview
--------

This tutorial walks through the creation and testing of a validation skillet that will:

  * Check if NTP servers are configured
  * Check is password complexity is enabled with a minimum-length >= 12 characters
  * Check if all configured URL-filtering profiles are blocking the malware category
  * Check if all 'allow' security rules are configured with a security profile or group

Unlike configuration skillets that can start with the difference between two configuration files, validation
skillets are more open-ended. Therefore builders need to learn the mechanics of validation skillets to apply to their
own use cases. This includes capturing outputs as variables and using them in boolean tests.

The video provides an end-to-end perspective for building a validation skillet as a complement
to the documentation content.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=17392613-262a-4606-a11a-ab6c010b894e&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

|

Prerequisites
-------------

It is recommended that users review the following content before building a validation skillet

    * :ref:`XML and Skillets` to understand syntax, structure, XML parsing, and tools
    * :ref:`Jinja and Skillets` to understand variables and filters
    * :ref:`Custom Jinja Filters` to see how custom jinja filters can be applied
    * :ref:`Capture Output` to see various types of capture outputs to use in tests
    * Configuration Tutorial :ref:`Setting Up the Sandbox` for EDI, device, and Github readiness
    * :ref:`Skillet Builder Tools` specifically the Configuration Explorer and Test Tool

You can also view the short video giving a brief overview of validation skillets.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=3f7d279c-c732-49b9-bd0c-ab6c0116a41e&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

|

Example .meta-cnc.yaml File
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This tutorial will be recreating the .meta-cnc.yaml file in the SkilletBuilder repo as the `sample_validation_skillet`_

.. _sample_validation_skillet: https://github.com/PaloAltoNetworks/SkilletBuilder/blob/master/sample_validation_skillet/.meta-cnc.yaml

The same file is also shown below.

  .. toggle-header:: class
      :header: **show/hide the output .meta-cnc.yaml file**

      .. code-block:: yaml

        name: sample_validation_skilletbuilder
        label: Sample Validation Skillet

        description: |
          Short set of validations for skilletBuilder training tutorial with ntp check, password complexity,
          URL filtering for malware, and security allow rules with profiles or groups

        type: pan_validation
        labels:
          collection:
            - Skillet Builder
            - Validation

        variables:

          - name: placeholder
            description: Some Parameter
            default: yes
            type_hint: hidden

        snippets:

        # get ntp server and password complexity objects
          - name: device_config_file
            cmd: parse
            variable: config
            outputs:
              - name: ntp_servers
                capture_object: /config/devices/entry[@name='localhost.localdomain']/deviceconfig/system/ntp-servers
              - name: password_complexity
                capture_object: /config/mgt-config/password-complexity

        # check that ntp servers are configured
          - name: ntp_servers_test
            label: configure primary and secondary ntp servers
            test: |
              (
              ntp_servers | tag_present('primary-ntp-server.ntp-server-address')
              and ntp_servers | tag_present('secondary-ntp-server.ntp-server-address')
              )
            fail_message: |
              time server configuration is reccommended to ensure the firewall clock is in sync with external service and logging
              platforms.
            pass_message: recommended primary and secondary ntp servers are configured
            documentation_link: https://iron-skillet.readthedocs.io/en/docs_dev/viz_guide_panos.html#device-setup-services-services

         # check for password complexity minimum password length
          - name: password_complexity_test
            label: configure strong password complexity ( >= 12 chars)
            test: |
              (
              password_complexity | element_value('enabled') == 'yes'
              and password_complexity | element_value('minimum-length') >= '12'
              )
            fail_message: |
              check that password complexity is enabled with a minimum password length of 12 characters
            pass_message: |
              password complexity is enabled with a minimum password length of 12 characters
            documentation_link: https://iron-skillet.readthedocs.io/en/docs_dev/viz_guide_panos.html#device-setup-management-minimum-password-complexity

         # test that all url-filtering profiles block the category malware
          - name: url_profile_test
            cmd: parse
            variable: config
            outputs:
              # get list of all url profiles for debug example
              - name: url_filtering_profiles
                capture_list: |-
                  /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles/url-filtering/entry/@name

              # get list of url profiles with malware explicitly set to block
              # using this model instead of checking for alert, allow, continue - especially with allow not showing in the config
              - name: url_profiles_block_malware
                capture_list: |-
                  /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles/url-filtering/entry
                  /block/member[text()='malware']/../../@name

              # get list of all url profiles then filter to profiles not in url_profiles_block_malware
              - name: url_profiles_not_blocking_malware
                capture_list: |-
                  /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles/url-filtering/entry/@name
                filter_items: item not in url_profiles_block_malware

          # check that all url profiles are blocking malware
          - name: check_all_url_profiles_block_malware
            label: check that all url profiles block category malware
            test: url_profiles_not_blocking_malware | length == 0
            severity: high
            fail_message: |
              url profiles not blocking malware: {{ url_profiles_not_blocking_malware }}
            pass_message: |
              all url profiles are currently blocking the category malware
            documentation_link: https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-admin/url-filtering/configure-url-filtering.html#

         # test that all allow security policies have a profile or profile-group configured
          - name: security_policy_test
            cmd: parse
            variable: config
            outputs:
              # get a list of security policies with a profile or group configured
              - name: security_policies_with_profile_or_group
                capture_list: |-
                  /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
                  /rulebase/security/rules/entry/profile-setting/../@name

              # get a list of security policies with action allow
              - name: allow_security_policies_without_profile
                capture_list: |-
                  /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
                  /rulebase/security/rules/entry/action[text()='allow']/../@name
                filter_items: item not in security_policies_with_profile_or_group

          # check that all allow security policies have a profile or group
          - name: check_allow_security_policies_have_profile
            label: check that all allow security policies have a profile or group
            test: allow_security_policies_without_profile | length == 0
            severity: medium
            fail_message: |
              allow security policies without a profile or group: {{ allow_security_policies_without_profile }}
            pass_message: |
              all allow security policies have a profile or group configured
            documentation_link: https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-admin/policy/security-profiles/create-a-security-profile-group.html

Skeleton Validation YAML File
-----------------------------

Similar to the configuration skillet, the initial setup includes the new validation directory in an existing cloned
repo or added to a newly created repo in Github. In this directory create placeholder .meta-cnc.yaml and README.md files.

In panHandler under the Skillet Builder collection, run the :ref:`Skillet YAML File Template` skillet. Add in the values
for the skillet ID, label, description, and collection name. Select `validation` as the skillet type.

 .. image:: /images/validation_tutorial/skeleton_yaml_file.png
     :width: 600

Paste the output into the placeholder .meta-cnc.yaml file. The preamble contains the values from the web form. The
key attribute is the type: pan_validation. This defines this as a validation skillet. You can delete the text
under the variables and snippets section.

.. code-block:: yaml

    # skillet preamble information used by panhandler
    # ---------------------------------------------------------------------
    # unique snippet name
    name: validation_tutorial
    # label used for menu selection
    label: validation to test stuff
    description: validation to test - ntp, password complexity, url-filtering to block. malware, and security rules profiles

    # type of device configuration
    # common types are panorama, panos, and template
    # https://github.com/PaloAltoNetworks/panhandler/blob/develop/docs/metadata_configuration.rst
    type: pan_validation
    # preload static or default-based templates
    extends:

    # grouping of like snippets for dynamic menu creation in panhandler
    labels:
      collection:
        - Tutorial


Validation Tests
----------------

The tutorial will step through each validation test including the respective capture output.

Each test will work through the following:

    * review the configuration to see what we will capture and test
    * specify the capture output parameters
    * define the test
    * add messaging and documentation links to each test

As a reminder, a starter XPath needed for each capture can be found using one or more of the techniques
covered in :ref:`Tools to Find the XPath`. In the tutorial I'll use the CLI option with `debug cli on` and
`set cli config-output xml`.

All of the initial testing will be done locally using the test tool without pushing the skillet to Github.
After all of the tests are working we'll push to Github and do final review using the panHandler formatted outputs.

NTP Servers
~~~~~~~~~~~

The first test will check to see if NTP configuration is present. The CLI command to view the NTP configuration is
`show deviceconfig system ntp-servers`.

.. code-block:: bash
    :emphasize-lines: 1, 6, 11-18

    admin@homeSkilletFirewall# show deviceconfig system ntp-servers
    (container-tag: deviceconfig container-tag: system container-tag: ntp-servers)
    ((eol-matched: . #t) (eol-matched: . #t) (xpath-prefix: . /config/devices/entry[@name='localhost.localdomain'])
    (context-inserted-at-end-p: . #f))  /usr/local/bin/pan_ms_client --config-mode=xml --set-prefix='set deviceconfig
    system ' --cookie=5245413957557299 <<'EOF'  |sed 2>/dev/null -e 's/devices localhost.localdomain//'  |/usr/bin/less -X -E -M
    <request cmd="get" obj="/config/devices/entry[@name='localhost.localdomain']/deviceconfig/system/ntp-servers"></request>
    EOF

    <response status="success" code="19">
      <result total-count="1" count="1">
        <ntp-servers>
          <primary-ntp-server>
            <ntp-server-address>0.pool.ntp.org</ntp-server-address>
          </primary-ntp-server>
          <secondary-ntp-server>
            <ntp-server-address>1.pool.ntp.org</ntp-server-address>
          </secondary-ntp-server>
        </ntp-servers>
      </result>
    </response>
    [edit]
    admin@homeSkilletFirewall#

The output shows two key items.

**the XPath after 'obj='**

.. code-block:: bash

    /config/devices/entry[@name='localhost.localdomain']/deviceconfig/system/ntp-servers

**the NTP servers XML element**

.. code-block:: xml

    <ntp-servers>
      <primary-ntp-server>
        <ntp-server-address>0.pool.ntp.org</ntp-server-address>
      </primary-ntp-server>
      <secondary-ntp-server>
        <ntp-server-address>1.pool.ntp.org</ntp-server-address>
      </secondary-ntp-server>
    </ntp-servers>

Since the user can set the server address to any value, the focus will be on the tags. In this case the NTP
configuration exists if the <ntp-server-address> tags are present under the primary and secondary server settings.
This leads to the decision to use the :ref:`tag_present` custom jinja filter with :ref:`capture_object`. The capture
object lets us capture the entire XML element to use in the test.

The first part of the snippet is the capture output, where we'll use capture_object.

.. code-block:: yaml

  - name: device_config_file
    cmd: parse
    variable: config
    outputs:
      - name: ntp_servers
        capture_object: /config/devices/entry[@name='localhost.localdomain']/deviceconfig/system/ntp-servers

Capture output attribute settings. Let's outline each item for the first test.

    * name: contextual name for this capture section
    * cmd: using `parse` to parse the config file
    * variable: set to config to parse the config file as the raw input content
    * outputs: where we can define one or more output variables
    * name: unique variable where the NTP configuration object is stored
    * capture_object: XPath for the NTP configuration

Now with the ntp-servers dict object, we can craft the test and associated messages and links. These are added to the
snippets section of the .meta-cnc.yaml file.

.. code-block:: yaml

    - name: ntp_servers_test
      label: configure primary and secondary ntp servers
      test: |
        (
        ntp_servers | tag_present('primary-ntp-server.ntp-server-address')
        and ntp_servers | tag_present('secondary-ntp-server.ntp-server-address')
        )
      fail_message: |
        time server configuration is reccommended to ensure the firewall clock is in sync with external service and logging
        platforms.
      pass_message: recommended primary and secondary ntp servers are configured
      documentation_link: https://iron-skillet.readthedocs.io/en/docs_dev/viz_guide_panos.html#device-setup-services-services

Test section attribute settings. Let's outline each item as part of the first test.

    * name: unique name for the test
    * label: panHandler test results display line item
    * test: test performed; this example uses `and` to test two items
    * fail_message: what to display if the test fails
    * pass_message: what to display if the test passes
    * documentation link: helper content specific to the test

Let's look at the test attribute in more detail. Everything else should be fairly straightforward.

.. code-block:: yaml

      test: |
        (
        ntp_servers | tag_present('primary-ntp-server.ntp-server-address')
        and ntp_servers | tag_present('secondary-ntp-server.ntp-server-address')
        )

Let's break it down.

  The first mini test uses the ntp_servers capture object as the input. The check is after the pipe '|' using
  a custom filter 'tag_present'. The dot notation is used to step down into the object to primary-ntp-server
  to get to the tag of interest <ntp-server-address>. If this tag is present the test returns `True`.

  The second mini test performs an identical check but looks at the secondary-ntp-server portion of the configuration
  to see if the <ntp-server-address> tag is part of the configuration. If this tag is present the test returns
  `True`.

  In this case we want both servers to be configured so the `and` is used with outer parentheses to combine each
  isolated test into one boolean test output. The test is `True` only if both mini tests return `True`. A `True`
  will display the pass_message and a `False` will output the fail message.

  The pipe after 'test:' is a formatting option to allow for multiline inputs. Common for aggregate tests.

With the capture output and test put together we get the following in the snippets section.

.. code-block:: yaml

      - name: device_config_file
        cmd: parse
        variable: config
        outputs:
          - name: ntp_servers
            capture_object: /config/devices/entry[@name='localhost.localdomain']/deviceconfig/system/ntp-servers

    # check that ntp servers are configured
      - name: ntp_servers_test
        label: configure primary and secondary ntp servers
        test: |
          (
          ntp_servers | tag_present('primary-ntp-server.ntp-server-address')
          and ntp_servers | tag_present('secondary-ntp-server.ntp-server-address')
          )
        fail_message: |
          time server configuration is reccommended to ensure the firewall clock is in sync with external service and logging
          platforms.
        pass_message: recommended primary and secondary ntp servers are configured
        documentation_link: https://iron-skillet.readthedocs.io/en/docs_dev/viz_guide_panos.html#device-setup-services-services

Copy this text to the snippets section of the .meta-cnc.yaml file. Our first test is complete.

Now copy the entire .meta-cnc.yaml text and paste into Skillet Content section of the :ref:`Skillet Test Tool`. You
should have NGFW access in your sandbox and can use `Running Configuration` as the Online Configuration Source.
Click `Submit` to play the skillet.

Look at the output from the first section, 'Execution Results'. This shows what would be sent back to the application
to present the results and is used for debugging purposes.

.. code-block:: json

        {
      "snippets": {
        "ntp_servers_test": true
      },
      "pan_validation": {
        "ntp_servers_test": {
          "results": true,
          "label": "configure primary and secondary ntp servers",
          "severity": "low",
          "documentation_link": "https://iron-skillet.readthedocs.io/en/docs_dev/viz_guide_panos.html#device-setup-services-services",
          "test": "(\nntp_servers | tag_present('primary-ntp-server.ntp-server-address')\nand ntp_servers | tag_present('secondary-ntp-server.ntp-server-address')\n)\n",
          "output_message": "recommended primary and secondary ntp servers are configured"
        }
      }
    }

Under pan_validation.ntp_servers_test you see the results, items read from the YAML file, and an output message
selected based on True or False results.

The second section of the test output is the YAML text. The third section shows all of the variable values.

.. code-block:: json
    :emphasize-lines: 12-19

    hostname = "myFirewall"

    choices = "choices"

    snippets = ""

    device_config_file = {
      "results": "success",
      "changed": false
    }

    ntp_servers = {
      "ntp-servers": {
        "primary-ntp-server": {
          "ntp-server-address": "0.pool.ntp.org"
        },
        "secondary-ntp-server": {
          "ntp-server-address": "1.pool.ntp.org"
        }
      }
    }

    ntp_servers_test = {
      "results": true,
      "label": "configure primary and secondary ntp servers",
      "severity": "low",
      "documentation_link": "https://iron-skillet.readthedocs.io/en/docs_dev/viz_guide_panos.html#device-setup-services-services",
      "test": "(\nntp_servers | tag_present('primary-ntp-server.ntp-server-address')\nand ntp_servers | tag_present('secondary-ntp-server.ntp-server-address')\n)\n",
      "output_message": "recommended primary and secondary ntp servers are configured"
    }

This allows you to see the ntp_servers object content read from the NGFW. In this case the servers are configured.
An empty value is typically the result of an empty NGFW configuration or an incorrect capture_object XPath.
If the test results aren't as expected review the running configuration to make sure it aligns with the context output.

This test looks good so lets move on to the next one.

Password Complexity
~~~~~~~~~~~~~~~~~~~

For this test we'll just cover the highlights. Review the previous NTP servers test for attribute explanations.

This test checks to see if password complexity is enabled and if the minimum password length is >=12.
The CLI command to view the NTP configuration is `show deviceconfig system ntp-servers`.

.. code-block:: bash
    :emphasize-lines: 1, 6, 11-21

    admin@homeSkilletFirewall# show mgt-config password-complexity
    (container-tag: mgt-config container-tag: password-complexity)
    ((eol-matched: . #t) (eol-matched: . #t) (xpath-prefix: . /config) (context-inserted-at-end-p: . #f))
    /usr/local/bin/pan_ms_client --config-mode=xml --set-prefix='set mgt-config ' --cookie=9688686339792135 <<'EOF'
    |sed 2>/dev/null -e 's/devices localhost.localdomain//'  |/usr/bin/less -X -E -M
    <request cmd="get" obj="/config/mgt-config/password-complexity"></request>
    EOF

    <response status="success" code="19">
      <result total-count="1" count="1">
        <password-complexity>
          <enabled>yes</enabled>
          <minimum-length>12</minimum-length>
          <minimum-uppercase-letters>1</minimum-uppercase-letters>
          <minimum-lowercase-letters>1</minimum-lowercase-letters>
          <minimum-numeric-letters>1</minimum-numeric-letters>
          <minimum-special-characters>1</minimum-special-characters>
          <block-username-inclusion>yes</block-username-inclusion>
          <password-history-count>24</password-history-count>
          <new-password-differs-by-characters>3</new-password-differs-by-characters>
        </password-complexity>
      </result>
    </response>
    [edit]
    admin@homeSkilletFirewall#

The output shows two key items.

**the XPath after 'obj='**

.. code-block:: bash

    /config/mgt-config/password-complexity

**the pasword-complexity XML element**

.. code-block:: xml
    :emphasize-lines: 2-3

    <password-complexity>
      <enabled>yes</enabled>
      <minimum-length>12</minimum-length>
      <minimum-uppercase-letters>1</minimum-uppercase-letters>
      <minimum-lowercase-letters>1</minimum-lowercase-letters>
      <minimum-numeric-letters>1</minimum-numeric-letters>
      <minimum-special-characters>1</minimum-special-characters>
      <block-username-inclusion>yes</block-username-inclusion>
      <password-history-count>24</password-history-count>
      <new-password-differs-by-characters>3</new-password-differs-by-characters>
    </password-complexity>

In this example we're explicitly looking for the `enabled` and `minimum-length` settings.
Instead of tags we're focused on the element text values: the 'yes' between the <enabled> tags
and the '12' between the <minimum-length> tags.

Design choices: we could create two unique capture_value outputs for each item with more granular XPaths
but in this case I've opted to test items from a single password-complexity object.
This is useful if I later decide to add more tests for various password-complexity settings.

.. code-block:: yaml
    :emphasize-lines: 7-8

      - name: device_config_file
        cmd: parse
        variable: config
        outputs:
          - name: ntp_servers
            capture_object: /config/devices/entry[@name='localhost.localdomain']/deviceconfig/system/ntp-servers
          - name: password_complexity
            capture_object: /config/mgt-config/password-complexity

In this example I've added the output for password_complexity to the ntp_servers output. This shows how you can
add more captures under one outputs attribute. You could also create a new capture section. We'll do that with
the next test.

Add a new test section. This one is called password_complexity_test and also uses two mini tests to get an aggregate
result. These could optionally be two unique tests with their own test results depending on design choices.

.. code-block:: yaml

     - name: password_complexity_test
        label: configure strong password complexity ( >= 12 chars)
        test: |
          (
          password_complexity | element_value('enabled') == 'yes'
          and password_complexity | element_value('minimum-length') >= '12'
          )
        fail_message: |
          check that password complexity is enabled with a minimum password length of 12 characters
        pass_message: |
          password complexity is enabled with a minimum password length of 12 characters
        documentation_link: https://iron-skillet.readthedocs.io/en/docs_dev/viz_guide_panos.html#device-setup-management-minimum-password-complexity

Let's break it down

  The first test uses element_value and the tag of interest, enabled. Since this is at the top of the captured
  object, no dot notation stepping down the configuration is needed. The expression == yes is used for the test.
  If enabled is 'yes' the test result is True. Otherwise we get a False.

  The second test is similar using the minimum-length tag. This expression checks >= 12 and if the configuration
  setting meets this condition, a True result is returned.

Copy the password-complexity outputs lines and the new test into the .meta-cnc.yaml file. Then copy the full
skillet into the Test Tool and run.

.. NOTE::
    make sure the YAML file alignments are correct or you'll get errors running the skillet.

You'll now see both test results in the output.

.. code-block:: yaml

        {
          "snippets": {
            "ntp_servers": true,
            "password_complexity_test": true
          },
          "pan_validation": {
            "ntp_servers": {
              "results": true,
              "label": "configure primary and secondary ntp servers",
              "severity": "low",
              "documentation_link": "https://iron-skillet.readthedocs.io/en/docs_dev/viz_guide_panos.html#device-setup-services-services",
              "test": "(\nntp_servers | tag_present('primary-ntp-server.ntp-server-address')\nand ntp_servers | tag_present('secondary-ntp-server.ntp-server-address')\n)\n",
              "output_message": "recommended primary and secondary ntp servers are configured"
            },
            "password_complexity_test": {
              "results": true,
              "label": "configure strong password complexity ( >= 12 chars)",
              "severity": "low",
              "documentation_link": "https://iron-skillet.readthedocs.io/en/docs_dev/viz_guide_panos.html#device-setup-management-minimum-password-complexity",
              "test": "(\npassword_complexity | element_value('enabled') == 'yes'\nand password_complexity | element_value('minimum-length') >= '12'\n)\n",
              "output_message": "password complexity is enabled with a minimum password length of 12 characters"
            }
          }
        }

Also review the Full Context section of the output to see the password_complexity captured object.

.. code-block:: yaml

    password_complexity = {
      "password-complexity": {
        "enabled": "yes",
        "minimum-length": "12",
        "minimum-uppercase-letters": "1",
        "minimum-lowercase-letters": "1",
        "minimum-numeric-letters": "1",
        "minimum-special-characters": "1",
        "block-username-inclusion": "yes",
        "password-history-count": "24",
        "new-password-differs-by-characters": "3"
      }
    }

You can modify the NGFW settings and see the changes in the output here. A null value may indicate an empty
running configuration or incorrect XPath for this capture.

This completes the second test.

URL-Filtering and Malware
~~~~~~~~~~~~~~~~~~~~~~~~~

The prior tests were looking at very specific items: primary and secondary NTP settings and password-complexity
configuration. This test however will query across a set of URL-filtering objects, their names unknown. So the logic
is a bit more fuzzy.

The goal is to get a list of all URL-filtering profiles, specifically the names. Then get the names of all profiles
with the category malware explicitly set to block. The difference between the two lists of names are the URL-filtering
profiles that do not have malware set to block. For this test we'll use a built-in :ref:`Jinja Filter` and
:ref:`capture_list` for the output.

The CLI command to view the URL-filtering profile configuration is `show profiles url-filtering`. The output
XML element has been edited to only show the malware category for each profile. Actual output will
be much longer.


.. code-block:: bash
    :emphasize-lines: 1, 8

        admin@homeSkilletFirewall# show profiles url-filtering
        (container-tag: profiles container-tag: url-filtering)
        ((eol-matched: . #t) (eol-matched: . #t) (eol-matched: . #t) (xpath-prefix: .
        /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1'])
        (context-inserted-at-end-p: . #f)) /usr/local/bin/pan_ms_client --config-mode=xml --set-prefix='set profiles
        ' --cookie=2581626760981804 <<'EOF'  |sed 2>/dev/null -e 's/devices localhost.localdomain//'
        |/usr/bin/less -X -E -M <request cmd="get"
        obj="/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles/url-filtering"></request>
        EOF

        <response status="success" code="19">
          <result total-count="1" count="1">
            <url-filtering>
              <entry name="Outbound-URL">
                <block>
                  <member>malware</member>
                </block>
              </entry>
              <entry name="Alert-Only-URL">
                <alert>
                  <member>malware</member>
                </alert>
              </entry>
              <entry name="Exception-URL">
                <block>
                  <member>malware</member>
                </block>
              </entry>
            </url-filtering>
          </result>
        </response>

The output shows two key items.

**the XPath after 'obj='**

.. code-block:: bash

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles/url-filtering

**the URL-filtering XML element**

.. code-block:: xml

        <url-filtering>
          <entry name="Outbound-URL">
            <block>
              <member>malware</member>
            </block>
          </entry>
          <entry name="Alert-Only-URL">
            <alert>
              <member>malware</member>
            </alert>
          </entry>
          <entry name="Exception-URL">
            <block>
              <member>malware</member>
            </block>
          </entry>
        </url-filtering>

In this example we want to capture a list of all profile names. Then we want to create a list of profiles
where <block> <member> includes malware. This requires :ref:`Parsing XML` to capture the lists.

The first step is to put the XPath into the :ref:`Configuration Explorer Tool` and begin to tune the outputs.
With an active connection to the NGFW, use Online mode and enter the XPath into the XPath Query field.
The output will show the XML element, the same output as the CLI show command. The goal is is to make sure we have
a solid starting point.

Now run the query again with `/entry/@name` appended to the XPath. The Execution results will be a list of profile
names.

.. code-block:: json

    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles/url-filtering/entry/@name

    ========================================================================================================================

    xml:
    List of items:


    Outbound-URL
    Alert-Only-URL
    Exception-URL

    =========================================================================================================================

    json:
    [
      "Outbound-URL",
      "Alert-Only-URL",
      "Exception-URL"
    ]

This gets us closer to what we need for testing: a list of all profile names.

While here we also want to create an XPath query that only returns the names with malware set to block. This requires
both a filter to limit the results and then walking back up the tree to get the names. Time to experiment.

Appending the base XPath with '/block' will return all of the <block> config elements. But we don't have the entry
names yet. Then going one level down by adding '/member' will show the member entries.
Now append the output with 'text()' to only see the category names.
This is how we can step through the tree and tune the capture.

Time to filter. Remove '/text()' from the end and instead use in a filter with `[text()='malware']` after member.
The output is now just <member>malware</member> so we've limited to these config elements. But what are the entry names?

.. code-block:: json

    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
    /profiles/url-filtering/entry/block/member[text()='malware']

    =======================================================================================

    xml:
    List of items:

    <member>malware</member>
    <member>malware</member>


The last part of the query is to step back up the tree to the <entry> level and grab the names. This requires
the '..' notation similar to returning up a level in a Linux directory path. Looking back at the XML element
we have to go up two levels: <member> to <block>, <block> to <entry>. So we'll append '/../../' to the
end of the XPath. Since we only want the names, append again with /@name. Yes this is a long XPath query string.

.. code-block:: json

    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/
    profiles/url-filtering/entry/block/member[text()='malware']/../../@name

    ========================================================================================

    xml:
    List of items:

    Outbound-URL
    Exception-URL

So the output we need is based on the XML query above to get the list of profile names with malware = block.
Now that we have the two queries, time to get back to our skillet.

.. code-block:: yaml

  - name: url_profile_test
    cmd: parse
    variable: config
    outputs:

      # get list of url profiles with malware explicitly set to block
      # using this model instead of checking for alert, allow, continue - especially with allow not showing in the config
      - name: url_profiles_block_malware
        capture_list: |-
          /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles/url-filtering/entry
          /block/member[text()='malware']/../../@name

      # get list of all url profiles then filter to profiles not in url_profiles_block_malware
      - name: url_profiles_not_blocking_malware
        capture_list: |-
          /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles/url-filtering/entry/@name
        filter_items: item not in url_profiles_block_malware

For this validation we'll need two outputs. The first, `url_profiles_block_malware` captures the list of all
URL-filtering profiles that have malware as block. The capture_list XPath should look familiar.

The second uses the capture_list for all the profile names. The variable name is `url_profiles_not_blocking_malware`
so we need to filter the full list and exclude items with malware set to block. Here we use `filter_items` to step
through all of the names and if its NOT in the url_profiles_block_malware list, add it to this one. Thus we're
comparing two lists to find the delta. That delta is our list of interest for the test.

The test looks like

.. code-block:: yaml

      - name: check_all_url_profiles_block_malware
        label: check that all url profiles block category malware
        test: url_profiles_not_blocking_malware | length == 0
        severity: high
        fail_message: |
          url profiles not blocking malware: {{ url_profiles_not_blocking_malware }}
        pass_message: |
          all url profiles are currently blocking the category malware
        documentation_link: https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-admin/url-filtering/configure-url-filtering.html#

You'll notice the test is very simple. If the `url_profiles_not_blocking_malware` list has a length == 0 (meaning empty)
then the test passes. If any profiles show up in this list then they don't have malware set to block and cause a test
Fail. We also use the list variable in the fail_message to show what profiles caused the test to fail.

Now copy the capture output and test sections and paste at the bottom of the .meta-cnc.yaml file. This is the third
test. Use the test tool to see the outputs.

.. TIP::
    You can create a scratch skillet file with only the capture and test currently begin developed. This is pasted
    into the test tool and removes any clutter from other tests. Once the test is properly configured you can
    copy back to the master validation YAML file.

The Execution Results show a test fail. This is a good thing since the Alert-Only-URL profile doesn't block malware.
I know this is the bad apple by looking at the output_message line and the profile name is listed.

.. code-block:: json

    {
      "snippets": {
        "check_all_url_profiles_block_malware": false
      },
      "pan_validation": {
        "check_all_url_profiles_block_malware": {
          "results": false,
          "label": "check that all url profiles block category malware",
          "severity": "high",
          "documentation_link": "https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-admin/url-filtering/configure-url-filtering.html#",
          "test": "url_profiles_not_blocking_malware | length == 0",
          "output_message": "url profiles not blocking malware: ['Alert-Only-URL']"
        }
      }
    }

The other data of interest in the Full Context section is the capture values for the two outputs.
Useful for debugging when the results are not as expected.

.. code-block:: json

    url_profiles_block_malware = [
      "Outbound-URL",
      "Exception-URL"
    ]

    url_profiles_not_blocking_malware = [
      "Alert-Only-URL"
    ]

You can see the lists captured for each output entry.

.. TIP::
    If you want to see all of the profile names you can use a capture_list output with the list of names
    exluding any filters. Even without a test association, the list of names will appear in the debug output
    as part of the Full Context.

Proper testing and tuning would include changing the settings in the NGFW and seeing the output results.

Security Rules with Profiles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The last test looks across all 'allow' security rules to see which have a profile or profile-group configured.
Creating this test is similar to the URL-filtering example.

The goal is to get a list of all 'allow' security rules, specifically the names. Then get the names of all rules
with a profile or profile-group. The difference between the two lists of names will gives us the rules of interest,
the allow rules without a profile or group. For this test we'll again use a built-in :ref:`Jinja Filter` and
:ref:`capture_list` for the output.

The CLI command to view the security rules is `show rulebase security rules`. The output
XML element based on HomeSkillet has been edited to only show the name, action, and profile settings.
Actual output will be much longer. The example has also modified the HomeSkillet configuration by
removing the profile settings from the rule HS-non-def-web-ports and using profiles in the rule HS-find-non-def-apps.
These changes help show the different between profiles and groups while giving us a 'bad rule' that will fail
the test.


.. code-block:: bash
    :emphasize-lines: 1, 9

        admin@homeSkilletFirewall# show rulebase security rules
        (container-tag: rulebase container-tag: security container-tag: rules)
        ((eol-matched: . #t) (eol-matched: . #t) (eol-matched: . #t) (xpath-prefix: .
        /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1'])
        (context-inserted-at-end-p: . #f))
        /usr/local/bin/pan_ms_client --config-mode=xml --set-prefix='set rulebase security '
        --cookie=7811212055193400 <<'EOF'  |sed 2>/dev/null -e 's/devices localhost.localdomain//'
        |/usr/bin/less -X -E -M <request cmd="get"
        obj="/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/security/rules"></request>
        EOF

        <response status="success" code="19">
          <result total-count="1" count="1">
            <rules>
              <entry name="Outbound Block Rule">
                <action>deny</action>
              </entry>
              <entry name="Inbound Block Rule">
                <action>deny</action>
              </entry>
              <entry name="DNS Sinkhole Block">
                <action>deny</action>
              </entry>
              <entry name="HS-block-quic">
                <action>deny</action>
              </entry>
              <entry name="HS-no-unknown-URL-xfer">
                <profile-setting>
                  <group>
                    <member>Outbound-Unknown-URL</member>
                  </group>
                </profile-setting>
                <action>allow</action>
              </entry>
              <entry name="HS-allow-outbound">
                <action>allow</action>
                <profile-setting>
                  <group>
                    <member>Outbound</member>
                  </group>
                </profile-setting>
              </entry>
              <entry name="HS-non-def-SSL-ports">
                <action>allow</action>
                <profile-setting>
                  <group>
                    <member>Outbound</member>
                  </group>
                </profile-setting>
              </entry>
              <entry name="HS-non-def-web-ports">
                <action>allow</action>
              </entry>
              <entry name="HS-find-non-def-apps">
                <action>allow</action>
                <profile-setting>
                    <profiles>
                      <virus>
                        <member>Outbound-AV</member>
                      </virus>
                      <vulnerability>
                        <member>Outbound-VP</member>
                      </vulnerability>
                    </profiles>
                </profile-setting>
              </entry>
            </rules>
          </result>
        </response>
        [edit]
        admin@homeSkilletFirewall#

The output shows two key items.

**the XPath after 'obj='**

.. code-block:: bash

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/security/rules

**the Security Rule XML element**

.. code-block:: xml

        <rules>
          <entry name="Outbound Block Rule">
            <action>deny</action>
          </entry>
          <entry name="Inbound Block Rule">
            <action>deny</action>
          </entry>
          <entry name="DNS Sinkhole Block">
            <action>deny</action>
          </entry>
          <entry name="HS-block-quic">
            <action>deny</action>
          </entry>
          <entry name="HS-no-unknown-URL-xfer">
            <profile-setting>
              <group>
                <member>Outbound-Unknown-URL</member>
              </group>
            </profile-setting>
            <action>allow</action>
          </entry>
          <entry name="HS-allow-outbound">
            <action>allow</action>
            <profile-setting>
              <group>
                <member>Outbound</member>
              </group>
            </profile-setting>
          </entry>
          <entry name="HS-non-def-SSL-ports">
            <action>allow</action>
            <profile-setting>
              <group>
                <member>Outbound</member>
              </group>
            </profile-setting>
          </entry>
          <entry name="HS-non-def-web-ports">
            <action>allow</action>
          </entry>
          <entry name="HS-find-non-def-apps">
            <action>allow</action>
            <profile-setting>
                <profiles>
                  <virus>
                    <member>Outbound-AV</member>
                  </virus>
                  <vulnerability>
                    <member>Outbound-VP</member>
                  </vulnerability>
                </profiles>
            </profile-setting>
          </entry>
        </rules>

In this example we want to capture a list of all action=allow rule names. Then we want to create a list of rules
where <profile-setting> is present. Then we'll compare these two lists.
This requires :ref:`Parsing XML` to capture the lists.

The first step is to put the XPath into the :ref:`Configuration Explorer Tool` and begin to tune the outputs.
With an active connection to the NGFW, use Online mode and enter the XPath into the XPath Query field.
The output will show the XML element same output as the CLI show command. The goal is is to make sure we have
a solid starting point.

Now run the query again with `/entry/@name` appended to the XPath. The Execution results will be a list of all
security rules names.

.. code-block:: json

    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
    /rulebase/security/rules/entry/@name

    ======================================================================================

    xml:
    List of items:


    Outbound Block Rule
    Inbound Block Rule
    DNS Sinkhole Block
    HS-block-quic
    HS-no-unknown-URL-xfer
    HS-allow-outbound
    HS-non-def-SSL-ports
    HS-non-def-web-ports
    HS-find-non-def-apps

This is all of the rules but first we only want the allow rules.

For the action=allow we'll look one down level by removing '/@name' and adding '/action' to the XPath.
The output is a list of <action> elements, a mix of deny and allow.

.. code-block:: json

    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
    /rulebase/security/rules/entry/action

    =====================================================================================

    xml:
    List of items:

    <action>deny</action>
    <action>deny</action>
    <action>deny</action>
    <action>deny</action>
    <action>allow</action>
    <action>allow</action>
    <action>allow</action>
    <action>allow</action>
    <action>allow</action>

Next we filter to only capture the 'allow' elements by appending action with `[text()='allow']`

.. code-block:: json

    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
    /rulebase/security/rules/entry/action[text()='allow']

    =====================================================================================

    xml:
    List of items:

    <action>allow</action>
    <action>allow</action>
    <action>allow</action>
    <action>allow</action>
    <action>allow</action>

So at this stage we're only grabbing allow elements but we need their entry names. Next we walk back up the tree
one level with a `/../` and append the query with `@name` to only return the names.

.. code-block:: json

    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
    /rulebase/security/rules/entry/action[text()='allow']/../@name

    =====================================================================================

    xml:
    List of items:

    HS-no-unknown-URL-xfer
    HS-allow-outbound
    HS-non-def-SSL-ports
    HS-non-def-web-ports
    HS-find-non-def-apps

We now have the XPath query to use as one part of our capture output.

The second list isn't looking for names or specific values but checking if the <profile-setting> tag is present.
This tag only appears in the configuration if a profile or group exists.

.. code-block:: json

    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
    /rulebase/security/rules/entry/profile-setting

    ======================================================================================

    xml:
    List of items:

    <profile-setting>
      <group>
        <member>Outbound-Unknown-URL</member>
      </group>
    </profile-setting>

    <profile-setting>
      <group>
        <member>Outbound</member>
      </group>
    </profile-setting>

    <profile-setting>
      <group>
        <member>Outbound</member>
      </group>
    </profile-setting>

    <profile-setting>
      <profiles>
        <virus>
          <member>Outbound-AV</member>
        </virus>
        <vulnerability>
          <member>Outbound-VP</member>
        </vulnerability>
      </profiles>
    </profile-setting>

Close but we want the names of the rules with the profile-settings. To get this we'll use `/../` to come up a level
from <profile-setting> to <entry> and then output the entry names by appending `@name` to the XPath.

.. code-block:: json

    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
    /rulebase/security/rules/entry/profile-setting/../@name

    =====================================================================================

    xml:
    List of items:

    HS-no-unknown-URL-xfer
    HS-allow-outbound
    HS-non-def-SSL-ports
    HS-find-non-def-apps

This output is all of the security rules with a profile-setting. Now we have the XPath query to use in the
capture output for the profile-setting rules.

Now that we have both queries, time to get back to our skillet.

.. code-block:: yaml

     # test that all allow security policies have profile-settings configured
      - name: security_policy_test
        cmd: parse
        variable: config
        outputs:
          # get a list of security policies with a profile or group configured
          - name: security_policies_with_profile_or_group
            capture_list: |-
              /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
              /rulebase/security/rules/entry/profile-setting/../@name

          # get a list of security policies with action allow
          - name: allow_security_policies_without_profile
            capture_list: |-
              /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']
              /rulebase/security/rules/entry/action[text()='allow']/../@name
            filter_items: item not in security_policies_with_profile_or_group

For this validation we'll need two outputs. The first, `security_policies_with_profile_or_group` captures the list of all
security policies with a profile setting.

The second uses the capture_list for all of the allow security rules. The variable name is
`allow_security_policies_without_profile` so we need to filter the full list of rules down to the items
that are not in the `security_policies_with_profile_or_group` list. The delta is our list of interest showing
which allow rules don't have a profile setting.

The test looks like

.. code-block:: yaml

    # check that all allow security policies have a profile or group
      - name: check_allow_security_policies_have_profile
        label: check that all allow security policies have a profile or group
        test: allow_security_policies_without_profile | length == 0
        severity: medium
        fail_message: |
          allow security policies without a profile or group: {{ allow_security_policies_without_profile }}
        pass_message: |
          all allow security policies have a profile or group configured
        documentation_link: https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-admin/policy/security-profiles/create-a-security-profile-group.html

You'll notice the test is very simple. If the `allow_security_policies_without_profile` list has a length == 0 (meaning empty)
then the test passes. If any rules show up in this list then they don't have a profile-setting and cause a test
Fail. We also use the list variable in the fail_message to show what rules caused the test to fail.

Now copy the capture output and test sections and paste at the bottom of the .meta-cnc.yaml file. This is the final
test. Now use the test tool to see the outputs.

The Execution Results show a test fail. This is a good thing since the HS-non-def-web-ports rule doesn't have a
profile setting.
I know this is the bad apple by looking at the output_message line and the security rule name is listed.

.. code-block:: json

    {
      "snippets": {
        "check_allow_security_policies_have_profile": false
      },
      "pan_validation": {
        "check_allow_security_policies_have_profile": {
          "results": false,
          "label": "check that all allow security policies have a profile or group",
          "severity": "medium",
          "documentation_link": "https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-admin/policy/security-profiles/create-a-security-profile-group.html",
          "test": "allow_security_policies_without_profile | length == 0",
          "output_message": "allow security policies without a profile or group: ['HS-non-def-web-ports']"
        }
      }
    }

The other data of interest is the capture values for the two outputs. Useful for debugging when the results
are not as expected.

.. code-block:: json

    security_policies_with_profile_or_group = [
      "HS-no-unknown-URL-xfer",
      "HS-allow-outbound",
      "HS-non-def-SSL-ports",
      "HS-find-non-def-apps"
    ]

    allow_security_policies_without_profile = [
      "HS-non-def-web-ports"
    ]

You can see the lists captured for each output entry.

Proper testing and tuning would include changing the settings in the NGFW and viewing the output results.

Push to Github and Test in panHandler
-------------------------------------

Now the .meta-cnc.yaml file has the four tests ready to go. Push the skillet to Github and import into panHandler.
Run the skillet to view results.

   .. image:: /images/validation_tutorial/validation_output.png
       :width: 800

  * review label text, results, and documentation links
  * expand labels and review the pass/fail messages

.. Note::
    The Severity settings are optional and added into the tests for demonstration. Severity can be used
    in the tests or left as the default 'low'.

Edit the README.md Docs
-----------------------

The final step as with any skillet is to add the :ref:`Documentation` in the skillet REAMD.md file.


