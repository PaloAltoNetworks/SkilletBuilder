Configuration
=============

Overview
--------

This tutorial is designed to help the user build an introductory configuration skillet. The tutorial will showcase
PanHandler, along with several SkilletBuilder tools that assist the user in creating, editing, and testing skillets.
The configuration tutorial will create a simple configuration including:

  - An IP External Dynamic List (EDL) object
  - A Tag object
  - Security rules (Inbound and Outbound) referencing the EDL and tag objects

The video provides an end-to-end perspective for building a configuration skillet as a complement
to the documentation content.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=17392613-262a-4606-a11a-ab6c010b894e&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

|

Click below to jump to a specific section of the tutorial:

1. `Prerequisites`_

2. `Set Up Your Environment`_

3. `Build the Skillet`_

4. `Test and Troubleshoot`_

5. `Document`_


Prerequisites
-------------

Before moving forward with the tutorial, you will need the following:

- NGFW up and running with proper access to GUI and CLI(via SSH)
- A `GitHub <https://github.com/>`_ account with access permissions to edit repository content
- `Docker <https://www.docker.com/>`_ desktop installed and running on your local machine

- Access to the following repositories:

    - `PanHandler <https://github.com/PaloAltoNetworks/panhandler/>`_

- For users interested in working through the command line, have `SLI <https://pypi.org/project/sli/>`_ installed on your local machine

    - SLI is a CLI interface for interacting with Skillets. Please refer to the link above to learn about SLI and get started.

It may also be useful to review the following topics before getting started:

- :ref:`XMLandSkillets`
- :ref:`jinjaandskillets`


Set Up Your Environment
-----------------------

In this section of the tutorial we will set up everything you need to successfully complete the tutorial.

NGFW
~~~~

  This is the device that we will be working with and configuring during the tutorial.

  .. NOTE::
    Some skillet configuration elements may be version specific and require unique skillets per software release.
    Verify that the **Software Version** and associated skillets are compatible.

  **Baseline Configuration**

  Before making any configuration changes, it is recommended to save a 'baseline' configuration file. This will make
  it easier to rollback the NGFW for testing and demonstration purposes.


Start PanHandler
~~~~~~~~~~~~~~

  PanHandler is a utility that is used to create, load, and view configuration templates and workflows.

  In order to access the latest stable version of PanHandler, open a terminal/bash shell and enter the command below:

  .. code-block:: bash

    curl -s -k -L http://bit.ly/2xui5gM | bash

  Once that is finished running, navigate to the URL below using a web browser (Chrome, Firefox, Safari, etc):

  .. code-block:: bash

    http://localhost:8080

  The credentials to log into the PanHandler interface are 'paloalto'[Username] and 'panhandler'[Password]

  Please refer to the `PanHandler documentation <https://panhandler.readthedocs.io/en/master/overview.html/>`_
  for more detailed information on the PanHandler utility.

  **add section for PanHandler SSH key into github**

Restart PanHandler
~~~~~~~~~~~~~~~~~~

  If you already installed PanHandler, you will eventually need to restart the container.

  Navigate to the Docker Desktop Application on your local machine. You should see the 'panhandler' container listed on
  the dashboard.

  **INSERT PIC HERE**

  Click 'Start' to restart the container. You should now be able to access the PanHandler GUI at the same URL as before:

.. code-block:: bash

    http://localhost:8080


Initialize a New Repository and Import it into PanHandler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`The Skillet Framework` uses Github as the primary option for storing skillets.

  Log in to Github and select ‘New’ to add a new repo.

    .. image:: /images/configure_tutorial/create_new_repo_button.png
        :width: 600

  Suggestions are to include a README file and MIT license. You can also add a .gitignore file, primarily to ignore
  pushing any EDI directories such as .idea/ used by Pycharm.

    .. image:: /images/configure_tutorial/create_new_repo_fields.png
        :width: 600

  Once created, copy the clone URL from the GUI.
  This is found with the green ‘Code’ button and is NOT the browser URL.

    **INSERT PIC HERE**

  Navigate back to PanHandler. Click the PanHandler dropdown menu in the top left corner and select 'Import Skillets'.

  **INSERT PIC HERE**

  Scroll down the page and locate the 'Import Repository' Section. Enter the name of the repository and paste the URL
  you copied from the above step. Click 'Submit'.

  **INSERT PIC HERE**

  .. NOTE::
    If your account or repo is set up requiring 2-factor authentication then you should clone using the SSH link instead.
    This is required to push configuration changes back to the repo.  You may have to `add an SSH key for Github`_

.. _add an SSH key for Github: https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent


Install SLI
~~~~~~~~~~~

In a terminal/bash shell enter the following to create a virtual python environment and install SLI.

.. code-block:: bash
  > mkdir {directory name of your choice}
  > cd {directory from step above}
  > python3 -m venv ./venv (Create the venv)
  > source ./venv/bin/activate (Activate the venv)
  > pip install sli

  Please refer to the `SLI Documentation <https://pypi.org/project/sli/>`_ for more information on installing and using SLI

Build the Skillet
--------------------

Now that everything is set up and ready to go, we can begin building the skillet.


Create the Configuration in the NGFW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Before modifying the configuration, ensure you have a snapshot of the 'before/baseline' configuration.

  Navigate to Device > Setup > Operations.

  **INSERT PIC HERE**

  Click 'Save named configuration snapshot', enter a name for the file (ex. baseline.xml), and click OK.

  **INSERT PIC HERE**

  The tutorial examples use the GUI to create the EDL, tag, and security rules.
  Many of the config values are placeholders that look like variable names (hint, hint).
  You can also load the :ref:`Sample Configuration Skillet` found in the Skillet Builder collection.

  Navigate to Objects > External Dynamic Lists
  Click 'Add' at the bottom of the page

  Configure the external-list object with a name, description, and source URL.

  .. image:: /images/configure_tutorial/configure_edl.png
     :width: 600


  |


  Navigate to Objects > Tags
  Click 'Add' at the bottom of the page

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

  Navigate to Policies > Security
  Click 'Add' at the bottom of the page

.. image:: /images/configure_tutorial/configure_security_rules.png
    :width: 800


  Follow the screenshots below to edit the security policy rules. You can assume the default settings if they are not present below.

  **INSERT PIC HERE**

  Commit the changes you just made and save the configuration file.
  Navigate back to Device > Setup > Operations and 'Save named configuration snapshot' again, but name the file something you
  will remember (ex. skilletbuilder.xml).

  **INSERT PIC HERE**

  Export both the 'baseline' configuration file and the file you just saved to your local machine.

  **INSERT PIC HERE**


Generate the Skillet from Uploaded Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  In the PanHandler dropdown menu, click 'Skillet Repositories' and locate the skillet repository that you imported in an
  above step. Click 'Details'.

  **INSERT PIC HERE**

  Click either of the 'Create Skillet' buttons on the page.

  **INSERT PIC HERE**

  Locate the section 'Generate From Uploaded Files' and Click 'Upload'.

  **INSERT PIC HERE**

  Recall the two configuration files that you exported in an above step. Upload the 'baseline' or pre-configuration file
  in the pre-configuration section. Upload the post-configuration file in the section below. Click 'Submit'.

  **INSERT PIC HERE**


  Edit the Initial Config Settings for the Skillet. Here are some suggested inputs for this tutorial:

  - Skillet ID [must be unique]: Tutorial_Skillet_New
  - Skillet Label: Tutorial Skillet
  - Skillet Description: Skillet generated from uploaded files/configs
  - Skillet Type: PAN-OS
  - Branch: local
  - Commit Message: Create New Skillet

  **INSERT PIC HERE**

  To continue on with the tutorial click to go to the next section: `Add Variables to Snippets`_

Generate the Skillet from PAN-OS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  **SKIP**

Generate the Skillet with SLI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer to use the command line, SLI can also extract the difference between two configuration files.
**add pics and more context**


Add Variables to Snippets
~~~~~~~~~~~~~~~~~~~~~~~~~

  Within the Skillet Editor, you should see the all the settings you input in the previous step. Scroll down to the
  'Snippets' section; it should be pre-populated with snippets from the configuration files. These snippets represent
  the pieces of the NGFW configuration that were found to be different between the two files uploaded.

  **INSERT PIC HERE**

  Click the 'Edit' button to the far right of the external-list snippet.

  **INSERT PIC HERE**

  On the 'Edit PAN-OS Snippet' Page click the 'Edit' button in the bottom right corner.

  **INSERT PIC HERE**

  In this editor you can use the 'Text to Replace' feature at the bottom of the page to create the variables.

  **INSERT PIC HERE**

  Locate the 'entry name' element and enter 'edl_name' in both text boxes at the bottom of the page.

  **INSERT PIC HERE**

  On the right side, click this symbol **INSERT PIC HERE**
  This will change the variable to align with Jinja formatting.
  You should see the set of curly brackets appear around the variable name.

  **INSERT PIC HERE**

Local Skillet Test
~~~~~~~~~~~~~~~~~~

  Before pushing the skillet to Github, use the :ref:`Skillet Test Tool` to validate the final YAML file formatting
  and variable additions. Paste the contents of the YAML file into the test tool and submit. This will play the skillet
  using the default variable values. Check that the configuration loaded into the NGFW.

  Common errors at this stage likely include YAML formatting issues, snippet ordering problems, or a variable typo.

Testing with SLI
~~~~~~~~~~~~~~~~

  **add content here**

Push the Skillet to Github
~~~~~~~~~~~~~~~~~~~~~~~~~~



Test and Troubleshoot
------------------


Play the Skillet
~~~~~~~~~~~~~~~~

  From the Detail or Collection view, play the skillet. Although you may have tested with the Test Tool,
  playing the imported skillet allows the builder to review the Web UI elements presented to the user.

  .. image:: /images/configure_tutorial/configure_skillet_play.png
     :width: 800


|

  .. TIP::
    In order to save time in the testing phase, choose *Do not commit. Push changes only* in the Commit options.

  Before pushing the configuration to the device, you can use the ``Debug`` option to view the rendered skillets.
  This view is used to validate variable substitutions and XML formatting.

  .. image:: /images/configure_tutorial/configure_skillet_debug.png
     :width: 800


  Check both the output messages in PanHandler and actual NGFW view to test the skillet. Also verify that the
  configuration loads as candidate and will also commit. If you receive errors messages, common issues may be:

    - Snippet load order
    - Variable typos in the snippet section or not included in the variables section
    - Invalid input data that passes web form validation but not NGFW validation checks

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
    To view markdown edits in existing GitHub repos, click on the README.md file, then use the ``Raw``
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

