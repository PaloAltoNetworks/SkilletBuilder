Skillet Builder Tools
=====================

.. _Skillet Builder tools repo: https://github.com/PaloAltoNetworks/SkilletBuilder

The `Skillet Builder tools repo`_ contains a suite of tools to help create and test
skillets.

Import to panHandler as part of the Skillet Builder sandbox. The skillets are
part of the ``Skillet Builder`` collection.

|

Generate a Skillet
------------------

Used to generate an XML configuration skillet for PAN-OS or Panorama.
The generator creates an output of xpath and XML element snippets by analyzing
the difference between two XML configuration files.

.. image:: images/Generate_Skillet_tile.png
   :width: 300

Generate a Skillet steps:

    * Choose online or offline mode to obtain the 'before and after' configurations
    * Enter the yaml file preambles values
    * Copy the rendered output to the skillet .meta-cnc.yaml file

When running the generator choose between offline (From uploaded Configs) and online (From Running NGFW) mode.

.. image:: images/Generate_Skillet_running_or_offline.png
   :width: 300

Offline Mode
~~~~~~~~~~~~

  Recommended when generating a skillet from a custom base configuration typically
  for add-on configuration skillets.

  .. image:: images/Generate_Skillet_offline_option.png
     :width: 600

.. NOTE::
    Export the configuration files from the NGFW or Panorama before running the generator.

Online Mode
~~~~~~~~~~~

  Uses an 'out of the box' empty configuration as the baseline. This is useful to
  generate skillets for complete configurations used in demonstrations and POCs.

  .. image:: images/Generate_Skillet_online_mode_menu.png
     :width: 600


  Enter the device API credentials to export the running or candidate configuration
  file.

.. NOTE::
    The skillet attempts to ensure correct snippet ordering. In some cases the snippets must be manually
    reordered based on load order dependencies.

Skeleton YAML file attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After the files are captured the user is prompted for the skillet preamble information.

  .. image:: images/Generate_Skillet_yaml_skeleton.png
     :width: 600


  * Skillet ID: unique name for the skillet
  * Skillet Label: short text label used for skillet selection
  * Skillet description: descriptive text outlining the skillet usage
  * Collection Name: contextual name to group skillets
  * Skillet type: type of skillet (eg. panos, panorama, pan_validation)

Copy the Rendered Output to .meta-cnc.yaml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The output is a complete skillet metadata file. Copy the text and paste into the .meta-cnc.yaml file
for the respective skillet.



The .meta-cnc.yaml file can be further edited adding variables and pasted into the Skillet Test Tool
for local testing without the requirement to push to github.

.. _configuration tutorial skillet: https://github.com/PaloAltoNetworks/SkilletBuilder/blob/master/sample_xml_edl_policy/.meta-cnc.yaml

The `configuration tutorial skillet`_ shows the output of the skillet generator used in the .meta-cnc.yaml file.
This is the difference between an existing configuration file as base and a configuration file
including the tag, external-list, and security policy configuration elements. After the generation, the skillet file
was edited to include the variable components.

|

Preview XML Changes
-------------------

Analyzes the difference between two XML files and outputs the changes in red.

  .. image:: images/Preview_XML_Changes_tile.png
     :width: 300

When running the previewer choose between offline (From uploaded Configs) and online (From Running NGFW) mode.

.. image:: images/Preview_XML_Changes_offline_or_online_mode.png
   :width: 600

Offline Mode
~~~~~~~~~~~~

  Recommended when previewing a skillet from a custom base configuration.

  .. image:: images/Preview_XML_Changes_offline_mode_files.png
     :width: 600

.. NOTE::
    Export the configuration files from the NGFW or Panorama before running the previewer.

Online Mode
~~~~~~~~~~~

  Uses an 'out of the box' empty configuration as the baseline. This is useful to
  preview skillets to see a broad set of changes.

  .. image:: images/Preview_XML_Changes_online_mode_API_values.png
     :width: 600


  Enter the device API credentials to export the running or candidate configuration
  file for preview.

View the Changes
~~~~~~~~~~~~~~~~

After the skillet plays the output to screen includes a list of modified xpaths and the full configuration
file with changes highlighted with red text.


  .. image:: images/Preview_XML_Changes_modifications_xpaths.png
     :width: 600

The xpaths are active links and will jump to its respective section of the configuration file.

  .. image:: images/Preview_XML_Changes_modifications_elements.png
     :width: 400

The red text associates to the tag and external-list xpath configuration elements.

The preview can be useful to see the configuration surrounding outputs from the skillet generator to assist
with any manual skillet tuning.


|

Generate Set CLI Commands
-------------------------

In some cases it is preferred to use set commands instead of XML API configuration. This skillet finds the difference
between two configuration files and outputs the associated set commands.

  .. image:: images/Generate_Set_Commands_tile.png
     :width: 300

When running the generator choose between offline (From uploaded Configs) and online (From Running NGFW) mode.

.. image:: images/Generate_Set_Commands_offline_or_offline_selection.png
   :width: 600

Offline Mode
~~~~~~~~~~~~

  Recommended when generating a skillet from a custom base configuration typically
  for add-on configuration skillets.

  .. image:: images/Generate_Set_Commands_offline_files_to_upload.png
     :width: 600

.. NOTE::
    Export the configuration files from the NGFW or Panorama before running the generator.

Online Mode
~~~~~~~~~~~

  Uses an 'out of the box' empty configuration as the baseline. This is useful to
  generate skillets for complete configurations used in demonstrations and POCs.

  .. image:: images/Generate_Set_Commands_online_mode_API_values.png
     :width: 600


  Enter the device API credentials to export the running or candidate configuration
  file.


|

Skillet Test Tool
-----------------

The test tool is used to play skillets without the need to upload to Github and import into tools like panHandler.
Debug outputs can also be used for enhanced skillet testing.

  .. image:: images/Skillet_Test_Tool_tile.png
     :width: 300

When running the test tool choose between Offline and Online modes. Also select Debug mode if required.

Offline Mode
~~~~~~~~~~~~

    * validation skillets: paste in a configuration text file without requiring API access
    * other skillet types: not applicable and may generate errors

.. image:: images/Skillet_Test_Tool_offline_mode_text_box.png
   :width: 800

.. NOTE::
    Export the configuration files from the NGFW or Panorama before running the test tool.

Online Mode
~~~~~~~~~~~

    * panos/panorama: load skillet snippets using API credentials
    * validation: get the device configuration file and run the validation
    * rest: run the skillet with REST credentials and output the results

  .. image:: images/Skillet_Test_Tool_oneline_mode_API_values.png
     :width: 800


Debug Mode
~~~~~~~~~~

If ``True`` provides extended output after the skillet is complete.

    * output response messages after skillet execution: ``success`` or ``failed`` responses
    * .meta-cnc.yaml text
    * context variable values
    * For validation skillets this shows the capture outputs to assist with skillet testing and tuning.

  .. image:: images/Skillet_Test_Tool_debug_mode_select.png
     :width: 800

Skillet Content
~~~~~~~~~~~~~~~

This is the skillet to be played. Paste in the complete .meta-cnc.yaml file content including the preamble.

  .. image:: images/Skillet_Test_Tool_skillet_content.png
     :width: 800

.. NOTE::
    In panHandler this content is cached and will appear each time the Test Tool skillet is used. This allows for
    instead editing to quickly test skillets. However if extensive edits are required, edits should be done in the
    skillet editor to ensure YAML syntax and alignment is correct.


Test Tool Output
~~~~~~~~~~~~~~~~

Based on the skillet type and debug mode, output will vary.

  .. image:: images/Skillet_Test_Tool_output.png
     :width: 800

More detailed outputs and using the test tool is covered in the details for building skillets.


|

Configuration Explorer Tool
---------------------------

The Configuration Explorer Tool is used to display xml elements and values based on xml parsing syntax.

    * Used to discover Capture outputs in validation skillets
    * assist with manual exploration of xpath and XML element associations

  .. image:: images/Skillet_Test_Tool_tile.png
     :width: 300

When running the explorer tool choose between Offline and Online modes. Also select Debug mode if required.

Offline Mode
~~~~~~~~~~~~

In offline mode the user pastes in the XML configuration file without the use of API interactions.

.. image:: images/Configuration_Explorer_Tool_offline_mode_input.png
   :width: 800

.. NOTE::
    Export the configuration files from the NGFW or Panorama before running the test tool.

Online Mode
~~~~~~~~~~~

Exports the device configuration based on the API values.

  .. image:: images/Configuration_Explorer_Tool_online_mode_API_values.png
     :width: 800


XPATH Query
~~~~~~~~~~~

The xpath query to use against the configuration file.

  .. image:: images/Configuration_Explorer_Tool_xpath_query.png
     :width: 500

Example xpath queries and syntax details are covered in the XML section of the documentation (TODO).

Configuration Explorer Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The output shows the results of the xpath query as an xml element, value, or list of values. This is determined by
the input query syntax.

  .. image:: images/Configuration_Explorer_Tool_output.png
     :width: 500

Output details include:

    * the xpath queried
    * XML results as an XML element, value, or list of values
    * json version of the XML results


|

Sample Configuration Skillet
----------------------------

This skillet provides a reference configuration skillet used in the tutorial content.

  .. image:: images/Sample_Configuration_tile.png
     :width: 300

Configuration includes:

    * tag snippet with tag name, description, and color variables
    * external-list snippet with external-list name, description, and URL variables
    * Inbound and Outbound block security policies referencing tag and external-list variables

  .. image:: images/Sample_Configuration_input_variables.png
     :width: 600

.. _View the details of the configuration skillet: https://github.com/PaloAltoNetworks/SkilletBuilder/blob/master/sample_xml_edl_policy/.meta-cnc.yaml

`View the details of the configuration skillet`_


|

Sample Validation Skillet
-------------------------

This skillet provides a reference validation skillet used in the tutorial content.

  .. image:: images/Sample_Validation_tile.png
     :width: 300

Validation includes:

    * check that NTP servers are configured
    * check that password complexity is enabled with a 12 char minimum password
    * check that all url-filtering profiles block category malware
    * check that all allow security policies include a profile or group

  .. image:: images/Sample_Validation_output.png
     :width: 800

.. _View the details of the validation skillet: https://github.com/PaloAltoNetworks/SkilletBuilder/blob/master/sample_validation_skillet/.meta-cnc.yaml

`View the details of the validation skillet`_

|

Skillet YAML File Template
--------------------------

This skillet uses a simple text render to generate a starter .meta-cnc.yaml formatted output.

  .. image:: images/Skeleton_YAML_tile.png
     :width: 300

Skeleton file inputs include:

  * Skillet ID: unique name for the skillet
  * Skillet Label: short text label used for skillet selection
  * Skillet description: descriptive text outlining the skillet usage
  * Collection Name: contextual name to group skillets
  * Skillet type: type of skillet (eg. panos, panorama, pan_validation)

  .. image:: images/Skeleton_YAML_inputs.png
     :width: 800

.. _View the skeleton YAML template: https://github.com/PaloAltoNetworks/SkilletBuilder/blob/master/skeleton_yaml/meta-cnc-skeleton.conf

`View the skeleton YAML template`_


