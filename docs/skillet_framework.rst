The Skillet Framework
=====================

The Skillet Framework is designed to create a structured yet extensible model for a multitude of skillet types.


  .. image:: images/skillet_framework.png
     :width: 800


View the video for a quick overview of the Skillet Framework

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=ccdf68c7-106b-4132-9c77-ab6b00f1f57d&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

|

Github
------

Github is a widely known version-control and collaboration platform. Typically used by software developers, it
provides the perfect solution as a skillet archive. The key elements of Github include:

    * easy to push and archive skillet content
    * simple import to ingest and play skillets
    * branching for development and software version requirements
    * forking for community development and customization
    * issue tracking to provide skillet feedback

Other sites and platforms that mimic Github can also be used to archive and share skillets.

Github Repositories
-------------------

Repositories (repos) are used to capture a set of skillets. Any new skillet author will require a Github account and each
project will have its own repo.

Github Branches
---------------

Each repo can have one or more branches. Branches are used to isolate development without affecting other branches.

The primary branch is ``master`` with optional branches using names such as ``develop`` or ``panos_v9.1``.
These optional branches are named according to their purpose for skillet development or software version specific skillets.

Each branch contains:

    * the skillet folders
    * a common README.md file including documentation, authors, and the support policy
    * LICENSE file
    * [optional] .gitignore file to name files and directories not pushed to Github


Skillet Folders
---------------

Each skillet is stored in its own directory containing:

    * the .meta-cnc.yaml file with core skillet content
    * README.md file with skillet specific documentation
    * [optional] associated files based on skillet type


Skillet Metadata File
---------------------

The skillet metafile contains key descriptors, variable definitions, and skillet actions.

  .. image:: images/skillet_framework_yaml_file.png
     :width: 800


Preamble
~~~~~~~~

  The opening section of the skillet yaml file containing contextual data about the skillet.


  Includes:

    * name: unique skillet name
    * label: contextual text used in applications for skillet selection
    * description: short description of the skillet and any prerequisites
    * type: the type of skillet such as panos, panorama, pan_validation
    * collection: one or more tags for skillet grouping
    * optional metadata tags

Variables
~~~~~~~~~

  Variables used in the skillet are entered as part of a web form or inherited from prior played skillets.

  This allows the Skillet Builder to determine what variables are used within the skillet, use form validation to ensure
  proper formatting is used for each variable, and use dynamic elements such as hide/show to provide display controls.

  A broad set of :ref:`Variable Types` are available.

Snippets
~~~~~~~~

  This is the action part of the skillet and unique for each skillet type.

    * panos/panorama: reads a list of XPaths and elements that are pushed to the device for configuration
    * template: simple rendering of a text file displayed to the screen
    * rest: a series of REST API interactions including response capture
    * python: run a python script in a local virtual environment
    * pan_validation: assess a configuration against a set of predefined rules
    * terraform: run terraform deployments for cloud deployments
    * docker: instantiate a docker container to run virtual applications

