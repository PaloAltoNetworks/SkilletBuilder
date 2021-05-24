Workflow
=============

Overview
--------

    This tutorial is aimed at novice skillet developers who want to build a sample workflow skillet.
    Workflows are a simple way to tie together multiple skillets into one chain of execution.
    This solution type is preferred in these specific use cases:

      * Joining together skillets of multiple types
      * Breaking the automation into many steps with human input in the middle

    This workflow tutorial considers both of these use cases when developing a solution
    that chains a **validation** skillet, a **configuration** skillet, and a **template** skillet into
    one cohesive workflow solution.


    Click below to jump to a specific section of the tutorial:
      1. `Prerequisites`_
      2. `Design the Solution`_
      3. `Build the Skillet`_
      4. `Test and Troubleshoot`_
      5. `Document`_

|

Prerequisites
-------------

    Before moving forward with the tutorial, you will need to do the following:

        1. Create a GitHub repository, instructions here
        2. Open your repository in a text editor or IDE, instructions here
        3. Install PanHandler using Docker, instructions here
        4. Install SLI using a Python virtual environment, instructions here
        5. Deploy a Next Generation Firewall for testing, instructions here

|

Design the Solution
-------------------

    Designing the execution flow of a workflow skillet is one of the most important aspect of its
    development.

    From a high level, workflow skillets begin execution by prompting the user for input, which get
    saved as variables. Once the user finishes with the prompted workflow menu, each workflow sub-skillet
    gets executed in a defined sequence. This sequence can be static, or it can conditionally
    change depending on the user's input.

    As a result, when designing a workflow, you must think about:

      * Overall sequence of sub-skillets
      * Conditional execution of each sub-skillet
      * User-facing menu options

Design this Tutorial's Solution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    The sequence of this tutorial's workflow solution is described in the image below.

      .. image:: /images/workflow_tutorial/workflow_sequence.png
         :width: 800

    In this tutorial, you will walk through the steps to create the main workflow skillet.
    It is assumed that the individual sub-skillets that the workflow calls are previously developed.
    You can use developed skillets from the `Quickplay Solution's LIVEcommunity page`_; you can use
    GitHub submodules to incorporate developed skillets; or you can develop your own skillets.
    For information on developing other skillet types, please look through the tutorials under
    the **Tutorials** section.

    .. _Quickplay Solution's LIVEcommunity page: https://live.paloaltonetworks.com/t5/quickplay-solutions/ct-p/Quickplay_Solutions

      .. NOTE::
            You can **NOT** call a workflow skillet inside of a workflow skillet.

    The last design decision for this workflow solution is the user-facing workflow menu options.
    Since the automation will be accessing a Next Generation Firewall (NGFW), it will need access credentials.
    In addition, the solution will need configuration details specific to the configuration skillet. Lastly,
    it will need to know when the user wants the validation skillets run.

    With this information, we can outline what the menu options should look like:

      .. image:: /images/workflow_tutorial/workflow_menu.png
         :width: 800

|

Build the Skillet
--------------------

    The following steps take the user from creating the GitHub repo, through generating and editing the main skillet,
    to a final push of the main skillet content back to the created repo.

Set-up the Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  In your text editor/IDE of choice, open the repository's root directory, and add a subdirectory/folder, which
  will contain all of the skillet contents (eg. edl_xml_policy_workflow). Inside of this newly created folder,
  add the following files:

    * An empty ``workflow_tutorial.skillet.yaml`` file for the main workflow skillet contents (to be populated later)
    * An empty ``README.md`` file (to be populate later)
    * ``config_xml_edl_policy.skillet.yaml`` file with the configuration sub-skillet contents

          .. toggle-header:: class
              :header: **Show/Hide the configuration skillet contents**

              .. code-block:: yaml

                # skillet preamble information used by panhandler
                # ---------------------------------------------------------------------
                # unique snippet name
                name: config_xml_edl_policy
                # label used for menu selection
                label: Sample SkilletBuilder skillet with EDL, tag, and security policy
                description: Used by SkilletBuilder to demonstrate skillet creation and loading and cross-element variables

                # type of device configuration
                # common types are panorama, panos, and template
                type: panos

                # grouping of like snippets for dynamic menu creation in panhandler
                labels:
                  collection:
                    - Skillet Builder

                # ---------------------------------------------------------------------
                # end of preamble section

                # variables section
                # ---------------------------------------------------------------------
                # variables used in the configuration templates
                # type_hint defines the form field used by panhandler
                # type_hints examples include text, ip_address, or dropdown
                variables:
                  # variables used for connection with NGFW; type_hint of hidden since
                  # the values are cached in the context after the workflow skillet
                  - name: TARGET_IP
                    description: NGFW IP or Hostname
                    default: 192.168.55.10
                    type_hint: hidden
                  - name: TARGET_USERNAME
                    description: NGFW Username
                    default: admin
                    type_hint: hidden
                  - name: TARGET_PASSWORD
                    description: NGFW Password
                    default: admin
                    type_hint: hidden

                  - name: edl_name
                    description: name of the external list
                    default: my_edl
                    type_hint: text
                  - name: edl_description
                    description: description of the external list
                    default: this is an ip block list
                    type_hint: text
                  - name: edl_url
                    description: external list url
                    default: http://someurl.com
                    type_hint: text
                  - name: tag_name
                    description: tag name
                    default: tag name
                    type_hint: text
                  - name: tag_description
                    description: tag description
                    default: tag description
                    type_hint: text
                  - name: tag_color
                    description: tag color
                    default: red
                    type_hint: dropdown
                    dd_list:
                      - key: blue
                        value: color3
                      - key: green
                        value: color2
                      - key: orange
                        value: color6
                      - key: red
                        value: color1

                # ---------------------------------------------------------------------
                # end of variables section

                # snippets section
                # ---------------------------------------------------------------------
                # snippets used for api configuration including xpath and element as file name
                # files will load in the order listed
                snippets:
                  - name: object_tag
                    xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag
                    element: |-
                        <entry name="{{ tag_name }}">
                          <color>{{ tag_color }}</color>
                          <comments>{{ tag_description }}</comments>
                        </entry>

                  - name: object_edl
                    xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]
                    element: |-
                        <external-list>
                          <entry name="{{ edl_name }}">
                            <type>
                              <ip>
                                <recurring>
                                  <five-minute/>
                                </recurring>
                                <description>{{ edl_desc }}</description>
                                <url>{{ edl_url }}</url>
                              </ip>
                            </type>
                          </entry>
                        </external-list>

                  - name: policy_security_outbound
                    xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/rulebase/security/rules
                    element: |-
                        <entry name="{{ edl_name }}-out">
                          <to>
                            <member>any</member>
                          </to>
                          <from>
                            <member>any</member>
                          </from>
                          <source>
                            <member>any</member>
                          </source>
                          <destination>
                            <member>{{ edl_name }}</member>
                          </destination>
                          <source-user>
                            <member>any</member>
                          </source-user>
                          <category>
                            <member>any</member>
                          </category>
                          <application>
                            <member>any</member>
                          </application>
                          <service>
                            <member>application-default</member>
                          </service>
                          <hip-profiles>
                            <member>any</member>
                          </hip-profiles>
                          <tag>
                            <member>{{ tag_name }}</member>
                          </tag>
                          <action>deny</action>
                          <description>outbound EDL IP block rule. EDL info: {{ edl_desc }}</description>
                        </entry>

                  - name: security_policy_inbound
                    xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/rulebase/security/rules
                    element: |-
                        <entry name="{{ edl_name }}-in">
                          <to>
                            <member>any</member>
                          </to>
                          <from>
                            <member>any</member>
                          </from>
                          <source>
                            <member>{{ edl_name }}</member>
                          </source>
                          <destination>
                            <member>any</member>
                          </destination>
                          <source-user>
                            <member>any</member>
                          </source-user>
                          <category>
                            <member>any</member>
                          </category>
                          <application>
                            <member>any</member>
                          </application>
                          <service>
                            <member>application-default</member>
                          </service>
                          <hip-profiles>
                            <member>any</member>
                          </hip-profiles>
                          <tag>
                            <member>{{ tag_name }}</member>
                          </tag>
                          <action>deny</action>
                          <description>inbound EDL IP block rule. EDL info: {{ edl_desc }}</description>
                        </entry>

    * ``validate_xml_edl_policy.skillet.yaml`` file with the validation sub-skillet contents

          .. toggle-header:: class
              :header: **Show/Hide the validation skillet contents**

              .. code-block:: yaml

                # skillet preamble information used by panhandler
                # ---------------------------------------------------------------------
                # unique snippet name
                name: validate_xml_edl_policy
                # label used for menu selection
                label: Sample SkilletBuilder validation for EDL, tag, and security policy
                description: |
                  Used by SkilletBuilder to demonstrate configuration capturing and validation skillet creation.

                # type of device configuration
                # common types are panorama, panos, and template
                # https://github.com/PaloAltoNetworks/panhandler/blob/develop/docs/metadata_configuration.rst
                type: pan_validation

                # grouping of like snippets for dynamic menu creation in panhandler
                labels:
                  collection:
                    - Skillet Builder

                # ---------------------------------------------------------------------
                # end of preamble section

                # variables section
                # ---------------------------------------------------------------------
                # variables used in the configuration templates
                # type_hint defines the form field used by panhandler
                # type_hints examples include text, ip_address, or dropdown
                variables:
                  # variables used for connection with NGFW; type_hint of hidden since
                  # the values are cached in the context after the workflow skillet
                  - name: TARGET_IP
                    description: NGFW IP or Hostname
                    default: 192.168.55.10
                    type_hint: hidden
                  - name: TARGET_USERNAME
                    description: NGFW Username
                    default: admin
                    type_hint: hidden
                  - name: TARGET_PASSWORD
                    description: NGFW Password
                    default: admin
                    type_hint: hidden

                  - name: edl_url
                    description: External Dynamic List URL
                    default: http://someurl.com
                    type_hint: hidden

                # ---------------------------------------------------------------------
                # end of variables section

                # snippets section
                # ---------------------------------------------------------------------
                snippets:
                    # Capture the name of the IP External Dynamic Lists with URL set to user-inputted edl_url
                  - name: capture_external_lists
                    cmd: parse
                    variable: config
                    outputs:
                      - name: external_lists
                        capture_object: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/external-list
                      - name: user_edl_name
                        capture_value: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/external-list/entry/type/ip/url[text()="{{ edl_url }}"]/../../../@name

                    # Verify that the captured name isn't null, meaning an EDL is configured
                  - name: test_external_lists
                    label: configure IP External Dynamic List (EDL) object
                    test: |
                      (
                       user_edl_name | length
                      )
                    fail_message: |
                      There are no External Dynamic Lists (EDL) configured on this firewall for {{ edl_url }}.
                    pass_message: |
                      The External Dynamic List (EDL), {{ user_edl_name }}, is configured for {{ edl_url }}.
                    documentation_link: https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-web-interface-help/objects/objects-external-dynamic-lists

                    # Capture the name of security rules that deny from source/destination EDL
                  - name: capture_security_rules
                    cmd: parse
                    variable: config
                    outputs:
                      - name: security_rules_with_EDL_source
                        capture_list: /config/devices/entry/vsys/entry/rulebase/security/rules/entry[source/member/text()="{{ user_edl_name }}"][action/text()="deny"]/@name
                      - name: security_rules_with_EDL_destination
                        capture_list: /config/devices/entry/vsys/entry/rulebase/security/rules/entry[destination/member/text()="{{ user_edl_name }}"][action/text()="deny"]/@name

                    # Verify that the captured list isn't null, meaning security rules are configured
                  - name: test_security_rules_out
                    label: configure security rule blocking traffic to EDL object
                    test: |
                      (
                       security_rules_with_EDL_destination | length
                      )
                    fail_message: |
                      There are no security rules denying traffic to the destination of External Dynamic Lists (EDL) object.
                    pass_message: At least one security rule with EDL destination is configured.
                    documentation_link: https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-admin/policy/use-an-external-dynamic-list-in-policy/enforce-policy-on-an-external-dynamic-list.html
                  - name: test_security_rules_in
                    label: configure security rule blocking traffic from EDL oject
                    test: |
                      (
                       security_rules_with_EDL_source | length
                      )
                    fail_message: |
                      There are no security rules denying traffic from the source of External Dynamic Lists (EDL) object.
                    pass_message: At least one security rule with EDL source is configured.
                    documentation_link: https://docs.paloaltonetworks.com/pan-os/10-0/pan-os-admin/policy/use-an-external-dynamic-list-in-policy/enforce-policy-on-an-external-dynamic-list.html

                # ---------------------------------------------------------------------
                # end of snippets section


    * ``template_xml_edl_policy.skillet.yaml`` file with the template sub-skillet contents

          .. toggle-header:: class
              :header: **Show/Hide the template skillet contents**

              .. code-block:: yaml

                # skillet preamble information used by panhandler
                # ---------------------------------------------------------------------
                # unique snippet name
                name: template_xml_edl_policy
                # label used for menu selection
                label: Sample template skillet used for workflow tutorial
                description: Used by SkilletBuilder to demonstrate workflow completion output messaging.

                # type of device configuration
                # common types are panorama, panos, and template
                # https://github.com/PaloAltoNetworks/panhandler/blob/develop/docs/metadata_configuration.rst
                type: template

                # grouping of like snippets for dynamic menu creation in panhandler
                labels:
                  collection:
                    - Skillet Builder

                # ---------------------------------------------------------------------
                # end of preamble section

                # variables section
                # ---------------------------------------------------------------------
                # variables used in the configuration templates
                # type_hint defines the form field used by panhandler
                # type_hints examples include text, ip_address, or dropdown
                variables:
                  # type_hint of hidden since the values are cached in the context
                  # after the workflow skillet
                  - name: TARGET_IP
                    description: NGFW IP or Hostname
                    default: 192.168.55.10
                    type_hint: hidden
                  - name: edl_name
                    description: name of the external list
                    default: my_edl
                    type_hint: hidden
                  - name: tag_name
                    description: tag name
                    default: tag name
                    type_hint: hidden

                # ---------------------------------------------------------------------
                # end of variables section

                # snippets section
                # ---------------------------------------------------------------------
                snippets:
                # contextual name with the name of the template file
                  - name: output_message
                    file: template_output_report.j2

                # ---------------------------------------------------------------------
                # end of snippets section



    * ``template_output_report.j2`` file with the template HTML output contents

          .. toggle-header:: class
              :header: **Show/Hide the template HTML output contents**

              .. code-block:: html

                <div>
                <br/>
                <h2 style="text-align:center;">WORKFLOW COMPLETED</h2>
                <br/>
                The External Dynamic List, named <i>{{ edl_name }}</i>, was added to
                the configuration of the NGFW ({{ TARGET_IP }}). In addition, security policies with the tag <i>{{ tag_name }}</i>
                were configured to deny traffic to and from this EDL.
                <br/>
                <br/>
                For a step-by-step tutorial on building workflows, please navigate to the <a href="">Workflow Tutorial</a>
                in the SkilletBuilder documentation.
                </div>


  The directory structure will look like:

      .. image:: /images/workflow_tutorial/workflow_directory_structure.png
         :width: 250


Create the Workflow Skillet Skeleton
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    In your PanHandler Web GUI, navigate to *PanHandler* dropdown menu in the top left
    of the page, and click on **Skillet Collections**.

        .. image:: /images/workflow_tutorial/panhandler_dropdown.png
         :width: 250

    Scroll down the *Skillet Collections* page until you find the *Skillet Builder* tile,
    and click **Go**.

        .. image:: /images/workflow_tutorial/skillet_builder_tile.png
         :width: 250

    Scroll down the *Skillet Builder Collections* page until you find the
    *Skillet YAML File Template* tile, and click **Go**.

        .. image:: /images/workflow_tutorial/skillet_yaml_file_template.png
         :width: 250

    The :ref:`Skillet YAML File Template` provides an easy user interface for building the skillet structure
    and populating the :ref:`Preamble Attributes`.

        .. image:: /images/workflow_tutorial/workflow_skeleton_template.png
         :width: 800

    Here are the suggested tutorial inputs:

        * **Skillet ID**: workflow_xml_edl_policy
        * **Skillet Label**: Sample SkilletBuilder workflow for EDL validation and configuration
        * **Skillet Description**: Used by SkilletBuilder to demonstrate chaining skillets together as workflow solutions.
        * **Collection Name**: Skillet Builder
        * **Skillet Type**: ``workflow``

    Click **Submit** to view the rendered template. This YAML file template contains:

        1. Preamble populated with the web form values
        2. Variables section with placeholder values
        3. Snippets section with placeholder values

    Copy this template and paste it into the ``workflow_tutorial.skillet.yaml`` file in your repository's
    ``edl_xml_policy_workflow`` folder. Since the variables and snippets sections are populated with filler,
    you can delete these sections to get the main workflow skillet's skeleton.

          .. toggle-header:: class
              :header: **Show/Hide the workflow skillet skeleton**

              .. code-block:: yaml

                # skillet preamble information used by panhandler
                # ---------------------------------------------------------------------
                # unique snippet name
                name: workflow_xml_edl_policy
                # label used for menu selection
                label: Sample SkilletBuilder workflow for EDL validation and configuration
                description: Used by SkilletBuilder to demonstrate chaining skillets together as workflow solutions.

                # type of device configuration
                # common types are panorama, panos, and template
                # https://github.com/PaloAltoNetworks/panhandler/blob/develop/docs/metadata_configuration.rst
                type: workflow

                # grouping of like snippets for dynamic menu creation in panhandler
                labels:
                  collection:
                    - Skillet Builder

                # ---------------------------------------------------------------------
                # end of preamble section

                # variables section
                # ---------------------------------------------------------------------
                # variables used in the configuration templates
                # type_hint defines the form field used by panhandler
                # type_hints examples include text, ip_address, or dropdown
                variables:


                # ---------------------------------------------------------------------
                # end of variables section

                # snippets section
                # ---------------------------------------------------------------------
                snippets:


                # ---------------------------------------------------------------------
                # end of snippets section



Add Variables to the Skillet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Similar to other skillet types, workflow skillets utilize :ref:`Variables` in the variables section
    to prompt the user for input, which gets checked for proper formatting, and to vary the automation
    workflow (in an expected way) to handle many use cases.

    In workflow skillets, users can be prompted for input in two main situations:

        1. On the beginning workflow menu, defined in the main workflow's YAML file
        2. In the middle of the workflow, defined in a sub-skillet's YAML file

    Variables defined in the main workflow YAML file are saved to context and can be used by all of the
    following sub-skillets. This option is useful for variables that are already known to the user going into
    the automation and that do not depend on a sub-skillet's execution. For example, each sub-skillet in
    the tutorial workflow needs to know the firewall's access credentials, which will not change during
    the workflow execution, so defining the IP, username, and password in the main workflow menu minimizes
    and streamlines user input.

    Add the following YAML code to the **variables** section of the ``workflow_tutorial.skillet.yaml``
    file:

    .. code-block:: yaml

            # variables section
        # ---------------------------------------------------------------------
        # variables used in the configuration templates
        # type_hint defines the form field used by panhandler
        # type_hints examples include text, ip_address, or dropdown
        variables:
          - name: TARGET_IP
            description: NGFW IP or Hostname
            default: 192.168.55.10
            type_hint: fqdn_or_ip
          - name: TARGET_USERNAME
            description: NGFW Username
            default: admin
            type_hint: text
          - name: TARGET_PASSWORD
            description: NGFW Password
            default: admin
            type_hint: password

          - name: edl_url
            description: External Dynamic List's Source URL
            default: http://someurl.com
            type_hint: text

          - name: assess_options
            description: Config Validation Options
            default: []
            type_hint: checkbox
            cbx_list:
              - key: Validate configuration at the beginning of the workflow
                value: run_validation_begin
              - key: Validate configuration at the end of the workflow
                value: run_validation_end


        # ---------------------------------------------------------------------
        # end of variables section

    .. NOTE::
        When you move variables to the front of the workflow, you **MUST** still include the necessary
        variables in each individual sub-skillet.

        A sub-skillet will only ever see the variables defined in its variables list, even if that variable
        is loaded into the context.

    In order to minimize the amount of user interaction, you will need to change the variables'
    **type_hint** in each sub-skillet's variables section to *hidden*. This will load the variable
    from context for the sub-skillet to use and will not prompt a user to re-define it.

    The validation skillet's **variables** section is then changed to:

    .. code-block:: yaml

        variables:
          # variables used for connection with NGFW; type_hint of hidden since
          # the values are cached in the context after the workflow skillet
          - name: TARGET_IP
            description: NGFW IP or Hostname
            default: 192.168.55.10
            type_hint: hidden
          - name: TARGET_USERNAME
            description: NGFW Username
            default: admin
            type_hint: hidden
          - name: TARGET_PASSWORD
            description: NGFW Password
            default: admin
            type_hint: hidden

          - name: edl_url
            description: External Dynamic List URL
            default: http://someurl.com
            type_hint: hidden

        # ---------------------------------------------------------------------
        # end of variables section

    .. TIP::
        YAML is notoriously finicky about whitespace and formatting. While it's a relatively
        simple structure and easy to learn, it can often also be frustrating to work with.
        A good reference to use to check your YAML syntax is the
        `YAML Lint site <http://www.yamllint.com/>`_.

    A common problem with developing workflow skillets is variable name matching across all the
    skillets. You must make sure that a variable's name matches from skillet to skillet. If they do
    not match and you don't have the ability to change the names (This could happen if you don't own the sub-skillets),
    you can use a **transform** attribute in the snippets section to map one sub-skillet's output variable
    to another sub-skillet's input variable. For examples of this attribute in a workflow, navigate to
    the `SkilletLib repo in GitHub`_.

Add Snippets to the Skillet
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    For main workflow skillets, each *snippet* in the **snippets** section is the name of a
    skillet to be executed in turn. You can find the unique name of each sub-skillet by
    opening the sub-skillet's YAML file and locating the **name** attribute in the preamble
    section. Each of the sub-skillet's names have to be globally unique for the main workflow skillet to
    understand which sub-skillet to execute.

    Conditional execution of a sub-skillet is accomplished by using the **when** attribute
    underneath the sub-skillet's name in question. That snippet will only run
    when the conditional logic defined with the :ref:`when` attribute evaluates as True.

    For this tutorial, if the user decides to validate at both the beginning and end of the workflow,
    the sequence of execution is validate, config, validate, and then output a message.
    As seen in the main workflow skillet's snippet section below, this sequence was achieved by
    the intentional ordering of snippet names.

    In order to take the user's input into account regarding the validation ordering,
    **when** attributes are placed after each validation snippet and defined with the logical
    statement of ``"'run_validation_begin' in assess_options"``. This evaluates to when the
    ``assess_options`` checkbox's list item with the *value* ``run_validation_beginning`` is
    checked, run the snippet.

    Add the following YAML code to the **snippets** section of the ``workflow_tutorial.skillet.yaml``
    file:

    .. code-block:: yaml

        # snippets section
        # ---------------------------------------------------------------------
        snippets:
            # Run the validation skillet if the user checks the checkbox
          - name: validate_xml_edl_policy
            when: "'run_validation_begin' in assess_options"

          - name: config_xml_edl_policy

            # Run the validation skillet if the user checks the checkbox
          - name: validate_xml_edl_policy
            when: "'run_validation_end' in assess_options"

            # Finish with output message of completion to the user
          - name: template_xml_edl_policy
        # ---------------------------------------------------------------------
        # end of snippets section

    In addition to **when** attributes, the only other attribute used in the snippet section
    of workflow skillets is **transform**.  You may optionally also include a **transform**
    attribute, which will map the output from one sub-skillet to the input of another. For an
    example of a workflow skillet using transform, navigate to the `SkilletLib repo in GitHub`_.

    .. _SkilletLib repo in GitHub: https://github.com/PaloAltoNetworks/skilletlib/tree/master/example_skillets/workflow_transform

    .. NOTE::
        **REMEMBER**: To avoid PanHandler skillet import errors, skillets' names must be globally unique.

Push the Skillet to GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~

    At this stage initial building is complete. The YAML file preamble, variables, and snippets sections all have
    relevant content added. Now we want to push this to GitHub for additional testing and tuning.

    Use:

    * ``git add .`` to add the modified files to the commit
    * ``git commit -m "message"`` to commit the files with a change message
    * ``git push origin master`` to push to the repo master branch

|

Test and Troubleshoot
---------------------

    Now that the skillet has been pushed to GitHub, the skillet can be imported or loaded into one of the skillet
    player tools, such as PanHandler or SLI, for testing. Similar to designing, testing involves three main
    components:

        1. User-facing menu options
        2. Overall sequence of sub-skillets
        3. Conditional execution of each sub-skillet

    Continue reading to see how to test these components in various skillet players.


Test the Skillet in PanHandler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Import the workflow skillet into PanHandler (instructions and troubleshooting found here), and open the
    **Sample SkilletBuilder workflow for EDL validation and configuration** workflow skillet from either
    the *Skillet Collections* or *Skillet Repositories* page.

    From this page, make sure that all of the workflow menu options appear as expected. For advanced variable
    types and attributes, such as **toggle_hint**, test all variations of the workflow menu and verify that these
    variables appear appropriately. If they do not appear as expected, you must go back into the **variables**
    section of the workflow skillet and troubleshoot.

        .. image:: /images/workflow_tutorial/run_workflow_menu.png
         :width: 800

    The main workflow skillet itself does not have a *Debug* tool like the other skillet types, so you will need to
    manually verify that the overall sub-skillet sequence is correct by stepping through the workflow. However,
    configuration sub-skillets do allow for inline debugging with the Skillet Debugger. Continue by clicking **Submit**.

    You should now be prompted with the user-input section of the first sub-skillet, the validation skillet. All of this
    sub-skillet's variables (firewall IP, username, and password and EDL URL) will not appear on the screen since they
    are defined as type **hidden**. Do know that every variable defined in the variable section of the sub-skillet's
    YAML file will get loaded from the context. Use :ref:`this guide<Checking Variable Values with Context>` to view
    all variables and their values in the context.

        .. image:: /images/workflow_tutorial/validation_user_input.png
          :width: 800

    Continuing the workflow, you should see the validation output. Verify this output using the validation skillet
    testing found in :ref:`the Validation Tutorial<Push to GitHub and Test in panHandler>`. In addition, you can find more
    resources in the PanHandler documentation for `Creating and Debugging Validation Skillets`_.

        .. image:: /images/workflow_tutorial/validation_output.png
          :width: 800

    .. _Creating and Debugging Validation Skillets: https://panhandler.readthedocs.io/en/master/skillets.html#creating-and-debugging-validation-skillets

    Click **Continue**, and then fill out the forms for the *Sample SkilletBuilder skillet with EDL, tag, and security policy*
    configuration skillet. Click **Continue** to land on the *Configure Target Information* screen.

        .. image:: /images/workflow_tutorial/configure_target_screen.png
          :width: 800

    On the target screen, you can click **Debug**, which gives an inline overview of each snippet in the configuration skillet.
    You can check here to make sure your user inputs are correct and the XML is formatted properly.

        .. image:: /images/workflow_tutorial/skillet_debugger.png
          :width: 800

    Finish out the workflow by continuing through each of the steps until you land on the *Workflow Completed* page, which is
    rendered from the final template sub-skillet.

        .. image:: /images/workflow_tutorial/workflow_completed.png
          :width: 800

    If a sub-skillet gets skipped or runs when it's not intended to, check the :ref:`Context<Checking Variable Values with Context>`
    for variable names and values currently cached. In addition, you can troubleshoot by viewing the context both before and after
    a sub-skillet is run to see which variables get generated during the sub-skillet execution.

    .. NOTE::
        If your workflow has a sequence of configure then validate, you will need to commit after the configuration
        skillet to see any changes in the validation skillet since the validation only looks at the running configuration.


Test the Skillet with SLI
~~~~~~~~~~~~~~~~~~~~~~~~~

    The SLI python package provides users a command line interface (CLI) for interacting with skillets, including a
    workflow skillet. Testing with SLI is very similar to :ref:`Test the Skillet in PanHandler`, except that you are
    using the command line instead of a Web GUI.

    After installing SLI in a python virtual environment and cloning your GitHub repository onto your local
    machine, change directory into the root of your repository. This SLI tutorial is going to use the SkilletBuilder's
    repository as an example of your GitHub repo.

    Start by loading and viewing all skillets inside your repository, using ``sli load``.

        .. code-block:: bash

            (venv) testing-device:~/SkilletBuilder$ sli load
              Name                                     Type
            -----------------------------------------------------------
              preview_xml_changes                      workflow
              generate_skillet_preview_output          template
              generate_skillet_preview_online          python3
              generate_skillet_preview_offline         python3
              SkilletBuilderSample_EDL_policy          panos
              configuration_explorer                   python3
              template_xml_edl_policy                  template
              validate_xml_edl_policy                  pan_validation
              workflow_xml_edl_policy                  workflow
              config_xml_edl_policy                    panos
              skeleton_yaml_file_xml                   template
              generate_set_cli                         workflow
              generate_set_cli_online                  python3
              generate_set_cli_offline                 python3
              generate_ansible_playbook                python3
              test_skillet_inline                      python3
              sample_validation_skilletbuilder         pan_validation
              skeleton_yaml_file_any                   template
              Generate_Skillet_workflow_exp            workflow
              generate_skillet_snippets_from_device    python3
              generate_skillet_snippets_from_config    python3
            (venv) testing-device:~/SkilletBuilder$

    Next, run the workflow skillet using the context with ``sli workflow -uc --name workflow_xml_edl_policy``, where
    *workflow_xml_edl_policy* is the name of your workflow skillet as seen in the load command. This executes the main
    workflow skillet and starts the user-interaction piece of the skillet menu.

        .. code-block:: bash

            (venv) testing-device:~/SkilletBuilder$ sli workflow -uc --name workflow_xml_edl_policy
            Device: 192.168.1.1
            Username: admin
            Password:
            NGFW IP or Hostname (192.168.1.1):
            NGFW Username (admin):
            NGFW Password:
            Confirm - NGFW Password:
            External Dynamic List's Source URL (http://someurl.com): http://sampleurl.com

            Config Validation Options
            -------------------------

            Validate configuration at the beginning of the workflow (y/n default: no): y
            Validate configuration at the end of the workflow (y/n default: no): y

              Input                                                      Value
            --------------------------------------------------------------------
              Validate configuration at the beginning of the workflow    Yes
              Validate configuration at the end of the workflow          Yes

            Are These answers ok? (y/n): y
            End of user variables.
            Running skillet validate_xml_edl_policy - pan_validation
            .
            .
            .

    .. NOTE::
        Variables in the user-input stage are either defined as a user's input to the command line or as
        the value currently stored in the context (as seen next to a variable in parenthesis). To use the
        context's value, the user **MUST** only input **enter**.

    To view the values stored in the context, use the command ``sli show_context -nc``. The ``-nc`` flag
    removes the entire configuration XML from the output for easier viewing.

    For additional information about SLI, view the documentation on `the SLI PyPI page`_.

    .. _the SLI PyPi page: https://pypi.org/project/sli/

|

Document
--------

    The final stage is to document key details about the skillet to provide contextual information
    to the user community.

README.md
~~~~~~~~~

    The workflow skillet repository has an empty placeholder ``README.md`` that should give an overview of the solution.
    The ``README.md`` should provide skillet-specific details such as what the skillet does, variable input descriptions,
    and caveats and requirements.

    ``README.md`` uses the markdown formatting language. Numerous examples can be found in the skillet files. There is also a
    wide array of `markdown cheat sheets`_ you can find using Google searches.
    Below are a few common markdown elements you can use in your documentation. Most IDEs can display the user view
    as you edit the markdown file.

    .. _markdown cheat sheets: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

        +-------------------------------------------------------------------------------------+
        | Markdown syntax options                                                             |
        +=====================================================================================+
        | `#, ##, ###` for header text levels (H1, H2, H3, etc.)                              |
        +-------------------------------------------------------------------------------------+
        | `**text**` for bold text                                                            |
        +-------------------------------------------------------------------------------------+
        | `*text*` or `_text_` to underline                                                   |
        +-------------------------------------------------------------------------------------+
        | `1. text` to create numbered lists                                                  |
        +-------------------------------------------------------------------------------------+
        | `* text`, `+ text`, `- text` for bullet style lists                                 |
        +-------------------------------------------------------------------------------------+
        | `[text](url)` for inline web links                                                  |
        +-------------------------------------------------------------------------------------+
        | \`test\` to highlight a text string                                                 |
        +-------------------------------------------------------------------------------------+
        | \`\`\`text block - one or more lines\`\`\` to create a highlighted text block       |
        +-------------------------------------------------------------------------------------+

    .. TIP::
        To view markdown edits for existing GitHub repos, click on the README.md file, then use the **Raw**
        option to display the output as raw markdown text. From here, you can copy and paste or review formatting.

    Paste this sample ``README.md`` file into your repository and push to GitHub.

    .. code-block:: md

        # Sample Workflow Skillet

        This is used in the training material as part of the Workflow tutorial.

        The solution utilizes three skillets:

        1. A validation skillet to verify the running configuration
        2. A configuration skillet to configure:
            * tag: create a tag using inputs for name, description, and color
            * external-list: create an edl using inputs for name, description, and url
            * security policies: inbound and outbound security policies referencing the edl and tag names
        3. A template skillet to output the workflow end

        The configuration skillet was taken from the Configuration Tutorial for Skillet Builder documentation
        (https://skilletbuilder.readthedocs.io/en/latest/tutorials/tutorial_configuration.html#).

        ## Workflow Sequence

        This workflow skillet begins by prompting the user to input the workflow menu options, described below.

        Depending on the *assess_options* result, a validation skillet will be run next to verify that an
        External Dynamic List object is configured for the *edl_url* inputted by the user. In addition,
        it will validate that two security policies exist denying traffic from and to the EDL object.

        Next, the workflow prompts the user to fill in forms about the EDL and tag information. With this information,
        the automation pushes a configuration that creates a tag object, EDL object, and two security policies.

        Again, depending on the *assess_options* result, the same validation skillet will be run.

        Finally, a template skillet is executed that outputs a **Workflow Completed** message, so the user is
        clear about the workflow's end.


        ## Variables

        ### Main Workflow Menu Options:

        * *TARGET_IP*: IP of firewall to validate and configure
        * *TARGET_USERNAME*: Username of firewall management user
        * *TARGET_PASSWORD*: Password of the above user
        * *edl_url*: URL used for the External Dynamic List
        * *assess_options*: Checkbox for validation skillet execution orders (beginning and/or
          end of the workflow)

        ### Configuration Sub-Skillet Options:

        * *tag_name*: Name of a newly created tag that is used in the security rules
        * *tag_description*: Text field to describe the tag
        * *tag_color*: Dropdown menu mapping color names to color numbers (required in the XML configuration)

        * *edl_name*: Name of the newly created External Dynamic List
        * *edl_description*: Text field used to describe the External Dynamic List

        The 'recurring' value for the EDL is set to *five-minutes*. This could be added as a variable but for this example, the
        value is considered a recommended practice so not configurable in the skillet.

        The EDL type is set to IP since used in the security policy and is not configurable in the skillet.

        ### Configuration Sub-Skillet Security Policy Referencing Variables

        The security policy does not have its own variables asking for rule name, zones, or actions. The rules are
        hardcoded with 'any' for most attributes and action as _deny_ to block traffic matching the EDL IP list.

        The security rule names use the EDL name followed by '-in' and '-out' to create unique security policies for each
        EDL. This is denoted in the yaml file with ```{{ edl_name }}``` included in the rule name.



    **Support Policy Text**

        Skillets are not part of Palo Alto Networks supported product so the policy text is appended to the
        README file to specify skillets are not supported. Sample text to copy/paste is found in the `SkilletBuilder repo README`_

    .. _SkilletBuilder repo README: https://raw.githubusercontent.com/PaloAltoNetworks/SkilletBuilder/master/README.md

LIVEcommunity
~~~~~~~~~~~~~

    Skillets can be shared in the LIVEcommunity as Community or Personal skillets. Community Skillets
    are expected to have a higher quality of testing, documentation, and ongoing support. Personal skillets
    can be shared as-is to create awareness and eventually become upgraded as Community Skillets.
