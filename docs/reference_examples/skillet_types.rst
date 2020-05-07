Skillet Types
=============

The original skillets were focused on configuration using XML snippets.
This is now extended to include a broad array of skillet types for deployment,
validation, operations, and other needs beyond configuration.

|

docker
------

  With a docker skillet you can use any available libraries in the docker image.
  This allows you to distribute custom tools and scripts, or use existing
  dockerized tools, as a skillet.

  Using a docker skillet, you can create a single docker image that contains
  all your dependencies and distribute that with the Skillet metadata file.

  Use cases:

    * Ansible playbooks and associated libraries
    * Terraform implementations
    * shell and python scripts


  **View examples of docker skillets**

  +---------------------------------------------------+
  | `Prisma Access stage 1 configuration`_            |
  +---------------------------------------------------+
  | `Sample docker skillets`_                         |
  +---------------------------------------------------+
  | `Docker Skillets at the Skillet District`_        |
  +---------------------------------------------------+

    .. _Prisma Access stage 1 configuration: https://github.com/PaloAltoNetworks/prisma-access-skillets/tree/master/configuration/stage_1_configuration
    .. _Sample docker skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/docker
    .. _Docker Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/docker

|


panorama
--------

  Used for API-based XML configuration and operational interactions with Panorama.

  Examples:

    * push XML configuration snippets that merge into the candidate configuration
    * operational commands to generate certificates or perform 'load config partial'
    * configuration commands for move, edit, and delete

  **View examples of panorama skillets**

  +---------------------------------------------------+
  | `IronSkillet v9.1 Panorama`_                      |
  +---------------------------------------------------+
  | `Panorama Skillets at the Skillet District`_      |
  +---------------------------------------------------+

  .. _IronSkillet v9.1 Panorama: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/templates/panos/snippets
  .. _Panorama Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/panorama


  .. NOTE::
      The panos and panorama types are functionally identical and used primarily to denote
      the platform target for the skillet

  .. NOTE::
      The panorama and panorama-gpcs [Prisma Access] skillet types are identical except for tool
      handling of the commit models. The panorama type will only commit to Panorama while the
      panorama-gpcs type will also push the configuration to Prisma Access.

|

panorama-gpcs
-------------

  Used for API-based XML configuration and operational interactions with Panorama specific
  to Prisma Access plug-in configurations.

  Examples:

    * standard Panorama configuration for templates, template-stacks, and device-groups
    * plug-in configuration for service connections, remote networks, and mobile users

  **View examples of Prisma Access skillets**

  +---------------------------------------------------+
  | `Prisma Access Remote Network`_                   |
  +---------------------------------------------------+

  .. _Prisma Access Remote Network: https://github.com/PaloAltoNetworks/prisma-access-skillets/tree/master/configuration/stage_2_configuration/remote_network_onboarding

|

panos
-----

  Used for API-based XML configuration and operational interactions with a PAN-OS NGFW.

  Examples:

    * push XML configuration snippets that merge into the candidate configuration
    * operational commands to generate certificates or perform 'load config partial'
    * configuration commands for move, edit, and delete


  **View examples of panos skillets**

  +---------------------------------------------------+
  | `Sample panos skillets`_                          |
  +---------------------------------------------------+
  | `IronSkillet v9.1 PAN-OS`_                        |
  +---------------------------------------------------+
  | `NGFW Skillets at the Skillet District`_          |
  +---------------------------------------------------+

  .. _Sample panos skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/panos
  .. _IronSkillet v9.1 PAN-OS: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/templates/panos/snippets
  .. _NGFW Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/ngfw

|

pan_validation
--------------

  Used to capture and parse XML configuration file and operational command outputs and
  match against a set of boolean test rules.

  Examples:

    * best practice configuration assessments (eg. IronSkillet)
    * dependency checks before loading configuration skillets
    * check for potential merge conflicts based on existing config elements
    * troubleshooting assistance with config/system insights

  **View examples of template skillets**

  +---------------------------------------------------+
  | `Iron Skillet v9.1 validations`_                  |
  +---------------------------------------------------+
  | `Sample validation skillets`_                     |
  +---------------------------------------------------+
  | `Validation Skillets at the Skillet District`_    |
  +---------------------------------------------------+

  .. _Iron Skillet v9.1 validations: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/validations
  .. _Sample validation skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/validation
  .. _Validation Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/validation

|

python3
-------

  Run python scripts within a controlled virtual environment and include a web UI
  instead of command line arguments. Designed to simplify sharing of python scripts.

  Current version used in panHandler is python3.6

  Examples:

    * perform content updates
    * use the NGFW and Support APIs to generate an SLR
    * generate and import configuration files to a device


  **View examples of python skillets**

  +---------------------------------------------------+
  | `HomeSkillet content updates`_                    |
  +---------------------------------------------------+
  | `Sample python skillets`_                         |
  +---------------------------------------------------+
  | `Python Skillets at the Skillet District`_        |
  +---------------------------------------------------+

  .. _HomeSkillet content updates: https://github.com/PaloAltoNetworks/HomeSkillet/tree/master/python_content_updates
  .. _Sample python skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/python
  .. _Python Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/python


  .. NOTE::
      Python scripts are useful when checking system state is required.
      The best example is checking job status for a process before performing
      the next task. Some skillets are stateless and do not have this capability.

|

rest
----

  General purpose REST interactions with any REST-supported API. View full results or
  capture to use as input variables in other skillets.

  Examples:

    * Prisma Access or other platform service information
    * query a device and return a list of values used in a skillet UI dropdown
    * check status of cloud platforms

  **View examples of rest skillets**

  +---------------------------------------------------+
  | `Sample REST skillets`_                           |
  +---------------------------------------------------+
  | `HomeSkillet get zone names`_                     |
  +---------------------------------------------------+
  | `Prisma Access get service information`_          |
  +---------------------------------------------------+
  |  `REST Skillets at the Skillet District`_         |
  +---------------------------------------------------+

  .. _Sample REST skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/rest
  .. _HomeSkillet get zone names: https://github.com/PaloAltoNetworks/HomeSkillet/tree/panos_v9.0/rest_get_zone_names
  .. _Prisma Access get service information: https://github.com/PaloAltoNetworks/prisma-access-skillets/tree/master/assess/get_service_info
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

  +---------------------------------------------------+
  | `Iron Skillet v9.1 set commands`_                 |
  +---------------------------------------------------+
  | `Iron Skillet v9.1 XML config file`_              |
  +---------------------------------------------------+
  | `Sample template skillets`_                       |
  +---------------------------------------------------+
  | `Template Skillets at the Skillet District`_      |
  +---------------------------------------------------+

  .. _Iron Skillet v9.1 set commands: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/templates/panos/set_commands
  .. _Iron Skillet v9.1 XML config file: https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v9.0/templates/panos/full
  .. _Sample template skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/template/template_example
  .. _Template Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/template

|

terraform
---------

  Used in conjunction with terraform templates to deploy devices.

  Examples:

    * deploy generic compute resources a public cloud
    * deploy a VM-series or Panorama in the public cloud


  **View examples of terraform skillets**

  +---------------------------------------------------+
  | `Deploy Panorama in Azure`_                       |
  +---------------------------------------------------+
  | `Sample Terraform skillets`_                      |
  +---------------------------------------------------+
  | `Terraform Skillets at the Skillet District`_     |
  +---------------------------------------------------+

  .. _Deploy Panorama in Azure: https://github.com/PaloAltoNetworks/prisma-access-skillets/tree/master/deploy/azure/deploy_panorama
  .. _Sample Terraform skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/terraform
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

  +---------------------------------------------------+
  | `HomeSkillet workflow`_                           |
  +---------------------------------------------------+
  | `Sample workflow skillets`_                       |
  +---------------------------------------------------+
  | `Workflow Skillets at the Skillet District`_      |
  +---------------------------------------------------+

  .. _HomeSkillet workflow: https://github.com/PaloAltoNetworks/HomeSkillet/tree/panos_v9.0/workflow_HomeSkillet_menu_selection
  .. _Sample workflow skillets: https://github.com/PaloAltoNetworks/Skillets/tree/master/workflow
  .. _Workflow Skillets at the Skillet District: https://live.paloaltonetworks.com/t5/Community-Skillets/tkb-p/Community_Skillets_Articles/label-name/workflow

