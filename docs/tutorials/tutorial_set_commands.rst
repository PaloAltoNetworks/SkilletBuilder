Basic Configuration With Set Commands
=====================================


Overview
--------

This tutorial is designed to help the user get familiar with using set commands to bring up and apply basic configs to their NGFW. By then end of this tutorial the user should be able to alter their firewall manually through the Command Line Interface(CLI) with set commands. All set/op commands that can be entered in the CLI manually can also be transformed into an automation playlist in the form of a skillet. This allows the user to run a series of set commands to easily configure their NGFW with just the click of a button. The configuration tutorial will create a simple configuration including:

  - An IP External Dynamic List (EDL) object
  - A tag object
  - Security rules (Inbound and Outbound) referencing the EDL and tag objects

This Basic Config with Set Commands tutorial will show the user how to:
  
  - Access and configure the Next Generation Firewall(NGFW) through the web UI and CLI
  - Capture configuration differences made on the NGFW into set commands and automation skillets
  - Learn how to use Panhandler tooling
  - Learn how to use the Skillet Line Interface(SLI) tool on the CLI
  - Learn the basics of using GitHub and repositories

The video below provides an end-to-end perspective for building a configuration skillet and can be used as a complement
to the documentation content.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=17392613-262a-4606-a11a-ab6c010b894e&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>


Navigation Menu
~~~~~~~~~~~~~~~

You can click on the hyperlink menu below to quickly navigate to different parts of the tutorial.

1. `Prerequisites`_

2. `Setting Up Your Environment`_

3. `Building Skillets with Set Commands`_

4. `Test and Troubleshoot`_

5. `Document`_


Prerequisites
-------------

Before moving forward with the tutorial, please ensure the following prerequisites have been fulfilled.

* Have an up and running NGFW Virtual Machine(VM)
* A GitHub_ account with access permissions to edit repository content
* Docker_ desktop installed, active and running on your local machine
* Ability to access the NGFW device via GUI[1][2], SSH/CLI[3] and API
* For users wishing to work through the command line have SLI_ set up and ready to go

  * SLI can be set up locally on your machine to run quick and efficient commands on your local CLI. SLI is a CLI interface used for interacting with Skillets. Please refer to and follow the steps in the linked SLI_ page to get started
* For users wishing to work through the browser UI log into PanHandler_ and be able to import/run Skillets, specifically SkilletBuilder_ tools
    
It may also be useful to review the following topics before getting started:

- :ref:`XMLandSkillets`
- :ref:`jinjaandskillets`

.. _PanHandler: https://panhandler.readthedocs.io/en/master/
.. _GitHub: https://github.com
.. _Docker: https://www.docker.com
.. _SkilletBuilder: https://github.com/PaloAltoNetworks/SkilletBuilder
.. _SLI: https://pypi.org/project/sli/

.. [1] Log in to the NGFW UI by entering this, *https://X.X.X.X* (with your NGFW's management IP replacing the X's), into the web browser URL bar.
.. [2] If you reach a warning page during this step, click advanced settings and choose the proceed to webpage option.
.. [3] Log in to the NGFW via CLI by opening a terminal/bash window on your local machine and entering this, *ssh {username}@{X.X.X.X}* (with your NGFW's management IP replacing the X's).

This tutorial will be split into 4 main sections below and can either be done by reading the document or by watching the tutorial videos. There is a video tutorial for achieving the intended results via use of the PanHandler UI tool and the SLI command line interface tool.


Setting Up Your Environment
---------------------------

In this section we will set up everything that will be needed to successfully complete the tutorial. Your skillet building environment consists of 5 essential parts:

1. GitHub
  * `Initialize a New Repository and Clone it to your Local Machine Using GitHub`_
  * `Create the File Structure for the Project in GitHub`_
2. Firewall
  * `NGFW`_
  * `Having the CLI Set Command Ready`_
3. PanHandler
  * `Running PanHandler`_
  * `Restarting PanHandler`_
4. SkilletBuilder Tools
  * `Importing SkilletBuilder Tools`_
5. SLI
  * `Running SLI`_
  


Initialize a New Repository and Clone it to your Local Machine Using GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Here we will be walking through logging into GitHub, creating and adding a repository as well as some GitHub best practices to keep
    in mind.

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
    
  .. NOTE::
    Please reference this `PanHandler Link`_ for more information on working with private git repositories and SSH keys in
    PanHandler. Please click on the side bar sections labeled **Adding a New Skillet Repository -> Using a Private Git Repository**.

.. _add an SSH key for Github: https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent    
.. _`PanHandler Link`: https://panhandler.readthedocs.io/en/master/using.html#adding-a-new-skillet-repository
    
Create the File Structure for the Project in GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  This model places the set command elements within the .skillet.yaml file. This is the standard output used by the Skillet Generator.

  In your terminal open the repo directory that was just cloned and add the following:

    * A new folder that will contain the skillet content (eg. tag_edl_block_rules)
    * In the new folder add an empty ``.skillet.yaml`` file 
    
        * The contents of the file will be populated later in the tutorial
    * in the new folder add an empty README.md file 
    
        * The contents of the file will be populated later in the tutorial

  The skillet directory structure will look like:

UPDATE THIS IMAGE

  .. image:: /images/configure_tutorial/configure_skillet_folder.png
     :width: 250

NGFW
~~~~

    This is the device that we will be working with and configuring during the tutorial. 

    **Baseline Configuration:** It is recommended to capture a *baseline* configuration of your newly brought up and pre-configured
    firewall. This is especially useful for testing purposes if you wish to quickly revert any changes made on the NGFW back to a
    blank slate. This can be done on the NGFW UI via *Devices->Setup->Operations->Save* named configuration snapshot*.
    
    .. NOTE::
    Some skillet configuration elements may be version specific and require unique skillets per software releases. Verify that your
    NGFW **Software Version** is compatible with associated skillets.


DO WE STILL NEED??
Having the CLI Set Command Ready
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This tutorial will use the Skillet Generator tool to create automation workflows to alter the NGFW configuration, but it is also
    useful to know how to configure the firewall through the CLI. 

    These operational commands below will help you get started with basic configurations but please also refer to this supplemental
    article_ for more guidance on using the CLI with the NGFW.

    .. NOTE::
      If you are logging into the NGFW for the first time via CLI, you may need to authorize the ECDSA key fingerprint. Type 'yes' 
      before continuing.

    .. code-block:: bash
      
      admin@PA-VM> ssh {username}@{X.X.X.X}
      admin@PA-VM> set cli config-output-format set
      admin@PA-VM> debug cli on
      admin@PA-VM> configure
      Entering configuration mode
      (this is where you will make changes on the NGFW)
      admin@PA-VM> set tag new color color3 comments "Example set command"
      admin@PA-VM> commit
      admin@PA-VM> exit
      exiting configuration mode
      
    First log in with the *ssh* command, we then enter a *set* command to display configuration data as set commands. *Debug cli on* 
    will allow for the easy capturing of the specific configuration xpath whenever a change is made via set commands on the cli, this
    `knowledgebase article`_ is also useful in understanding how to view NGFW configurations in *set* and *xml* formats via the cli.
    Next, enter configuration mode by typing the keyword, *configure*. Once in configuration mode we can make changes on the NGFW with
    set commands. After all desired changes are made you can commit them to the NGFW via entering the *commit* command and then 
    exiting out of configuration mode with the *exit* command.
    
.. _article: https://docs.paloaltonetworks.com/pan-os/9-0/pan-os-cli-quick-start.html
.. _`knowledgebase article`: https://knowledgebase.paloaltonetworks.com/KCSArticleDetail?id=kA10g000000ClHoCAK


Running PanHandler
~~~~~~~~~~~~~~~~~~

  PanHandler is a utility that is used to create, load and view configuration templates and workflows. 

  We will be using PanHandler to help create automation templates called *skillets*, and use these templates to automate the
  process of deploying set commands to our NGFW.
  
  If you have not already installed or run the latest version of PanHandler, in order to access the latest version of the
  PanHandler web UI you can do the following commands in your CLI.
  
  .. NOTE::
    PanHandler is always coming out with new releases. In order to get the most out of using PanHandler be sure to frequently
    check for updates for the latest version.
  
  .. code-block:: bash
  
    > curl -s -k -L http://bit.ly/2xui5gM | bash
  
  Then you want to input the following into your browser's URL.
    
  .. code-block:: html
  
    http://localhost:8080
    
 Once you have entered the above command into your browser's URL you will be prompted for a username and password. The default username
 is *paloalto* and the default password is *panhandler*.

  Please refer to the `PanHandler documentation`_ for more detailed information on the PanHandler utility tools.
  
.. _`PanHandler documentation`: https://panhandler.readthedocs.io/en/master/overview.html
  

Restarting PanHandler
~~~~~~~~~~~~~~~~~~~~~

  If you already installed PanHandler, you will eventually need to restart the container.

  Navigate to the Docker Desktop Application on your local machine. You should see the 'panhandler' container listed on
  the dashboard.

  **insert pic here**

  Click 'Start' to restart the container. You should now be able to access the PanHandler GUI at the same URL as before:

.. code-block:: bash

    http://localhost:8080
  
  
PROBABLY DONT NEED AFTER TALK WITH SCOTT SHOWCASE INERT PANHANDLER "SKILLETBUILDER" FUNCTIONALITY  
Importing SkilletBuilder Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This section will go over how to import skillet repositories to PanHandler.
    
    Once you have gained access to the PanHandler UI you will want to import the SkilletBuilder_ repository. This is done by clicking
    the **PanHandler** drop down menu at the top of the page, then click on **Import Skillets**. 
    
    ADD IMAGE
    
    Here under the  *"Recommended Repositories"* section you should see the *"Skillet Builder Tools"* section where you can quickly
    click **Import**. 
    
    ADD IMAGE
    
    For other repositories you may want to import, you can do so at the bottom of the page under the where you can change the repository 
    name under the *"Import Repository"* section and paste the cloned git repository URL using HTTPS or SSH.
    
    ADD IMAGE

.. _SkilletBuilder: https://github.com/PaloAltoNetworks/SkilletBuilder

  : NOTE::
    This method is the standard way of importing any valid skillet repositories into PanHandler.


Running SLI
~~~~~~~~~~~

    SLI is a nifty tool that can be used to quickly interact with skillets and your NGFW through the CLI. 
    
    .. code-block:: bash
    
      > mkdir {directory name of your choice}
      > cd {directory from step above}
      > python3 -m venv ./venv (Create the venv)
      > source ./venv/bin/activate (Activate the venv)
      > pip install sli
    
    Please refer to the `SLI GitLab`_ documentation library for instructions on more in depth information on to installtion and use
    of the SLI tool in your CLI and local machine.
    
.. _`SLI GitLab`: https://gitlab.com/panw-gse/as/sli

  
     
|

Building Skillets with Set Commands
-----------------------------------

Create the Configuration in the NGFW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Before modifying the configuration, ensure you have a snapshot of the *before* configuration of your NGFW saved

    The tutorial examples use the GUI to create the external dynamic list(EDL), tag, and security rules.
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

  Configure inbound and outbound security rules referencing the tag and external-list. Note that the
  rule names are prepended with the EDL name. In later steps variables are used in the rule names to
  map the EDL and ensure rule names are unique.

.. image:: /images/configure_tutorial/configure_security_rules.png
    :width: 800

Generate the Set Commands Skillet Online Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    In PanHandler use the click on the **PanHandler** tab at the top and then click on **Skillet Repositories**. 
    
    ADD IMAGE HERE
    
    Scroll down until you find the ``SkilletBuilder`` repository and then click on the **Detail** button
    skillet to extract the difference between the baseline and modified 
    NGFW configurations. To do this in offline mode, click on the dropdown menu underneath *"Source of Changes"* and then click on 
    **"From uploaded configs"**. 
    
    ADD IMAGE HERE
   .. image:: /images/configure_tutorial/configure_skillet_generator.png
        :width: 800 
|

    You will want to have 2 XML files that you exported from your NGFW configurations on your local 
    machine. You can then upload these files to *"Base Configuration:"* and *"Modified Configuration:"* sections here. 
    You can get these 2 XML files from your NGFW by navigating to and clicking on 
    **Devices->Setup->Operations->"Export named configuration snapshot"**. Once here export the baseline and modified versions of
    the NGFW and upload them to the SkilletBuilder tool.
    
    PLACE IMAGE HERE
    
    After the files are added, the PanHandler tool will output a list of set commands that you can use to do the exact same EDL, tag 
    and security rule configurations you manually made on your NGFW UI. 
    
    PLACE IMAGE HERE
    
    Once the set commands have been outputted you want to save them by copying them and pasting them into a *.conf* file which we will
    use as a snippet within our skillet.
    
      .. NOTE::
    Order matters with set commands! The *Generate Set CLI Commands* skillet won't always output set commands in the right order. For
    example it may output the commands in such a way that it will try to load in a security policy before the EDL is created. This would
    fail if you input it into the NGFW CLI since the EDL doesn't exist yet.
    
    SHOW IMAGE OR SOMETHING THAT THIS COULD HAPPEN TO THE USER
    
    Next we are going to add the same two base and modified configuration files from before to the *Generate a Skillet* tool in
    PanHandler. Under the *Skillet Source:* section click on the dropdown menu and click on **From Uploaded Configs**. Upload the 
    base and modified files again and click on **Submit**.
    
ADD IMAGE HERE

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

  Clicking **Submit** results in a screen output of the .skillet.yaml file.

  The rendered YAML file contains:

    * preamble populated with the web form values
    * placeholder variables section
    * snippets section with XPath/element entries where each diff found


Generate the Set Commands Skillet Offline Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    In PanHandler use the :ref:`Generate Set CLI Commands` skillet to extract the difference between the baseline and modified 
    NGFW configurations. To do this in offline mode, click on the dropdown menu underneath *"Source of Changes"* and then click on 
    **"From uploaded configs"**. 
    
    ADD IMAGE HERE
   .. image:: /images/configure_tutorial/configure_skillet_generator.png
        :width: 800 
|

    You will want to have 2 XML files that you exported from your NGFW configurations on your local 
    machine. You can then upload these files to *"Base Configuration:"* and *"Modified Configuration:"* sections here. 
    You can get these 2 XML files from your NGFW by navigating to and clicking on 
    **Devices->Setup->Operations->"Export named configuration snapshot"**. Once here export the baseline and modified versions of
    the NGFW and upload them to the SkilletBuilder tool.
    
    PLACE IMAGE HERE
    
    After the files are added, the PanHandler tool will output a list of set commands that you can use to do the exact same EDL, tag 
    and security rule configurations you manually made on your NGFW UI. 
    
    PLACE IMAGE HERE
    
    Once the set commands have been outputted you want to save them by copying them and pasting them into a *.conf* file which we will
    use as a snippet within our skillet.
    
      .. NOTE::
    Order matters with set commands! The *Generate Set CLI Commands* skillet won't always output set commands in the right order. For
    example it may output the commands in such a way that it will try to load in a security policy before the EDL is created. This would
    fail if you input it into the NGFW CLI since the EDL doesn't exist yet.
    
    SHOW IMAGE OR SOMETHING THAT THIS COULD HAPPEN TO THE USER
    
    Next we are going to add the same two base and modified configuration files from before to the *Generate a Skillet* tool in
    PanHandler. Under the *Skillet Source:* section click on the dropdown menu and click on **From Uploaded Configs**. Upload the 
    base and modified files again and click on **Submit**.
    
ADD IMAGE HERE

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

  Clicking **Submit** results in a screen output of the .skillet.yaml file.

  The rendered YAML file contains:

    * preamble populated with the web form values
    * placeholder variables section
    * snippets section with XPath/element entries where each diff found

. toggle-header:: class
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

  .. TIP::
  YAML is notoriously finicky about whitespace and formatting. While it's a relatively simple structure and easy to learn,
  it can often also be frustrating to work with. A good reference to use to check that your
  YAML syntax is up to standard is the `YAML Lint site <http://www.yamllint.com/>`_.


Copy the Output to .skillet.yaml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Copy the output text under the generated skillet and paste it into the .skillet.yaml file in your personal GitHub repository.
    
    Add Image Here
    
    .. NOTE:: 
    At this point if building your own skillet you can use the :ref:`Skillet Test Tool` to play the skillet without variables. Common
    reasons for raw output testing include the possible need for snippet reordering and confirmation that the snippet elements will load

Creating the .conf File
~~~~~~~~~~~~~~~~~~~~~~~
    Since this is specifically a set commands tutorial, we now have to replace the XML output from the ``Generate A Skillet`` tool with 
    set commands. For that we will use a .conf file. In your GitHub repository create a file and name it something like
    ``set_commands_tutorial.conf``. Now take all the generated set commands from before and paste them into this file.
    
    ADD IMAGE HERE

    We are going to use this .conf file within our skillet file's ``snippets`` section. You can now delete all of the current snippets
    within the current skillet file as we will be replacing the snippets with our .conf file.
    
    ADD IMAGE HERE


Organizing the .conf File
~~~~~~~~~~~~~~~~~~~~~~~~~

    Now that the set commands are all within the .conf file it can be useful to organize them into sections. For example a tag section,
    an external-list section and a security rules section. This will help make the file more readable and will allow us to make sure the
    workflow looks right.
    
    ADD IMAGE HERE

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





