Validation
==========

Overview
--------

This tutorial walks through the creation and testing of a validation skillet that will:

  * Check if NTP servers are configured
  * Check is password complexity is enabled with a minimum-length >= 12 characters
  * Check if all configured URL-filtering profiles are blocking the malware category
  * Check if all 'allow' security rules are configured with a security profile or group

Unlike configuration skillets that can easy start with the difference between two configuration files, validation
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
---------------------------

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
                  /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/security/rules/entry
                  //profile-setting//member/../../../@name

              # get a list of security policies with action allow
              - name: allow_security_policies_without_profile
                capture_list: |-
                  /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/security/rules/entry
                  /action[text()='allow']/../@name
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

Paste the output into the placeholder .meta-cnc.yaml file. The preamble contains the values from the web form. They
key attributed is the type: pan_validation. This defines this as a validation skillet.

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


NTP Server Test
---------------


