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
  * `Initializing a New Repository and Working with SSH Keys`_
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
  

NGFW
~~~~

    This is the device that we will be working with and configuring during the tutorial. 

    **Baseline Configuration:** It is recommended to capture a *baseline* configuration of your newly brought up and pre-configured
    firewall. This is especially useful for testing purposes if you wish to quickly revert any changes made on the NGFW back to a
    blank slate. This can be done on the NGFW UI via *Devices->Setup->Operations->Save* named configuration snapshot*.
    
    .. NOTE::
    Some skillet configuration elements may be version specific and require unique skillets per software releases. Verify that your
    NGFW **Software Version** is compatible with associated skillets.


Working on the NGFW with the CLI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This section is for users who are interested in learning how to configure the firewall through the CLI. 

    The command below will help you understand how to log into the NGFW through the CLI, but please also refer to this
    supplemental article_ for more in depth guidance on using the CLI with the NGFW. For information on making configurations on
    the NGFW through the CLI please refer to this `knowledgebase article`_.

    .. NOTE::
      If you are logging into the NGFW for the first time via CLI, you may need to authorize the ECDSA key fingerprint. Type 'yes' 
      before continuing.

    .. code-block:: bash
      
      $ ssh {username}@{X.X.X.X}
      
    
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
  
  

Working with GitHub, PanHandler and SSH Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Here we will be walking through logging into GitHub, creating and adding a repository to our GitHub account as well as some
    GitHub best practices to keep in mind.

:ref:`The Skillet Framework` uses Github as the primary option for storing skillets.

  Log in to Github and click the small **+** sign in the upper right corner of your screen and click on **New repository** to add 
  a new repo.
  
    .. image:: /images/set_command_tutorial/New_repo_github.png
        :width: 600

  Suggestions are to include a README file and MIT license.

UPDATE IMAGE
    .. image:: /images/configure_tutorial/create_new_repo_fields.png
        :width: 600

  Once created, click on the green **Code** button and underneath the ``Clone`` section click on **SSH**. Then click on the small
  **clipboard** sign on the right of the SSH URL to copy the SSH key. Remember this step as we will circle back to this a little
  later in the tutorial.

UPDATE IMAGE
    .. image:: /images/configure_tutorial/clone_new_repo.png
       :width: 600


  Next we want to clone this repository into PanHandler using the SSH key we have copied. Open up the PanHandler UI now and click
  on the dropdown menu in the top right of the browser that says **paloalto**, from the dropdown click on **View SSH Public Key**.
  
  ADD IMAGE HERE
  
  This will take you to an ``SSH Public Key`` Page that has the ``ssh-rsa`` for you to copy. copy the whole block of text including 
  ``ssh-rsa``.
  
  ADD IMAGE HERE
  
  Now navigate back to your GitHub page and click on your user bubble on the top right corner of the browser, it should be to the
  right of the ``+`` sign we clicked on before. From the dropdown menu click on **settings**. 
  
  ADD IMAGE HERE
  
  On the left menu bar you want to click on **SSH and GPG Keys**. Then click on the green **New SSH key** and title it
  ``PanHandler``. Paste the ``SSH Public Key`` we got from PanHandler earlier here and then click the green **Add SSH key**.
  
  ADD IMAGE HERE
  
  Upon finishing this step you should be able to import your newly created repository into PanHandler using SSH keys. go back to
  PanHandler and click on the **PANHANDLER** drop down at the top left corner and the select **Import Skillets** from the menu.
  
  ADD IMAGE HERE
  
  Finally, at the bottom of the page under the ``Import Repository`` section you can choose your ``Repository Name`` and enter 
  in the SSH Key that you got from your GitHub repo from the earlier step.
  
  ADD IMAGE HERE
  
  After this step you should be able to view your newly imported repository in PanHandler!
  
  ADD IMAGE HERE
 
  .. NOTE::
    If your account or repo is set up requiring 2-factor authentication then you should clone using the SSH link instead.
    This is required to push configuration changes back to the repo.  You may have to `add an SSH key for Github`_
    
  .. NOTE::
    Please reference this `PanHandler Link`_ for more information on working with private git repositories and SSH keys in
    PanHandler. Please click on the side bar sections labeled **Adding a New Skillet Repository -> Using a Private Git Repository**.

.. _add an SSH key for Github: https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh    
.. _`PanHandler Link`: https://panhandler.readthedocs.io/en/master/using.html#adding-a-new-skillet-repository
    
    
Create the File Structure for the Project in GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  In your Terminal open the repo directory that was just cloned by doing the following commands and add the following folders:
  
  .. code-block:: bash

      $ cd {Directory of cloned repo}
      $ vim 

    * A new folder that will contain the skillet content (eg. tag_edl_block_rules)
    * In the new folder add an empty ``.skillet.yaml`` file 
    
        * The contents of the file will be populated later in the tutorial
    * in the new folder add an empty README.md file 
    
        * The contents of the file will be populated later in the tutorial

  The skillet directory structure will look like:

UPDATE THIS IMAGE

  .. image:: /images/configure_tutorial/configure_skillet_folder.png
     :width: 250
  
  
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

    Before modifying the configuration, ensure you have a snapshot of the `before` configuration of your NGFW saved, we will use
    this saved snapshot to perform an offline configuration difference later. To do this click on the **Devices** tab of your NGFW,
    then click on the **Setup** tab and then the **Operations** tab. Here you can click on **Save named configuration snapshot** to
    save the current NGFW config.
    
    .. image:: /images/set_command_tutorial/save_config_snapshot.png
        :width: 600

    The tutorial examples use the GUI to create the external dynamic list(EDL), tag, and security rules. Before starting these steps,
    make sure you commit whatever most recent changes were made to your NGFW, to do this click on the **Commit** button at the top.
    right of the NGFW GUI.
    
    .. image:: /images/set_command_tutorial/commit_button.png
        :width: 600
    
    Now after commiting we want to start making changes to our NGFW. First we want to configure the external-list object with a name,
    description, and source URL and then click the **OK** button to save the changes. To get to the `External Dynamic List` section
    on your NGFW navigate through the following, **Objects->External Dynamic Lists->Add**. 


    .. image:: /images/set_command_tutorial/External_list.png
        :width: 600


    .. image:: /images/set_command_tutorial/edl_configure.png
        :width: 600

|

    Next we need to configure the tag object with a name, color, and comments (description) and then click the **OK** button. Tag
    objects are found by clicking through the following, **Objects->Tags->Add**.
    
    .. image:: /images/set_command_tutorial/find_tag.png
        :width: 400


    .. image:: /images/set_command_tutorial/tag_configure.png
        :width: 400

|

    .. TIP::
        The skillet will only add a single tag to the configuration.
        However, the GUI shows a color name while the XML data in the NGFW is based on a color number.
        The use of multiple tag entries is used to extract the color values.
        So note that in some cases the GUI and XML can use different values and we can use sample configs
        like this to discover those values.

|

  Configure inbound and outbound security rules referencing the tag and external-list. In order to add Security rules please
  navigate through the following, **Policy->Security->Add**. Note that the rule names are prepended with the EDL name. In later 
  steps variables are used in the rule names to map the EDL and ensure rule names are unique.


  .. image:: /images/set_command_tutorial/navigate_security_policy.png
      :width: 400
        

  .. image:: /images/set_command_tutorial/security_policy_add.png
      :width: 400
    
  If you want to be able to generate your set commands skillet in offline mode don't forget to save a modified configuration
  snapshot of your NGFW here just like we did earlier in this section.


Generate the Set Commands Skillet Online Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    In this section of the tutorial we are going to use an online NGFW and PanHandler to create a set commands skillet. Start up
    PanHandler and click on the **PanHandler** tab at the top and then click on **Skillet Repositories**. 
    
    .. image:: /images/set_command_tutorial/panhandler_nav.png
        :width: 400
    
    Scroll down until you find the `SkilletBuilder` repository and then click on the **Details** button. 
    
    .. image:: /images/set_command_tutorial/panhandler_nav.png
        :width: 400
    
    Here you want to locate and click on the **Create Skillet** button.
    
    .. image:: /images/set_command_tutorial/create_skillet.png
        :width: 400
    
    
    skillet to extract the difference between the baseline and modified  NGFW configurations. To do this in offline mode, click on
    the dropdown menu underneath *"Source of Changes"* and then click on 
    **"From uploaded configs"**. 
    
    ADD IMAGE HERE
   .. image:: ../images/configure_tutorial/configure_skillet_generator.png
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

    In this section of the tutorial we are going to use an offline NGFW configuration files and PanHandler to create a set commands
    skillet. Start up PanHandler and click on the **PanHandler** tab at the top and then click on **Skillet Repositories**. 
    
    ADD IMAGE HERE
    
    Scroll down until you find the ``SkilletBuilder`` repository and then click on the **Details** button.  
    
    ADD IMAGE HERE
    
    Here you want to locate and click on the **Create Skillet** button.
    
    Now we want to extract the difference between the baseline and modified NGFW configurations as set commands. To do this in
    offline mode, find the box on this page that says ``Generate Set Commands From Uploaded Files`` and then click on **Upload**.
    
    ADD IMAGE HERE
    
    Now we will be at a page labeled ``Skillet Generator``. Here we will upload our base and modified configuration files we saved
    earlier in the tutorial.
    
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





