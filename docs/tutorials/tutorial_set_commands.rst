Basic Configuration With Set Commands
=====================================


Overview
--------

This tutorial is designed to help the user get familiar with using set commands to bring up and apply basic configs to their NGFW. By then end of this tutorial the user should be able to alter their firewall manually through the Command Line Interface(CLI) with set commands. All set/op commands that can be entered in the CLI manually can also be transformed into an automation playlist in the form of a skillet. This allows the user to run a series of set commands to easily configure their NGFW with just the click of a button.

This Basic Config with Set Commands tutorial will show the user how to:

* Access and configure the Next Generation Firewall(NGFW) through the web UI and CLI
* Capture configuration differences made on the NGFW into set commands and automation skillets
* Learn how to use Panhandler tooling
* Learn how to use the Skillet Line Interface(SLI) tool on the CLI
* Learn the basics of using GitHub and repositories

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

2. `Set Up Your Environment`_

3. `Building Skillets with Set Commands`_

4. `Test and Troubleshoot`_

5. `Document`_


Prerequisites
-------------

Before moving forward with the tutorial, please ensure the following prerequisites have been fulfilled.

* Have an up and running NGFW Virtual Machine(VM)
* A GitHub_ account with access permissions to edit repository content
* Docker_ desktop installed, active and running on your machine
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
.. [1] PyCharm or SublimeText are good options for a beginner IDE or text editor.
.. [2] Log in to the NGFW UI by entering this, *https://XXX.XXX.XXX.XXX* (with your NGFW's management IP replacing the X's), into the web browser URL bar.
.. [3] If you reach a warning page during this step, click advanced settings and choose the proceed to webpage option.
.. [4] Log in to the NGFW via CLI by opening a terminal/bash window on your local machine and entering this, *ssh {username}@{X.X.X.X}* (with your NGFW's management IP replacing the X's).

This tutorial will be split into 4 main sections below and can either be done by reading the document or by watching the tutorial videos. There is a video tutorial for achieving the intended results via use of the PanHandler UI tool and the SLI command line interface tool.


Set Up Your Environment
-----------------------

In this section we will set up everything that will be needed to successfully complete the tutorial. 


NGFW
~~~~

    This is the device that we will be working with and configuring during the tutorial. Be sure that you are able to log into the
    firewall UI by inputting its management IP into the web browser. When logged in it can be useful to do a number of things.

    **Software Version:**
    Please take note of the devices software version when traversing this tutorial. Some configuration elements may be version
    specific and require unique skillets per software releases.

    **Baseline Configuration:** It is recommended to capture a *baseline* configuration of your newly brought up and pre-configured
    firewall. This is especially useful for testing purposes if you wish to quickly revert any changes made on the NGFW back to a
    blank slate. This can be done on the NGFW UI via *Devices->Setup->Operations->Save* named configuration snapshot*.

    **API Access**
    Login credentials with API access to test playing Skillets and any changes made by using set commands.


Having the CLI 'Set Command Ready'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This tutorial will use the Skillet Generator tool to create automation workflows to alter the NGFW configuration, but it is also
    useful to know how to configure the firewall through the CLI. 

    These operations commands below will help you get started with basic configurations but please also refer to this supplemental
    article_ for more guidance on using the CLI with the NGFW.

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
  
  .. code-block:: bash
  
    > curl -s -k -L http://bit.ly/2xui5gM | bash
  
  Then you want to input the following into your browsers URL.
    
  .. code-block:: html
  
    http://localhost:8080

  Please refer to the `PanHandler documentation`_ for more detailed information on the many useful functions of the PanHandler utility.
  
.. _`PanHandler documentation`: https://panhandler.readthedocs.io/en/master/overview.html
  
  
Importing SkilletBuilder Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This section will go over how to import skillet repositories to PanHandler.

    
    Once you have gained access to the PanHandler UI you will want to import the SkilletBuilder_ repository. This is done by clicking
    the **PanHandler** drop down menu at the top of the page. Then click on **Import Skillets** and here under the 
    *"Recommended Repositories"* section you should see the *"Skillet Builder Tools"* section where you can quickly click **Import**. 
    
    For other repositories you may want to import, you can do so at the bottom of the page under the where you can change the repository 
    name under the *"Import Repository"* section and paste the cloned git repository URL using HTTPS or SSH.

.. _SkilletBuilder: https://github.com/PaloAltoNetworks/SkilletBuilder


Running SLI
~~~~~~~~~~~

    SLI is a nifty tool that can be used to quickly interact with skillets and your NGFW through the CLI. 
    
    Please refer to the `SLI PyPi`_ documentation library for instructions on how to install and use the SLI tool in your CLI.
    
.. _`SLI PyPi`: https://pypi.org/project/sli/

Setting Up GitHub
~~~~~~~~~~~~~~~~~

    Here we will be walking through logging into GitHub, creating and adding a repo as well as some GitHub best practices to keep in mind.

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
    

Create the File Structure for the Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This model places the set command elements within the .skillet.yaml file. This is the standard output used by the Skillet Generator.

  In the editor open the repo directory that was just cloned and add the following:

    * a new folder that will contain the skillet content (eg. tag_edl_block_rules)
    * in the new folder add an empty ``.meta-cnc.yaml`` file 
    
        * The contents of the file will be populated later in the tutorial
    * in the new folder add an empty README.md file 
    
        * The contents of the file will be populated later in the tutorial

  The skillet directory structure will look like:

  .. image:: /images/configure_tutorial/configure_skillet_folder.png
     :width: 250
     

Skillet Editor
~~~~~~~~~~~~~~

    The IDE should be ready with:
    
    * A full view of files and directories in the skillet
    * Text editor that supports YAML and XML file types
    * Terminal access to interact with Git/Github
    
|

Building Skillets with Set Commands
-----------------------------------

Create the Configuration in the NGFW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Before modifying the configuration, ensure you have a snapshot of the *before* configuration of your NGFW saved

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


Generate the Set Commands Skillet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    In PanHandler use the :ref:`Generate Set CLI Commands` skillet to extract the difference between the baseline and modified 
    NGFW configurations. To do this in offline mode, click on the dropdown menu underneath *"Source of Changes"* and then click on 
    **"From uploaded configs"**. 
    
    .. image:: /images/configure_tutorial/configure_skillet_generator.png
        :width: 800
|

    You will want to have 2 XML files that you exported from your NGFW configurations on your local 
    machine. You can then upload these files to *"Base Configuration:"* and *"Modified Configuration:"* sections here. 
    You can get these 2 XML files from your NGFW by navigating to and clicking on 
    **Devices->Setup->Operations->"Export named configuration snapshot"**. Once here export the baseline and modified versions of
    the NGFW and upload them to the SkilletBuilder tool.
    
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





