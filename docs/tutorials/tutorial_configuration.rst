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



