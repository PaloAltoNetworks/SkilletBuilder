Skillet Builder Overview
========================

Welcome. This site contains Skillet Builder documentation, examples, and tutorials designed to expand the Builder community.
This is a living set of content updated as new skillet types, examples, and tutorials are available.

The video contains a quick Skillet overview and a few demonstrations playing Skillets with panHandler.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=8b8cb56c-f1dd-4d6e-821e-ab98014d9046&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

|

The purpose of Skillet Builders is to 'skilletize' knowledge and expertise into sharable entities that can be
played by users to eliminate the complexity of various tasks. This can complement or remove the requirement to
capture GUI config guides that can still require hours of configuration steps, often with all users entering the same
sets of data. Thus the transition from 'show me how to configure' to 'give a configuration to load'.

Skillet Use Cases
-----------------

Skillets are built and played to (1) simplify the burden of repeatable tasks and (2) rapidly get to an outcome using
recommended practices from subject matter experts. These goals can be extended over a wide array of use cases:

Deploy
~~~~~~

Instead of manually deploying infrastructure, skillets help with automated or semi-automated tasks. Integrating
with Terraform and Ansible, skillets can provide a web UI interface to capture data and run templates and playbooks.

    * instantiate compute resources in the cloud
    * simplify licensing
    * update device software
    * perform NGFW threat and AV content updates
    * install plug-ins

Configure
~~~~~~~~~

Save time by levering best practice and reference configurations created by subject matter experts.

    * Day One best practice configurations
    * one-click demo and POC setup
    * mobile workforce remote access
    * SecOps recommended reports and custom signatures
    * vertical-specific use cases
    * quick config guides as skillets

Assess
~~~~~~

Gain visibility about system and configuration state.

    * PAN-OS and Panorama configuration validation checks
    * automated Security Lifecycle Review (SLR)
    * query service information such as Prisma Access service info

|

Skillet Players
---------------

Skillets are open-source and extensible, ready to play using any supported application.

Supported players and utilities include:

  +---------------------------------------------------+
  | `panHandler Skillet Player`_                      |
  +---------------------------------------------------+
  | `Expedition (Migration Tool)`_                    |
  +---------------------------------------------------+
  | `Palo Alto Networks Customer Support Portal`_     |
  +---------------------------------------------------+
  | `Secure Dynamics`_                                |
  +---------------------------------------------------+
  | `skilletCLI or interacting with skillets`_        |
  +---------------------------------------------------+

  .. _panHandler Skillet Player: https://panhandler.readthedocs.io
  .. _Expedition (Migration Tool): https://live.paloaltonetworks.com/t5/Expedition-Migration-Tool/ct-p/migration_tool
  .. _Palo Alto Networks Customer Support Portal: https://support.paloaltonetworks.com/
  .. _Secure Dynamics: https://www.securedynamics.net/sechealth-for-firewalls/
  .. _skilletLib for application development: https://skilletlib.readthedocs.io/
  .. _skilletCLI or interacting with skillets: https://github.com/adambaumeister/skilletcli


