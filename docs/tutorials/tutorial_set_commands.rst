Basic Configuration With Set Commands
==============================

Overview
--------

This tutorial is designed to help the user get familiar with using set commands to bring up and apply basic configs to their NGFW. By then end of this tutorial the user should be able to alter their firewall manually through the Command Line Interface(CLI) with set commands. All set/op commands that can be entered in the CLI manually can also be transformed into an automation playlist in the form of a skillet. This allows the user to run a series of set commands to easily configure their NGFW with just the click of a button.

This Basic Config with Set Commands tutorial will show the user how to:

* Access and configure the Next Generation Firewall(NGFW) through the web UI and CLI
* Capture configuration differences made on the NGFW into set commands and automation skillets
* Learn how to use Panhandler tooling
* Learn how to use the SLI tool on the CLI

The video below provides an end-to-end perspective for building a configuration skillet as a complement
to the documentation content.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=17392613-262a-4606-a11a-ab6c010b894e&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

|

You can click on the hyperlink menu below to quickly navigate to different parts of the tutorial.

1. `Prerequisites`_

2. `Set Up Your Environment`_

3. `Build the Skillet`_

4. `Test and Troubleshoot`_

5. `Document`_


Prerequisites
-------------

Before moving forward with the tutorial, please ensure the following prerequisites have been fulfilled.

* Have an up and running NGFW Virtual Machine(VM)
* A GitHub_ account with access permissions to edit repository content
* Docker_ desktop active and running on your machine
* Personal preference of text editor/IDE(Integrated Development Environment) for XML/YAML editing[1]
* Ability to access the NGFW device via GUI[2][3], SSH/CLI[4] and API
* For users wishing to work through the command line have SLI_ set up and ready to go

  * SLI can be set up locally on your machine to run quick and efficient commands on your local CLI. Please refer to and follow the steps in the linked SLI_ page to get started
* For users wishing to work through the browser UI log into PanHandler_ and be able to import/run Skillets, specifically SkilletBuilder_ tools
    
It may also be useful to review the following topics before getting started:

- :ref:`XMLandSkillets`
- :ref:`jinjaandskillets`

.. _PanHandler: https://panhandler.readthedocs.io/en/master/
.. _GitHub: https://github.com
.. _Docker: https://www.docker.com
.. _SkilletBuilder: https://github.com/PaloAltoNetworks/SkilletBuilder
.. _SLI: https://pypi.org/project/sli/
.. [1] PyCharm or SublimeText are good options for a beginner text editor or IDE.
.. [2] Log in to the NGFW UI by entering this, *https://XXX.XXX.XXX.XXX* (with your NGFW's management IP replacing the X's), into the web browser URL bar.
.. [3] If you reach a warning page during this step, click advanced settings and choose the proceed to webpage option.
.. [4] Log in to the NGFW via CLI by opening a terminal/bash window on your local machine and entering this, *ssh username@XXX.XXX.XXX.XXX* (with your NGFW's management IP replacing the X's).

This tutorial will be split into 4 main sections below and can either be done by reading the document or by watching the tutorial videos. There is a video tutorial for achieving the intended results via use of the PanHandler UI tool and the SLI command line interface tool.

Set Up Your Environment
-----------------------

In this section we will set everything up that will be needed to successfully complete this tutorial. 

NGFW
~~~~

    This is the device that we will be working with and configuring during the tutorial. Be sure that you are able to log into the
    firewall UI by inputting its management IP into the web browser. When logged in it can be useful to make note of a number of things.

    **Software Version:**
    Please take note of the devices software version when traversing this tutorial. Some configuration elements may be version specific
    and require unique skillets per software releases.

    **Baseline Configuration:** It is recommended to capture a *baseline* configuration of your newly brought up and pre-configured
    firewall. This is especially useful for testing purposes if you wish to quickly revert any changes made on the NGFW back to a blank
    slate. This can be done on the NGFW UI via *Devices->Setup->Operations->Save* named configuration snapshot*.

    **API Access**
    Login credentials with API access to test playing Skillets and any changes made by using set commands.

Having the CLI 'Set Command Ready'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This tutorial will use the Skillet Generator tool but it is also useful to know how to configure the firewall through the CLI. These
    operations commands below will help you get started with configurations but please also refer to this supplemental article_ for more
    guidance on using the CLI with the NGFW.

    .. code-block:: bash
      
      admin@PA-VM> ssh admin@99.99.999.999
      admin@PA-VM> set cli config-output-format set
      admin@PA-VM> debug cli on
      admin@PA-VM> configure
      Entering configuration mode
      (this is where you will make changes on the NGFW)
      admin@PA-VM> set tag new color color3 comments "Example set command"
      admin@PA-VM> commit
      admin@PA-VM> exit
      exiting configuration mode
      
    First log in with the "*ssh*" command, we then enter a "*set*" command to display configuration data as set commands. *Debug cli on* 
    will allow for the easy capturing of the specific configuration xpath whenever a change is made via set commands on the cli, this
    `knowledgebase article`_ is also useful in understanding how to view NGFW configurations in "*set*" and "*xml*" formats via the cli.
    configuration mode with the keyword, "*configure*". Once in configuration mode we can make changes on the NGFW with set commands.
    After all desired changes are made you can commit them to the NGFW via the "*commit*" command and then exit out of configuration 
    mode with "*exit*".
    
.. _article: https://docs.paloaltonetworks.com/pan-os/9-0/pan-os-cli-quick-start.html
.. _`knowledgebase article`: https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClHoCAK

Running PanHandler
~~~~~~~~~~~~~~~~~~

  PanHandler is a utility that is used to create, load and view configuration templates and workflows. We will be using PanHandler to 
  help create automation templates called "*skillets*" and use these templates to automate the process of deploying set commands to our 
  NGFW.
  
  If you have not already installed or run the latest version of PanHandler, in order to access the latest version of the PanHandler web
  UI you do the following commands in your CLI.
  
  .. code-block:: bash
  
    > curl -s -k -L http://bit.ly/2xui5gM | bash
  
  Then you want to input the following into your browsers URL.
    
  .. code-block:: html
  
    http://localhost:8080

  Please refer to the `PanHandler documentation`_ for more detailed information on the many useful functions of the PanHandler utility.
  
.. _`PanHandler documentation`: https://panhandler.readthedocs.io/en/master/overview.html
  
Importing SkilletBuilder Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Once you have gained access to the PanHandler UI you will want to import the SkilletBuilder_ repository. This is done by clicking
    the **PanHandler** drop down menu at the top of the page. Then click on **import skillets** and at the bottom of the page you can
    change the repository name and paste the cloned git repository URL in HTPPS or SSH.

.. _SkilletBuilder: https://github.com/PaloAltoNetworks/SkilletBuilder

Build The Skillet
-----------------

  Edit the .meta-cnc.yaml file to create the skillet

  * create the github repo and clone to edit
  * create an empty .meta-cnc.yaml file
  * save 'before and after' configuration snapshots
  * use the :ref:`Generate a Skillet` tool to create the initial skillet
  * add the variables
  * commit and push to Github

Test and Troubleshoot
---------------------

  Test against a live device and fix/tune as needed.

  * Use the :ref:`Skillet Test Tool` to quick test the skillet
  * Import the skillet into panHandler to test web UI and config loading
  * Fix any UI or loading errors
  * Tune the web UI, configuration elements


Document
--------

  The final and important steps are good documentation and sharing with the community.

  * READme.md documentation in the Github repo
  * Skillet District posting
  * Others can now import into their tools and use the new skillet


















Run PanHandler
~~~~~~~~~~~~~~

  PanHandler will be used to generate and test the skillet.

  Use the curl command found in :ref:`Updating or Running the Master Version` if panHandler is not installed or not running
  the latest version.


Import Skillet Builder Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  In panHandler import the :ref:`Skillet Builder Tools` repo.

Skillet Editor
~~~~~~~~~~~~~~

  The IDE should be ready with:

  * a full view of files and directories in the skillet
  * text editor that supports YAML and XML file types
  * terminal access to interact with Git/Github

|

Build the Skillet
--------------------

The following steps take the user from creating the Github repo, through generating and editing the skillet, to a final
push of skillet content back to the created repo.

Creating a New Repo and Cloning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  :ref:`The Skillet Framework` uses Github as the primary option for storing skillets.

  Log in to Github and select ‘New’ to add a new repo.

    .. image:: /images/configure_tutorial/create_new_repo_button.png
        :width: 600

  Suggestions are to include a README file and MIT license. You can also add a .gitignore file, primarily to ignore
  pushing any EDI directories such as .idea/ used by Pycharm.

    .. image:: /images/configure_tutorial/create_new_repo_fields.png
        :width: 600

  Once created, copy the clone URL from the GUI.
  This is found with the green ‘Clone or download’ button and NOT the browser URL.

    .. image:: /images/configure_tutorial/clone_new_repo.png
       :width: 600


  Using a local console or your editor tools, clone the repo to your local system.
  For example, using the console and the link above:

  .. code-block:: bash

      midleton$ git clone https://github.com/scotchoaf/SBtest.git

  .. NOTE::
    If your account or repo is set up requiring 2-factor authentication then you should clone using the SSH link instead.
    This is required to push configuration changes back to the repo.  You may have to `add an SSH key for Github`_

.. _add an SSH key for Github: https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent


Create the Configuration in the NGFW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Before modifying the configuration, ensure you have a snapshot of the 'before' configuration.

  The tutorial examples use the GUI to create the EDL, tag, and security rules.
  Many of the config values are placeholders that look like variable names (hint, hint).
  You can also load the :ref:`Sample Configuration Skillet` found in the Skillet Builder collection.

  Configure the external-list object with a name, description, and source URL.

  .. image:: /images/configure_tutorial/configure_edl.png
     :width: 600


  |

  Configure the tag object with a name, color, and comments (description).

  .. image:: /images/configure_tutorial/configure_tag.png
     :width: 400


|

.. TIP::
    The skillet will only add a single tag to the configuration.
    However, the GUI shows a color name while the XML data in the NGFW is based on a color number.
    The use of multiple tag entries is used to extract the color values.
    So note that in some cases the GUI and XML can use different values and we can use sample configs
    like this to discover those values.

|

  Configure Inbound and Outbound security rules referencing the tag and external-list. Note that the
  rule names are prepended with the EDL name. In later steps variables are used in the rule names to
  map the EDL and ensure rule names are unique.

.. image:: /images/configure_tutorial/configure_security_rules.png
    :width: 800


Create the Project Skeleton Structure for XML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  This model places the XML elements within the .meta-cnc.yaml file. This is the standard output used by the
  Skillet Generator.

  In the editor open the repo directory and add the following:

    * a new folder that will contain the skillet content (eg. tag_edl_block_rules)
    * in the new folder add an empty ``.meta-cnc.yaml`` file (will populate the text later)
    * in the new folder add an empty README.md file (will populate the text later)

  The skillet directory structure will look like:

  .. image:: /images/configure_tutorial/configure_skillet_folder.png
     :width: 250


Generate the Skillet
~~~~~~~~~~~~~~~~~~~~

  In panHandler use the :ref:`Generate a Skillet` skillet to extract the difference between the baseline and
  modified configuration with offline mode choosing 'From uploaded configs'.

  .. image:: /images/configure_tutorial/configure_skillet_generator.png
     :width: 800


|

  After the files are added, the next stage of the workflow is a web form for the YAML file preamble attributes.

  .. image:: /images/configure_tutorial/configure_skillet_preamble.png
     :width: 800


|

  Suggested tutorial inputs:

    * Skillet ID: tag_edl_tutorial
    * Skillet Label: Tutorial skillet to configure tag, EDL, and security rules
    * Skillet description: The tutorial skillet demonstrates the use of various config snippets and variables
    * Collection Name: Tutorial
    * Skillet type: ``panos``

  Clicking ``Submit`` results in a screen output of the .meta-cnc.yaml file.

  The rendered YAML file contains:

    * preamble populated with the web form values
    * placeholder variables section
    * snippets section with XPath/element entries where each diff found

  .. toggle-header:: class
      :header: **show/hide the output .meta-cnc.yaml file**

      .. code-block:: yaml

        # skillet preamble information used by panhandler
        # ---------------------------------------------------------------------
        # unique snippet name
        name: tag_edl_tutorial
        # label used for menu selection
        label: Tutorial skillet to configure tag, EDL, and security rules
        description: The tutorial skillet demonstrates the use of various config snippets and variables

        # type of device configuration
        # common types are panorama, panos, and template
        # https://github.com/PaloAltoNetworks/panhandler/blob/develop/docs/metadata_configuration.rst
        type: panos
        # preload static or default-based templates
        extends:

        # grouping of like snippets for dynamic menu creation in panhandler
        labels:
          collection:
            - Tutorial

        # ---------------------------------------------------------------------
        # end of preamble section

        # variables section
        # ---------------------------------------------------------------------
        # variables used in the configuration templates
        # type_hint defines the form field used by panhandler
        # type_hints can be text, ip_address, or dropdown
        variables:
          - name: hostname
            description: Firewall hostname
            default: myFirewall
            type_hint: text
          - name: choices
            description: sample dropdown list
            default: choices
            type_hint: dropdown
            dd_list:
              - key: option1
                value: option1
              - key: option2
                value: option2
        # ---------------------------------------------------------------------
        # end of variables section

        # snippets section
        # ---------------------------------------------------------------------
        # snippets used for api configuration including xpath and element as file name
        # files will load in the order listed
        # NOTE: The following snippets are auto-generated and ordered automatically.
        # Changing the content of the snippet may be necessary, but do NOT change the order

        # There is a variable called snippets that we can use to auto-generate this section for us
        snippets:

          - name: entry-953630
            xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag
            element: |-
                <entry name="tag_name">
                              <color>color1</color>
                              <comments>tag_description</comments>
                            </entry>

          - name: external-list-467839
            xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]
            element: |-
                <external-list>
                            <entry name="edl_name">
                              <type>
                                <ip>
                                  <recurring>
                                    <five-minute/>
                                  </recurring>
                                  <description>edl_description</description>
                                  <url>http://someurl.com</url>
                                </ip>
                              </type>
                            </entry>
                          </external-list>

          - name: entry-702183
            xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/rulebase/security/rules
            element: |-
                <entry name="edl_name-out" uuid="29209605-e2f4-40b1-ab12-98edf6ae5b8b">
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
                                    <member>edl_name</member>
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
                                    <member>tag_name</member>
                                  </tag>
                                  <action>deny</action>
                                  <description>outbound EDL IP block rule. EDL info: </description>
                                </entry>

          - name: entry-978971
            xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/rulebase/security/rules
            element: |-
                <entry name="edl_name-in" uuid="20d10cd2-f553-42f2-ba05-3d00bebeac60">
                                  <to>
                                    <member>any</member>
                                  </to>
                                  <from>
                                    <member>any</member>
                                  </from>
                                  <source>
                                    <member>edl_name</member>
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
                                    <member>tag_name</member>
                                  </tag>
                                  <action>deny</action>
                                  <description>inbound EDL IP block rule. EDL info: </description>
                                </entry>


        # ---------------------------------------------------------------------
        # end of snippets section

|

Copy the Output to .meta-cnc.yaml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Copy the output text under **Generated Skillet** and paste into the .meta-cnc.yaml file.

  .. NOTE::
        At this point if building your own skillet you can use the :ref:`Skillet Test Tool` to play
        the skillet without variables. Common reasons for raw output testing include the possible need for snippet reordering
        and confirmation that the snippet elements will load

Add Variables to Snippets
~~~~~~~~~~~~~~~~~~~~~~~~~

  Snippets can be edited to use contextual names, more coarse or granular snippets,
  and formatting clean up such as XML elements. The modifications are optional based on Skillet Builder preference.

  Adding variables is done in both the snippets and variables sections. The snippets section is edited by
  adding a :ref:`Jinja Variable` where each value can be modified by the user. This correlates to variables
  defined in the variables section specifying type for web form display and validation.

  .. TIP::
    YAML is notoriously finicky about whitespace and formatting. While it's a relatively simple structure and easy to learn,
    it can often also be frustrating to work with. A good reference to use to check your
    YAML syntax is the `YAML Lint site <http://www.yamllint.com/>`_.

  The tag has 3 variables (tag_name, tag_description, tag_color)

  .. code-block:: yaml

      - name: object_tag
        xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag
        element: |-
            <entry name="{{ tag_name }}">
              <color>{{ tag_color }}</color>
              <comments>{{ tag_description }}</comments>
            </entry>

  The external-list element has 3 variables (edl_name, edl_description, edl_url)
  that are added into the configuration resulting in:


  .. code-block:: yaml

      - name: object_external_list
        xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]
        element: |-
            <external-list>
                <entry name="{{ edl_name }}">
                  <type>
                    <ip>
                      <recurring>
                        <five-minute/>
                      </recurring>
                      <description>{{ edl_description }}</description>
                      <url>{{ edl_url }}</url>
                    </ip>
                  </type>
                </entry>
              </external-list>


  Note that the <recurring> value is static as ``five-minute`` without a variable.
  Some values may remain static as a best practice or, as with type ``<ip>``, specific to the configuration requirement.


  Lastly, the security rules leverage EDL and tag variables (edl name, tag name) as a connected set of template configs.

  .. code-block:: yaml

      - name: security_rule_outbound
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
              <description>outbound EDL IP block rule. EDL info: {{ edl_description }} </description>
            </entry>

      - name: security_rule_inbound
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
              <description>inbound EDL IP block rule. EDL info: {{ edl_description }}</description>
            </entry>

  In this outbound rule example, not only are the variables used for the standard destination address and tag fields,
  but text substitution can also be used to create unique entries. In this case, the EDL name is used as
  a security rule name prefix joined with ‘-out’ and the rule description contains the edl_description.

  .. TIP::
    When creating the modified configuration for a skillet, you can use variable-type names where applicable to
    simplify the variable insertion into the snippets. Simply wrap the names with ``{{  }}`` or even use
    search-replace when text content is unique within the file.

  .. TIP::
    If the variables are used across multiple skillets as part of defined Steps or a workflow, reuse the same
    variable name where possible. Tools like panHandler will cache web form inputs and auto-populate values
    when the same variable is encountered again.

Edit the Variables Section
~~~~~~~~~~~~~~~~~~~~~~~~~~

  Now that the variable set is known, they must be added to the metadata file along with a description to be used
  in the web form, a default provided in the form, and a type_hint to specify the type of web form field.
  This metadata allows tools like panHandler to auto-generate the web form without any user specific HTML coding.

  Key is :ref:`Ensuring all variables are defined` in the variables section. In the tutorial we'll use the first
  grep option to generate a list of added variables.

  .. code-block:: bash

    midleton:SBtest$ grep -r '{{' . |  cut -d'{' -f3 | awk '{ print $1 }' | sort -u
    edl_description
    edl_name
    edl_url
    tag_color
    tag_description
    tag_name

  The output of the grep command shows the six variables used in the tutorial configs.

  From here, edit the variables section of the YAML file. Note that 4 are text and one is a URL while color is using a dropdown.
  The dropdown is useful when the GUI and XML use different values or limited choices should be offered.

  .. code-block:: yaml

    variables:
      - name: edl_name
        description: External-list name
        default: my_edl
        type_hint: text
      - name: edl_description
        description: External-list description
        default: my_edl description
        type_hint: text
      - name: edl_url
        description: External-list URL
        default: my_edl
        type_hint: url
      - name: tag_name
        description: tag name
        default: my_tag
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
          - key: green
            value: color2
          - key: orange
            value: color6
          - key: red
            value: color1

  The values for the tag color require color numbers and not the Web UI presented names. This is common for many dropdown
  selections in the Web UI. For these types of situations, you can create a set of items (eg. tags)
  to be displayed in the XML output to match Web UI and XML required values.

  For the tag color values, below is the config showing the 3 color values for green, orange, and red.
  Additional colors can be extracted by using the GUI to create more tags and then use the CLI and ‘show tag’
  to see additional color numbers.

  .. code-block:: xml

      <entry name="tag_name">
        <color>color1</color>
        <comments>tag_description</comments>
      </entry>
      <entry name="tag_orange">
        <color>color6</color>
      </entry>
      <entry name="tag_green">
        <color>color2</color>
      </entry>

  This method or the CLI '?' complete action can be used to find the XML specific configuration options instead of the
  Web UI options.

Local Skillet Test
~~~~~~~~~~~~~~~~~~

  Before pushing the skillet to Github, use the :ref:`Skillet Test Tool` to validate the final YAML file formatting
  and variable additions. Paste the contents of the YAML file into the test tool and submit. This will play the skillet
  using the default variable values. Check that the configuration loaded into the NGFW.

  Common errors at this stage likely include YAML formatting issues, snippet ordering problems, or a variable typo.

Push the Skillet to Github
~~~~~~~~~~~~~~~~~~~~~~~~~~

  At this stage initial building is complete. The YAML file preamble, variables, and snippets sections all have
  relevant content added. Now we want to push this to Github for additional testing and tuning.

  Use:

    * ``git add .`` to add the modified files to the commit
    * ``commit -m "message"`` to commit the files with a change message
    * ``git push origin master`` to push to the repo master branch

  .. code-block:: bash

    midleton:SBtest:$
    midleton:SBtest:$ git add .
    midleton:SBtest:$ git commit -m "first commit to Github"
    [master 5f73017] first commit to Github
     2 files changed, 177 insertions(+)
     create mode 100644 tag_edl_block_rules/.meta-cnc.yaml
     create mode 100644 tag_edl_block_rules/README.md
    midleton:SBtest:$ git push origin master
    Enumerating objects: 6, done.
    Counting objects: 100% (6/6), done.
    Delta compression using up to 12 threads
    Compressing objects: 100% (4/4), done.
    Writing objects: 100% (5/5), 1.62 KiB | 1.62 MiB/s, done.
    Total 5 (delta 1), reused 0 (delta 0)
    remote: Resolving deltas: 100% (1/1), completed with 1 local object.
    To github.com:scotchoaf/SBtest.git
       61b3520..5f73017  master -> master
    midleton:SBtest:$


  The skillet now resides in Github. Note however that the page README gives no real indication about
  what is contained in this repo. We'll get back to that later.

  .. image:: /images/configure_tutorial/configure_skillet_repo_updated.png
     :width: 800


Test and Troubleshoot
------------------

Now that the skillet has been pushed to Github, the skillet can be imported to panHandler to test the user experience.

Import the Skillet
~~~~~~~~~~~~~~~~~~

  Get the new skillet URL from Github

  .. image:: /images/configure_tutorial/skillet_clone_url.png
     :width: 300


|

  Use ``Import Skillets`` with the ``Clone or download`` Github URL to import the skillet to panHandler.

  .. image:: /images/configure_tutorial/configure_skillet_import.png
     :width: 400


|

  View the skillet ``Detail`` from the ``Skillet Repositories`` page.

  .. image:: /images/configure_tutorial/configure_skillet_detail.png
     :width: 800


|

  **Github URL and branch**

    * validate the correct URL for your skillet
    * check the Active Branch, master for the tutorial

  **Latest Updates**

    * review the last commit to ensure you are testing the latest push
    * ``Update to Latest`` as needed to pull recent commits

  **Metadata files**

    * check that all skillet Labels are listed; missing labels indicate an error in the YAML file
    * check that all label names and descriptions are unique and understandable
    * [Optional] click the gear icon next to a label to locally view the YAML file contents

  **Collections**

    * verify the collection names are correct and edit YAML files as needed

  .. TIP::
    You can run skillets from the Detail page by clicking its Label name. This bypasses the need to click into
    a Collection for each push update during testing.

  .. NOTE::
    If you receive errors during import, the most common issue is an error with YAML formatting.
    Check alignment and syntax, push to Github, then try to import again.

Play the Skillet
~~~~~~~~~~~~~~~~

  From the Detail or Collection view, play the skillet. Although you may have tested with the Test Tool,
  playing the imported skillet allows the builder to review the Web UI elements presented to the user.

  .. image:: /images/configure_tutorial/configure_skillet_play.png
     :width: 800


|

  Before pushing the configuration to the device, you can use the ``Debug`` option to view the rendered skillets.
  This view is used to validate variable substitutions and XML formatting.

  .. image:: /images/configure_tutorial/configure_skillet_debug.png
     :width: 800


  Check both the output messages in panHandler and actual NGFW view to test the skillet. Also verify that the
  configuration loads as candidate and will also commit. If you receive errors messages, common issues may be:

    * snippet load order
    * variable typos in the snippet section or not included in the variables section
    * invalid input data that passes web form validation but not NGFW validation checks

Edit, Push, Test
~~~~~~~~~~~~~~~~

 If errors are found, repeat the steps above until a clean skillet can be loaded and committed.

Document
-------------

The final stage is to document key details about the skillet to provide contextual information to the user community.

README.md
~~~~~~~~~

  The skillet repo created has a placeholder README.md and earlier in the tutorial we created a README.md within
  the skillet directory. The main README gives an overview of the repo for any user viewing the page. The skillet
  directory README should provide skillet-specific details such as what the skillet does, variable input descriptions,
  and caveats and requirements.

  README.md uses the markdown format. Numerous examples can be found in the skillet files. There is also a
  wide array of `markdown cheat sheets`_ you can find using Google searches.
  Below are a few common markdown elements you can use in your documentation. Most EDIs can display the user view
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
    To view markdown edits in existing Github repos, click on the README.md file, then use the ``Raw``
    option to display the output as raw markdown text. From here you can copy-paste or review formatting.

  Sample README.md file for the tutorial skillet. Paste into the skillet README file and push to Github.
  View the skillet repo to see the updated page text.

  .. code-block:: md

    # Sample Configuration Skillet

    This is used in the training material as part of the tutorial.

    The skillet has 3 xml elements:

    * tag: create a tag using inputs for name, description, and color
    * external-list: create an edl using inputs for name, description, and url
    * security policies: inbound and outbound security policies referencing the edl and tag names

    ## variables

    * tag_name: name of a newly created tag and used in the security rules
    * tag_description: text field to describe the tag
    * tag_color: dropdown mapping color names to color numbers (required in the xml configuration)

    * edl_name: name of the newly created external-list
    * edl_description: text field used to describe the external-list
    * edl_url: url used for the external-list

    The 'recurring' value for the EDL is set to five-minutes. This could be added as a variable but for this example, the
    value is considered a recommended practice so not configurable in the skillet.

    The EDL type is set to IP since used in the security policy and is not configurable in the skillet.

    ## security policy referencing variables

    The security policy does not have its own variables asking for rule name, zones, or actions. The rules are
    hardcoded with 'any' for most attributes and action as deny to block traffic matching the EDL IP list.

    The security rule names use the EDL name followed by '-in' and '-out' to create unique security policies for each
    EDL. This is denoted in the yaml file with ```{{ edl_name }}``` included in the rule name.

  **Support Policy Text**

  Skillets are not part of Palo Alto Networks supported product so the policy text is appended to the
  README file to specify skillets are not supported. Sample text to copy/paste is found in the `SkilletBuilder repo README`_

  .. _SkilletBuilder repo README: https://raw.githubusercontent.com/PaloAltoNetworks/SkilletBuilder/master/README.md

Live Community
~~~~~~~~~~~~~~

  Skillets can be shared in the Live community as Community or Personal skillets. Community Skillets
  are expected to have a higher quality of testing, documentation, and ongoing support. Personal skillets
  can be shared as-is to create awareness and eventually become upgraded as Community Skillets.


