.. _XMLandSkillets:

XML and Skillets
================

A basic understanding of eXtensible Markup Language (XML) structure and terminology is required for
PAN-OS and Panorama skillets.
These devices use XML as the format for the configuration file and operational command responses.

A more extensive knowledge of XML is required for validations skillets in order to capture output and perform tests
against the XML configurations and operational commands.

.. _explore the XML standard: https://www.w3.org/standards/xml/core

You can `explore the XML standard`_ but it isn't required for skillet work. Instead we'll focus on the XML details
of the device configuration files.

|

XML Basics
----------

The basics covers the essentials of XML terminology and structure.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=1b18bf7a-eda9-46bb-8654-ab6a016df3a6&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

|

XML Format
~~~~~~~~~~

The format of XML is related to HTML and uses a common set of terms:

    * **tags**: start and end tags formatted as <tag> and </tag>
    * **attributes and values**: placed inside the tag as attribute="value"
    * **element or 'text' values**: text or numbers as values between associated tags

This example shows how these items are used in HTML. HTML has pre-defined tags for elements such as headers and paragraphs
since HTML is focused on page display. The attributes are used for formatting, href links, and other style
components. The text values are items displayed on screen.

  .. image:: /images/xml_and_skillets/html_sample.png
     :width: 800


You can see that the XML format is similar. There are <tags>, some with attributes="value", and text between tags.
Unlike HTML, XML uses custom tags which is what makes it extensible.

  .. image:: /images/xml_and_skillets/xml_terminology.png
     :width: 800


|

XML Structure
~~~~~~~~~~~~~

At this stage we'll end the comparison to HTML. Although the format is the same, the structure is very different.
Whereas HTML is used to describe presentation, XML is used to describe data.

Folder-based Hierarchy
^^^^^^^^^^^^^^^^^^^^^^

Therefore the best comparison used for XML structure is a folder-based data structure with each <tag> as a folder.
The example shows a representation of the XML file as folders.

  .. image:: /images/xml_and_skillets/xml_structure_folders.png
     :width: 500


The 'config' tag is the top level folder. The second level folders/tags include mgt-config, devices, and shared.
Opening mgt-config shows the next level down, users and password-complexity. This model of nested tags creates the
structure of the configuration data file. The job of skillets is to edit or read this data file structure.

Paths and XPaths
^^^^^^^^^^^^^^^^

Using the same folder model I would reference the users folder path as ``/config/mgt-config/users``.
The path is just a series of folder names separated by '/' showing where I am in the data structure.

XML uses the same concept renaming path to ``XPath``.
The XPath equivalent is ``/config/mgt-config/users`` identical to the folder-based example above.
So the XPath is just a chain of tags separated by '/' stating where a piece of data is located in the file.
In the prior XML example look for the sequence of tags <config>, <mgt-config>, <users> to see the XPath hierarchy
in the raw XML configuration file.


**Attributes and Values in the XPath**

When multiple elements exist in a section of the file with the same tag, the attribute and value are added into each tag
to create a unique XPath branch. This is shown in the XPath with ``[@attribute="value"]`` appended after the tag.

A couple of examples are below.

::

    /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag

This XPath includes two attributes for the localhost name and the vsys name. Using the vsys example, this configuration is
specific to vsys1 while other vsys names could be referenced where needed.

::

    /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag/entry[@name="Inbound"]
    /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag/entry[@name="Outbound"]

In this example each XPath refers to a specific tag object entry based on its name, Inbound or Outbound. The attribute
and values are required since the XML tag ``entry`` is the same for each tag configured.

|

Tools to Find the XPath
-----------------------

Knowing the XPath is key for most of the configuration and validation skillets. Here are a few ways to find the XPath
for a specific configuration element.

The video tutorial shows examples of capturing the XPath and associated XML elements.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=e07d567b-c7cb-41a1-9bc6-ab6a014f0ebc&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

For each documentation example we'll use the same XPath for a NGFW tag object. Each example results in the same XPath.

|

Web UI Debug
~~~~~~~~~~~~

The Web UI Debug is a great starting place if you aren't sure where to begin and are familar with Web UI configuration.

Log into the device and then in another browser tab navigate to ``https://$NGFW_IP/debug`` where $NGFW_IP is the
device IP address.

  .. image:: /images/xml_and_skillets/XML_web_UI_debug.png
     :width: 600


Check ``Debug`` and ``Clear debug`` to get started.

In the configuration UI navigate to Objects > Tags and add a new tag. No need to commit.

Back in the debug tab click ``Refresh`` to view the debug output. You'll see lots of text scroll across the screen.
To find the configuration change, search for ``cmd="edit"`` or ``cmd="set"``. In our case **set** is required since a new
tag. If you make changes to an existing item then use **edit**.

  .. image:: /images/xml_and_skillets/XML_web_UI_debug_search.png
     :width: 800


Just to the right of the set or edit will be ``obj=`` with the XPath. The XPath in this example is:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag/entry[@name='demo_tag']


and ignoring the entry for the tag created the XPath for all tags would be:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag

|

Web UI XML API Explorer
~~~~~~~~~~~~~~~~~~~~~~~

The Web UI XML API Explorer is a web version of the CLI interface designed to view API information.

Log into the device and then in another browser tab navigate to ``https://$NGFW_IP/api`` where $NGFW_IP is the
device IP address.

  .. image:: /images/xml_and_skillets/XML_API_explorer.png
     :width: 250


Click through to the tag configuration:

::


    Configuration Commands > devices > entry[@name='localhost.localdomain'] > vsys > entry[@name='vsys1'] > tag

As you click through you'll notice the entry in the XPath window shows your current XML tree location.

  .. image:: /images/xml_and_skillets/XML_API_explorer_xpath.png
     :width: 800


Clicking ``tag`` at the end gives the XPath as:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag

|

CLI Debug
~~~~~~~~~

If you are familiar with the device CLI commands or are using commands that aren't found in Web UI this is a preferred option.

Simply enter ``debug cli on``, ``configure``, and ``show tag``.

  .. image:: /images/xml_and_skillets/XML_CLI_debug_xpath.png
     :width: 600


The highlighted text just above the tag configuration shows the XPath as:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag


To view the tag XML element, enter ``set cli config-output xml`` in operation mode and enter ``show tag`` in configure mode.
This switches the config view from JSON to XML.

|

Skillet Generator
~~~~~~~~~~~~~~~~~

This option uses the generator to output one or more XPaths based on configuration changes between two files.

To use the Skillet Generator see the :ref:`Generate a Skillet` documentation.

Save a baseline configuration, add a tag, and export the candidate configuration. Use these two files in the generator.

  .. image:: /images/xml_and_skillets/XML_skillet_generator_xpath.png
     :width: 600


The output snippet includes the XPath:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag

|

Parsing XML
-----------

The primary requirement for creating configuration skillets is to know the XPath and associated XML element.
For other types of skillets such as validations and REST, more extensive XML skills are needed to parse XML data.

Parsing XML uses the XPath and various syntax options to generate output including:

    * XML elements
    * a specific value
    * lists of values

This output is used in various ways in tests, pulldown menu options, or input to other skillets.

The :ref:`Configuration Explorer Tool` will be used to view XML parsing outputs.

|

Parsing Syntax Basics
~~~~~~~~~~~~~~~~~~~~~

Parsing the XML file starts with the base XPath which is appended based on the data to be output. The various options
will align to the type of output: element, value, list.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=76a5251d-caac-4c52-aae8-ab6d00f64f9d&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

|

Common items used for parsing configurations and outputs include:

+---------------------------------------+------------------------------------------------------------+
| Use in XPath Query                    |  How Impacts the Query and Output                          |
+=======================================+============================================================+
| append XPath with attribute ``@name`` |  list of names for the last XPath tag (eg. <entry>)        |
+---------------------------------------+------------------------------------------------------------+
| append XPath with text()              |  text value of the last XPath tag                          |
+---------------------------------------+------------------------------------------------------------+
| use tag_name[text()='text_value']     |  filter results where tag_name has a specific text_value   |
+---------------------------------------+------------------------------------------------------------+
| use ``//`` in the XPath               |  wildcard to look across XML branches                      |
+---------------------------------------+------------------------------------------------------------+
| Use ``..`` after a filter statement   |  reference items one level up in the tree for each /../    |
+---------------------------------------+------------------------------------------------------------+

The following sections show examples using the query syntax options above.

Output an XML Element
~~~~~~~~~~~~~~~~~~~~~

The simplest parsing simply returns an XML Element.

Using the XPath from the examples above

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag

the output from the Explorer shows the tag XML elements along with a json snippet.

  .. image:: /images/xml_and_skillets/XML_explorer_element.png
     :width: 600


This entry has 3 tags: block_list, tag name, and demo_tag.

Output a List based on Attribute Name
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This parsing example will return a list of tag names by appending the XPath with ``/entry/@name`` where entry is
the tag of interest and name is the attribute.

The new XPath to query is

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag/entry/@name

and the output is a list of items: the tag names.

  .. image:: /images/xml_and_skillets/XML_explorer_list_of_names.png
     :width: 600


Output a List Filtered on a Text Value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Building on the example, filters can be used to limit the output. In this example we'll filter the output looking for
tags with color = color1.

The new XPath to query is

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag//color[text()='color1']/../@name

and the output is now a list of items, the tag names with color1.

  .. image:: /images/xml_and_skillets/XML_explorer_filter_text.png
     :width: 600


Let's break this down referencing the XML element output in :ref:`Output an XML Element`

  The ``//`` before color is used to skip levels of the XPath, specifically where the tree branches and
  multiple entries exist. This allows us to search all of the <tag> entries.

  Including the  ``color[text()='color1']`` filter captures only the elements with text value = color1.
  At this point we have captured all of the color1 <tag> elements but the goal is to get only the tag object names.

  Using ``/../`` we come back up the tree one level from <color> to the <entry> level of the XPath.
  Each ``/../`` included in the XPath brings us up one level where ``/../../`` would be up two levels.
  We only need to return one level to <entry>.

  Appending ``@name`` gives us the attribute name values found in our captured elements.

The output is the filtered list based on a color value = color1.

.. NOTE::
    Using the Explorer you can try variations of the above XPath syntax without the /../, @name, or filter.
    You can also modify the filter color to return different values.


|

XPath Query Tips
~~~~~~~~~~~~~~~~

    1. Use the Explorer and start with a known XPath and zoom into specific details

    2. Verify what's contained in the configuration file you are querying

    3. If using the double dot ``/../../`` option make sure you properly count the number of levels required






