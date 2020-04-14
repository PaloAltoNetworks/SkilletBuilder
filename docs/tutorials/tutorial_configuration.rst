Configuration
=============

Overview
--------

This tutorial is aimed at novice skillet builders who want to work through building a sample skillet.

Content is grouped into 4 basic sections specific to each task category:

1- Set up the sandbox
~~~~~~~~~~~~~~~~~~~~~

  Prepare your skillet building and testing environment.

  * NGFW or Panorama up and running
  * GUI, SSH, and API access to the device
  * panhandler running with the SkilletBuilder tools imported
  * IDE (Integrated Development Environment) such as Pycharm or VS Code
  * Github account with access permissions to edit repository content

2- Build the skillet
~~~~~~~~~~~~~~~~~~~~

  Edit the .meta-cnc.yaml file to create the skillet

  * Add the github repo and clone to edit
  * create an empty .meta-cnc.yaml file
  * create 'before and after' configuration snapshots
  * Use the :ref:`Generate a Skillet` tool to create the initial skillet
  * Add the variables
  * commit and push to Github

3- Test and troubleshoot
~~~~~~~~~~~~~~~~~~~~~~~~

  Test against a live device and Fix/Tune as needed.

  * Use the :ref:`Skillet Test Tool` to quick test the skillet
  * Import the skillet into panHandler to test web UI and config loading
  * Fix any UI or loading errors
  * Tune the web UI, configuration elements


4- Document and Share
~~~~~~~~~~~~~~~~~~~~~

  The final and important steps are good documentation and sharing with the community.

  * READme.md documentation in the Github repo
  * Skillet District posting
  * Others can now import into their tools and use the new skillet

|

Configuration Tutorial Elements
-------------------------------

The configuration tutorial will create a simple configuration including:

  * an IP External Dynamic List (EDL) object
  * a Tag object
  * Security rules (Inbound and Outbound) referencing the EDL and tag objects

|

Setting up the Sandbox
----------------------

The skillet sandbox specific to this NGFW configuration will consist of 4 basic elements: the NGFW, panHandler,
the Skillet Builder tools, and the creation/editor environment.

NGFW
~~~~

  This is the device to be configured.

  **Software Version**
  Note the software version of the configuration device and associated skillets.
  Skillets configuration elements may be version specific require unique skillets per software release.

  **Baseline Configuration**
  Recommendation to save a configuration file as ‘baseline’ for easy rollback for generation, testing, and demonstration.

  **API Access**
  Login credentials with API access to test playing the skillet

Having the CLI ‘XML Ready’
~~~~~~~~~~~~~~~~~~~~~~~~~~

  The tutorial will use the Skillet Generator but later stages of testing and tuning may require review and capture
  of the XPath or XML elements. These operations commands make the CLI XML-ready:

  .. code-block:: bash

      admin@PA-VM> set cli config-output-format xml
      admin@PA-VM> debug cli on

  The first command will display configuration data as XML and the second will allow for easy capture of the configuration XPath.
  Review the :ref:`XML Basics` if you are not familiar with XML concepts.


PanHandler
~~~~~~~~~~

  PanHandler will be used to generate and test the skillet.

  Use the curl command found in :ref:`Updating or Running the Master Version` if panHandler is not installed or not running
  the latest version.


Skillet Builder Tools
~~~~~~~~~~~~~~~~~~~~~

  In panHandler import the :ref:`Skillet Builder Tools` repo.

Prepare the Skillet Edit Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  The IDE should be ready with:

  * a full view of files and directories in the skillets
  * text editor that supports YAML and XML file types
  * console access to interact with Git/Github

Building the Skillet
--------------------

The following steps take the user from creating the Github repo, through generating and editing the skillet, to a final
push or skillet content back to the created repo.

Creating a New Repo and Cloning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  :ref:`The Skillet Framework` uses Github as the primary option for storing skillets.

  Log in to Github and select ‘New’ to add a new repo.

.. image:: images/create_new_repo.png
   :width: 800
   :align: center

  Suggestions are to include a README file and MIT license. You can also add a .gitignore file, primarily to ignore
  pushing any EDI directories such as .idea/ used by Pycharm.

  Once created, copy the clone URL from the GUI.
  This is found with the green ‘Clone or download’ button and NOT the browser URL.

.. image:: images/clone_new_repo.png
   :width: 800
   :align: center

  Using a local console or your editor tools, clone the repo to your local editor. For example, using the console and the link above:

  .. code-block:: bash

      midleton$ git clone https://github.com/scotchoaf/SBtest.git

  .. NOTE::
    If your account or repo is set up requiring 2-factor authentication then you should clone using the SSH link instead.
    This is required to push configuration changes back to the repo.  You may have to `add an SSH key for Github`_

.. _add an SSH key for Github: https://help.github.com/en/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent


Create the Configuration in the NGFW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Before modifying the configuration, ensure you have a snapshot of the current configuration.

  The tutorial examples use the GUI to create the EDL, tag, and security rules.
  Many of the config values are placeholders that look like variable names (hint, hint).

  .. NOTE::
    You can also opt to load the :ref:`Sample Configuration Skillet` found in the Skillet Builder collection.

  This tutorial configuration is designed to show a simple real-world scenario with a set of configuration elements
  that span the GUI. It also has elements that reference one another: the security policies point to tag and EDL names.


  **EDL configuration**


.. image:: images/configure_edl.png
   :width: 800
   :align: center


  **Tag configuration**


.. image:: images/configure_tag.png
   :width: 800
   :align: center


    .. NOTE::
        The skillet will only add a single tag associated to the EDL name.
        However, the GUI shows a color name while the XML data in the NGFW is based on a color number.
        The use of multiple tag entries is used to extract the color values.
        So note that in some cases the GUI and XML can use different values and we can use sample configs like this to discover those values.


  **Security Policy configuration**

  .. image:: images/configure_security_rules.png
     :width: 800
     :align: center

  This is an example 2-rule configuration based on the EDL and tags.
  The rule names are prepended with the EDL name so we can add multiple EDLs with unique rules.

  At this stage, the configuration is in the firewall and the repo is cloned locally.
  Now its time to start putting the pieces together.

Create the Project Skeleton Structure for XML
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  This model places the XML elements within the .meta-cnc.yaml file. This is the standard output used by the
  Skillet Generator.

  In the editor open the repo directory and add the following:

    * add a new folder that will contain the skillet content (eg. SBtest)
    * in the new folder add an empty ``.meta-cnc.yaml`` file (will populate the text later)
    * in the new folder add an empty README.md file (will populate the text later)

  .. image:: images/configure_skillet_folder.png
     :width: 800
     :align: center

 This is the directory structure for the tutorial configuration skillet.

Generate the Skillet
~~~~~~~~~~~~~~~~~~~~

  In panHandler use the :ref:`Generate a Skillet` skillet to extract the difference between the baseline and
  modified coniguration with offline mode.

  .. image:: images/configure_skillet_generator.png
     :width: 800
     :align: center

  After the files are added, the next stage of the workflow is a web form for the YAML file preamble attributes.

  .. image:: images/configure_skillet_preamble.png
     :width: 800
     :align: center

  Suggested tutorial inputs:

    * Skillet ID: tag_edl_tutorial
    * Skillet Label: Tutorial skillet to configure tag, EDL, and security rules
    * Skillet description: The tutorial skillet demonstrates the use of various config snippets and variables
    * Collection Name: Tutorial
    * Skillet type: ``panos``

Copy the Output to .meta-cnc.yaml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Copy the output text under **Generated Skillet** and paste into the .meta-cnc.yaml file.

  The YAML file contains:

    * preamble populated with the web form values
    * placeholder variables section
    * snippets section with XPath/element entries where each diff found

  .. NOTE::
        At this point if building your own skillet you can use the :ref:`Skillet Test Tool` to play
        the skillet without variables. Common reasons for raw output testing include the need for snippet reordering
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


  For the tutorial, the external-list element has 3 variables (name, description, url)
  that are added into the configuration resulting in:

  .. image:: images/configure_skillet_edl_vars.png
     :width: 800
     :align: center

  Note that the <recurring> value is static as ``five-minute`` without a variable.
  Some values may remain static as a best practice or, as with type ``<ip>``, specific to the configuration requirement.

  The tag also has 3 variables (name, description, color)

  .. image:: images/configure_skillet_tag_vars.png
     :width: 800
     :align: center

  Lastly, the security rules leverage EDL and tag variables (edl name, tag name) as a connected set of template configs.

  .. image:: images/configure_skillet_rules_vars.png
     :width: 800
     :align: center

  In this outbound rule example, not only are the variables used for the standard destination address and tag fields,
  but text substitution can also be used to create unique entries. In this case, the EDL name is used as
  a security rule name prefix joined with ‘-out’.

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

  From here, edit the variables section of the YAML file. Note that 5 of 6 are text while color is using a dropdown.
  The dropdown is useful when the GUI and XML use different values or limited choices are offered.

  .. image:: images/configure_skillet_rules_vars.png
     :width: 800
     :align: center

  The values for the tag color require color numbers and not the Web UI presented names. This is common for many dropdown
  selections in the Web UI. For these types of situations, you can create a set of items (eg. tags)
  to be displayed in the XML output to match Web UI and XML required values.

  For the tag color values, below is the config showing the 3 color values for green, orange, and red.
  Additional colors can be extracted by using the GUI to create more tags and then use the CLI and ‘show tag’
  to see additional color numbers.

  .. image:: images/configure_skillet_tag_colors.png
     :width: 800
     :align: center

Local Skillet Test
~~~~~~~~~~~~~~~~~~

  Before pushing the skillet to Github, use the :ref:`Skillet Test Tool` to validate the final YAML file formatting
  and variable additions. Paste the contents of the YAML file into the test tool and submit. This will play the skillet
  using the default variable values. Check that the configuration loaded into the NGFW.

Push the Skillet to Github
~~~~~~~~~~~~~~~~~~~~~~~~~~

  At this stage initial building is complete. The YAML file preamble, variables, and snippets sections all have
  relevant content added. Now we want to push this to Github for additional testing and tuning.

  .. code-block:: bash

    TODO: insert the git add/commit/push commands

  The skillet now resides in Github.

  .. image:: images/configure_skillet_repo_updated.png
     :width: 800
     :align: center

Testing and Tuning
------------------

Now that the skillet has been pushed to Github, the skillet can be imported to panHandler to test the user experience.

Import the Skillet
~~~~~~~~~~~~~~~~~~

  Use ``Import Skillets`` with the ``Clone or download`` Github URL to import to panHandler.

  .. image:: images/configure_skillet_import.png
     :width: 800
     :align: center

  View the skillet ``Detail`` from the ``Skillet Repositories`` page.

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

  Check both the output messages in panHandler and actual NGFW view to test the skillet. Also verify that the
  configuration loads as candidate and will also commit. If you receive errors messages, common issues may be:

    * snippet load order
    * variable typos in the snippet section or not included in the variables section
    * invalid input data that passes web form validation but not NGFW validation checks

Edit, Push, Test
~~~~~~~~~~~~~~~~

 If errors are found, repeat the steps above until a clean skillet can be loaded and committed.

Documentation
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



  **Support Policy Text**
  Skillets are not part of Palo Alto Networks supported product so the policy text is appended to the
  README file to specify skillets are not supported. Sample text to copy/paste is found in the `SkilletBuilder repo README`_:

  .. _SkilletBuilder repo README: https://raw.githubusercontent.com/PaloAltoNetworks/SkilletBuilder/master/README.md

Live Community
~~~~~~~~~~~~~~

  Skillets can be shared in the Live community as Community or Personal skillets. Community Skillets
  are expected to have a higher quality of testing, documentation, and ongoing support. Personal skillets
  can be shared as-is to create awareness and eventually become upgraded as Community Skillets.

