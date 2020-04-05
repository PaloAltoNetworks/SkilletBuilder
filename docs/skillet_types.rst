Types of Skillets
=================

The original skillets were focused on configuration using XML snippets.
This is now extended to include a broad array of skillet types for deployment,
validation, operations, and other needs beyond configuration.

|

docker
------

  Using a docker skillet you can use any available libraries in the docker image.
  This allows you to distribute custom tools and scripts, or use existing
  dockerized tools, as a skillet.

  Using a docker skillet, you can create a single docker image that contains
  all your dependencies and distribute that with the Skillet metadata file.

  Examples:

    * Ansible playbooks and associated libraries
    * Terraform implementations
    * shell and python scripts


  **View examples of docker skillets**

    `Prisma Access stage 1 configuration`_

    .. _Prisma Access stage 1 configuration: https://github.com/PaloAltoNetworks/prisma-access-skillets/tree/master/configuration/panorama_stage_1_config

    `Sample docker skillets`_

    .. _Sample docker skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/docker

    `Docker Skillets at the Skillet District`_

    .. _Docker Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/docker


|

panorama
--------

  Used for API-based XML configuration and operational interactions with Panorama.

  Examples:

    * push XML configuration snippets that merge into the candidate configuration
    * operational commands to generate certificates or perform 'load config partial'
    * configuration commands for move, edit, and delete

.. NOTE::
    The panos and panorama types are functionally identical and used primarily to denote
    the platform target for the skillet

.. NOTE::
    The panorama and panorama-gpcs [Prisma Access] skillet types are identical except for tool
    handling of the commit models. The panorama type will only commit to Panorama while the
    panorama-gpcs type will also push the configuration to Prisma Access.


  **View examples of panorama skillets**



  `IronSkillet v9.1 Panorama`_

  .. _IronSkillet v9.1 Panorama: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/templates/panos/snippets

  `Panorama Skillets at the Skillet District`_

  .. _Panorama Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/panorama

|

panorama-gpcs
-------------

  Used for API-based XML configuration and operational interactions with Panorama specific
  to Prisma Access plug-in configurations.

  Examples:

    * standard Panorama configuration for templates, template-stacks, and device-groups
    * plug-in configuration for service connections, remote networks, and mobile users

  **View examples of Prisma Access skillets**

  `Prisma Access Mobile User`_

  .. _Prisma Access Mobile User: https://github.com/PaloAltoNetworks/prisma-access-skillets/blob/master/stage_2_configuration/load_config_partial_02/.meta-cnc.yaml

|

panos
-----

  Used for API-based XML configuration and operational interactions with a PAN-OS NGFW.

  Examples:

    * push XML configuration snippets that merge into the candidate configuration
    * operational commands to generate certificates or perform 'load config partial'
    * configuration commands for move, edit, and delete


  **View examples of panos skillets**


  `Sample panos skillets`_

  .. _Sample panos skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/panos

  `IronSkillet v9.1 PAN-OS`_

  .. _IronSkillet v9.1 PAN-OS: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/templates/panos/snippets

  `NGFW Skillets at the Skillet District`_

.. _NGFW Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/ngfw

|

pan_validation
--------------

  Used to capture and parse XML configuration file and operational command outputs and
  match against a set of boolean test rules.

  Examples:

    * best practice configuration assessments (eg. IronSkillet)
    * dependency checks before loading configuration skillets (referenced profiles, plugin versions, licensing)
    * check for potential merge conflicts (existing profile names or object ID values)
    * troubleshooting assistance with config/system insights


  **View examples of template skillets**

  `Iron Skillet v9.1 validations`_

  .. _Iron Skillet v9.1 validations: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/validations

  `Sample validation skillets`_

  .. _Sample validation skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/validation

  `Validation Skillets at the Skillet District`_

  .. _Validation Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/validation

|

python
------

  Run python scripts within a controlled virtual environment and include a web UI
  instead of command line arguments. Designed to simplify sharing of python scripts.

  Examples:

    * perform content updates
    * use the NGFW and Support APIs to generate an SLR
    * generate and import configuration files to a device

.. NOTE::
    Python scripts are useful when checking system state is required.
    The best example is checking job status for a process before performing
    the next task. Some skillets are stateless and do not have this capability.

  **View examples of python skillets**

  `HomeSkillet content updates`_

  .. _HomeSkillet content updates: https://github.com/PaloAltoNetworks/HomeSkillet/tree/master/python_content_updates

  `Sample python skillets`_

  .. _Sample python skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/python

  `Python Skillets at the Skillet District`_

  .. _Python Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/python

|

rest
----

  General purpose REST interactions with any REST-supported API. View full results or
  capture to use as input variables in other skillets.

  Examples:

    * Prisma Access service information
    * query a device and return a list of attributes to be used in a skillet dropdown or checklist
    * check status of cloud platforms

  **View examples of rest skillets**

  `Sample REST skillets`_

  .. _Sample REST skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/rest

  `HomeSkillet get zone names`_

  .. _HomeSkillet get zone names: https://github.com/PaloAltoNetworks/HomeSkillet/tree/panos_v9.0/rest_get_zone_names

  `Prisma Access get service information`_

  .. _Prisma Access get service information: https://github.com/PaloAltoNetworks/prisma-access-skillets/tree/master/assess/get_service_info

  `REST Skillets at the Skillet District`_

  .. _REST Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/rest


|

template
--------

  This general purpose skillet type takes a text file input and renders output to screen
  after variable substitutions.

  Examples:

    * full XML config file generation for manual imports
    * set command outputs
    * 3rd party text file generation as reference configurations
    * skillet workflow messaging outputs

  **View examples of template skillets**

  `Iron Skillet v9.1 set commands`_

  .. _Iron Skillet v9.1 set commands: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/templates/panos/set_commands

  `Iron Skillet v9.1 XML config file`_

  .. _Iron Skillet v9.1 XML config file: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/templates/panos/full

  `Sample template skillets`_

  .. _Sample template skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/template/template_example

  `Template Skillets at the Skillet District`_

  .. _Template Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/template


|

terraform
---------

  Used in conjunction with terraform templates to deploy devices.

  Examples:

    * deploy generic compute resources a public cloud
    * deploy a VM-series or Panorama in the public cloud


  **View examples of terraform skillets**

  `Deploy Panorama in Azure`_

  .. _Deploy Panorama in Azure: https://github.com/PaloAltoNetworks/prisma-access-skillets/tree/master/deploy/azure/deploy_panorama

  `Sample Terraform skillets`_

  .. _Sample Terraform skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/terraform

  `Terraform Skillets at the Skillet District`_

  .. _Terraform Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/terraform


|

workflow
--------

  Run a series of skillets across various configurations or skillet types.

  Examples:

    * query a device for attribute names then use in a configuration skillet
    * load a series of day one, network, and policy skillets based on user inputs
    * perform content updates before loading configuration elements
    * validation dependencies before loading configuration elements


  **View examples of workflow skillets**

  `HomeSkillet workflow`_

  .. _HomeSkillet workflow: https://github.com/PaloAltoNetworks/HomeSkillet/tree/panos_v9.0/workflow_HomeSkillet_menu_selection

  `Sample workflow skillets`_

  .. _Sample workflow skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/workflow

  `Workflow Skillets at the Skillet District`_

  .. _Workflow Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/workflow

