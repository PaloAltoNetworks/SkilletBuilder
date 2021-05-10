Basic Configuration With Set Commands
==============================

Overview
--------

This tutorial is designed to help the user get familiar with using set commands to bring up and apply basic configs to their NGFW. By then end of this tutorial the user should be able to alter their firewall manually through the Command Line Interface(CLI) with set commands. All set/op commands that can be entered in the CLI manually can also be transformed into an automation playlist in the form of a skillet. This allows the user to run a series of set commands to easily configure their NGFW with just the click of a button.

This Basic Config with Set Commands tutorial will show the user how to:

* Access and configure the Next Generation Firewall(NGFW) through the web UI and CLI
* Capture configuration differences made on the NGFW into set commands and automation skillets
* Learn how to use Panhandler tooling

However, in order to be able to run valid set commands to begin with, there are a number of prerequisites that must be satisfied.


Prerequisites
--------------

* Have an up and running NGFW Virtual Machine(VM)
* A GitHub_ account with access permissions to edit repository content
* Docker_ desktop active and running on your machine
* Personal preference of text editor/IDE(Integrated Development Environment) for XML/YAML editing[1]
* Ability to access the NGFW device via GUI[2][3], SSH/CLI[4] and API
* For users wishing to work through the command line have SLI_ set up and ready to go

  * SLI can be set up locally on your machine to run quick and efficient commands on your local CLI. Please refer to and follow the steps in the linked SLI page to get started
* For users wishing to work through the browser UI log into PanHandler_ and be able to import/run Skillets, specifically SkilletBuilder_ tools

.. _PanHandler: https://panhandler.readthedocs.io/en/master/
.. _GitHub: https://github.com
.. _Docker: https://www.docker.com
.. _SkilletBuilder: https://github.com/PaloAltoNetworks/SkilletBuilder
.. _SLI: https://pypi.org/project/sli/
.. [1] PyCharm or SublimeText are good options for a beginner text editor or IDE.
.. [2] Log in to the NGFW UI by entering this, *https://XXX.XXX.XXX.XXX* (with your NGFW's management IP replacing the X's), into the web browser URL bar.
.. [3] If you reach a warning page during this step, click advanced settings and choose the proceed to webpage option.
.. [4] Log in to the NGFW via CLI by opening a terminal/bash window on your local machine and entering this, *ssh username@XXX.XXX.XXX.XXX* (with your NGFW's management IP replacing the X's).

This tutorial will be split into # sections below and can either be done via the reading the document or watching the tutorial video. There is a video tutorial for achieving our intended results via use of the PanHandler UI tool and the SLI command line interface tool.

1- `Setting up the Sandbox`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Please ensure all pre-requisites from above have been met for this section.


2- `Build the Skillet`_
~~~~~~~~~~~~~~~~~~~~~~~

  Edit the .meta-cnc.yaml file to create the skillet

  * create the github repo and clone to edit
  * create an empty .meta-cnc.yaml file
  * save 'before and after' configuration snapshots
  * use the :ref:`Generate a Skillet` tool to create the initial skillet
  * add the variables
  * commit and push to Github

3- `Test and Troubleshoot`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Test against a live device and fix/tune as needed.

  * Use the :ref:`Skillet Test Tool` to quick test the skillet
  * Import the skillet into panHandler to test web UI and config loading
  * Fix any UI or loading errors
  * Tune the web UI, configuration elements


4- `Document and Share`_
~~~~~~~~~~~~~~~~~~~~~~~~

  The final and important steps are good documentation and sharing with the community.

  * READme.md documentation in the Github repo
  * Skillet District posting
  * Others can now import into their tools and use the new skillet


Setting up the Sandbox
----------------------
.. _`Setting up the Sandbox`:

In this section we will set everything up that will be needed to successfully complete this tutorial. 

NGFW
~~~~

This is the device that we will be working with and configuring during the tutorial. Be sure that you are able to log into the firewall UI by inputting its management IP into the web browser. When logged in it can be useful to make note of a number of things.

**Software Version:**
Please take note of the devices software version when traversing this tutorial. Some configuration elements may be version specific and require unique skillets per software releases.

**Baseline Configuration:** It is recommended to capture a *baseline* configuration of your newly brought up and pre-configured firewall. This is especially useful for testing purposes if you wish to quickly revert any changes made on the NGFW back to a blank slate. This can be done on the NGFW UI via *Devices->Setup->Operations->Save named configuration snapshot*.

**API Access**
Login credentials with API access to test playing Skillets and any changes made by using set commands.

GitHub
~~~~~~

The user will need a valid GitHub account that they can use to create, edit and clone repositories related to this tutorial. If you do not have an account please go to the GitHub_ website and create one. 

.. _GitHub: https://github.com


Build the Skillet
-----------------
.. _`Build the Skillet`:



.. _`Test and Troubleshoot`:



.. _`Document and Share`: 



