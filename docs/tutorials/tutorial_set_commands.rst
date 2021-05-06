Basic Config With Set Commands
==============================

Overview
--------

This tutorial is designed to help the user get familiar with using set commands to bring up and apply basic configs to their NGFW. By then end of this tutorial the user should be able to alter their firewall manually through the Command Line Interface(CLI) with set commands. All set/op commands that can be entered in the cli manually can also be transformed into an automation playlist in the form of a skillet. This allows the user to run a series of set commands to easily configure their NGFW with just the click of a button.

This Basic Config with Set Commands tutorial will show the user how to:

* Access and configure the Next Generation Firewall(NGFW) through the web UI and CLI
* Capture configuration differences made on the NGFW into set commands and automation skillets
* Learn how to use Panhandler tooling

However, In order to be able to run valid set commands to begin with, there are a number of prerequisites that must be satisfied.


Prerequisites
--------------

* Have an up and running NGFW VM
* A GitHub_ account with access permissions to edit repository content
* Docker_ desktop active and running on your machine
* Personal preference of Text editor/IDE(Integrated Development Environment) for XML/YAML editing
* Access to the following repositories
* Ability to access the NGFW device via GUI, SSH/CLI and API
* Be able to log into PanHandler_ and import/run skillets, specifically SkilletBuilder_ tools

.. _PanHandler: https://panhandler.readthedocs.io/en/master/
.. _GitHub: https://github.com
.. _Docker: https://www.docker.com
.. _SkilletBuilder: https://github.com/PaloAltoNetworks/SkilletBuilder

This tutorial will be split into # sections below.

1- Setting up the Sandbox
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Please ensure all pre-requisites have been met for this section.


2- Build the skillet
~~~~~~~~~~~~~~~~~~~~

  Edit the .meta-cnc.yaml file to create the skillet

  * create the github repo and clone to edit
  * create an empty .meta-cnc.yaml file
  * save 'before and after' configuration snapshots
  * use the :ref:`Generate a Skillet` tool to create the initial skillet
  * add the variables
  * commit and push to Github

3- Test and Troubleshoot
~~~~~~~~~~~~~~~~~~~~~~~~

  Test against a live device and fix/tune as needed.

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
  
  
  




































A link-  :ref:`Setting up the Sandbox`
