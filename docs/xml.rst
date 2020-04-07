XML and Skillets
================

A basic understanding of XML structure and terminology is required for PAN-OS and Panorama skillets. These devices use
the eXtensible Markup Language (XML) as the format for the configuration file and operational command responses.

A more extensive knowledge of XML is required for validations skillets in order to capture output and perform tests
against the XML configurations and operational commands.

.. _explore the XML standard: https://www.w3.org/standards/xml/core

You can `explore the XML standard`_ but it isn't required for skillet work. Instead we'll focus on the XML details
of the device configuration files.

|

XML Basics
----------

The basics covers the essentials of XML terminology and structure.



XML Format
~~~~~~~~~~

The format of XML is related to HTML and uses a common set of terms:

    * tags: start and end tags formatted as <tag> and </tag>
    * attributes and values: placed inside the tag as attribute="value"
    * element or 'text' values: text or numbers as values between associated tags

This example shows how these items are used in HTML. HTML has pre-defined tags for elements such as headers and paragraphs
since HTML is focused on page display. The attributes are used for formatting, href links, and other style
components. The text values are items displayed on screen.

  .. image:: images/html_sample.png
     :width: 800

You can see that the XML format is similar. There are <tags>, some with attributes="value", and text between tags.
Unlike HTML, XML uses custom tags which is what makes it extensible.

  .. image:: images/xml_terminology.png
     :width: 800


|

XML Structure
~~~~~~~~~~~~~

At this stage we'll end the comparison to HTML. Although the format is the same, the structure is very different.
Whereas HTML is used to describe presentation, XML is used to describe data.

Folder-based Hierarchy
^^^^^^^^^^^^^^^^^^^^^^

Therefore the comparison used for XML structure is a folder-based data structure with each <tag> as a folder. The example
shows a representation of the XML file as folders.

  .. image:: images/xml_structure_folders.png
     :width: 500

The 'config' tag is the top level folder. The second level folders/tags include mgt-config, devices, and shared.
Opening mgt-config shows the next level down, users and password-complexity.

This model of nested tags creates the structure of the configuration data file. The job of skillets is to edit or read this
data file structure.

Paths and XPaths
^^^^^^^^^^^^^^^^

Using the same folder model and a Linux prompt view, I can walk through the folder structure.

::

    midleton:config:$
    midleton:config:$ path
    /config
    midleton:config:$
    midleton:config:$ ls
    devices		mgt-config	shared
    midleton:config:$
    midleton:config:$ cd mgt-config/
    midleton:mgt-config:$
    midleton:mgt-config:$ path
    /config/mgt-config
    midleton:mgt-config:$
    midleton:mgt-config:$ cd users
    midleton:users:$
    midleton:users:$ path
    /config/mgt-config/users
    midleton:users:$
    midleton:users:$ ls
    entry_name_admin
    midleton:users:$
    midleton:users:$


I start at /config and move into child folders mgt-config and users. The ``path`` alias is the same as ``pwd`` but
only shows the relative folder starting at config. The final path is ``/config/mgt-config/users``.

The path is just a series of folder names separated by '/'.

Using the same path model for XML and calling it the ``XPath`` (well because it is XML) then you are able to define
where in the configuration data you need to make edits or read information using tags instead of folders.

In the XML example above, the user data is kept at ``/config/mgt-config/users``.  So the XPath is just a chain of tags
separated by '/' stating where a piece of data is located in the file.

**Attributes and Values in the XPath**

When multiple tags exist in the configuration with the same tag, the attribute and value are used to specific which
folder or tag you want to work with. When required ``[@attribute="value"]`` is included after the tag.

A couple of examples are below.

::

    /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag

This XPath includes two attributes for the localhost name and the vsys name. Using the vsys example, this configuration is
specific to vsys1 while other vsys names could be referenced where needed.

::

    /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag/entry[@name="Outbound"]


Going deeper in the configuration the attribute name and value are used to specific a tag of interest. In this example
a tag named Outbound.

|

Finding the XPath
~~~~~~~~~~~~~~~~~

Knowing the XPath is key for most of the configuration and validation skillets. Here are a few ways to find the XPath
for a specific configuration element.

For each example we'll look for the XPath to configure a tag yet the same method works for any configuration edits.

|

Web UI Debug
^^^^^^^^^^^^

The Web UI Debug is a great starting place if you aren't sure where to begin and are familar with Web UI configuration.

Log into the device and then in another browser tab navigate to ``https://$NGFW_IP/debug`` where $NGFW_IP is the
device IP address.

  .. image:: images/XML_web_UI_debug.png
     :width: 600

Check ``Debug`` and ``Clear debug`` to get started.

In the configuration UI navigate to Objects > Tags and add a new tag. No need to commit.

Back in the debug tab click ``Refresh`` to view the debug output. You'll see lots of text scroll across the screen.
To find the configuration change, search for ``cmd="edit"`` or ``cmd="set"``. In our case **set** is required since a new
tag. If you make changes to an existing item then use **edit**.

  .. image:: images/XML_web_UI_debug_search.png
     :width: 800

Just to the right of the set or edit will be ``obj=`` with the XPath. The XPath in this example is:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag/entry[@name='demo_tag']


and ignoring the entry for the tag created the XPath for all tags would be:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag

|

Web UI XML API Explorer
^^^^^^^^^^^^^^^^^^^^^^^

The Web UI XML API Explorer is a web version of the CLI interface designed to view API information.

Log into the device and then in another browser tab navigate to ``https://$NGFW_IP/api`` where $NGFW_IP is the
device IP address.

  .. image:: images/XML_API_explorer.png
     :width: 250

Click through to the tag configuration:

    Configuration Commands > devices > entry[@name='localhost.localdomain'] > vsys > entry[@name='vsys1'] > tag

As you click through you'll notice an entry in the XPath window.

  .. image:: images/XML_API_explorer_XPath.png
     :width: 800

Clicking tag at the end gives the XPath as:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag

|

CLI Debug
^^^^^^^^^

If you are familiar with the device CLI commands or have commands that aren't found in Web UI this is a preferred option.

Simply enter ``debug cli on``, ``configure``, and ``show tag``.

  .. image:: images/XML_CLI_debug_XPath.png
     :width: 600

The highlighted text just above the tag configuration gives the XPath as:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag


To view the tag XML element, enter ``set cli config-output xml`` in operation mode and enter ``show tag`` in configure mode.
This switches the config view from json to XML.

|

Skillet Generator
^^^^^^^^^^^^^^^^^

This option uses the generator to output one or more XPaths based on configuration changes between two files.

To use the Skillet Generator see the :ref:`Generate a Skillet` documentation.

Save a baseline configuration, add a tag, and export the candidate configuration. Use as the two files in the generator.

  .. image:: images/XML_skillet_generator_XPath.png
     :width: 600

The output snippet includes the XPath:

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag

|

Parsing XML
-----------

The primary requirements for creating configuration skillets is to know the XPath and associated XML element.
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

Common items used for parsing configurations and outputs include:

    * List of attribute values: append the xpath with ``@name`` where name is the attribute name
    * return element text: append ``text()`` to the end of the xpath
    * skip XPath tag levels, especially for broader queries: use ``//`` in the XPath instead of explicit tags
    * Filter queries: use ``tag_name[text()='text_value']`` where the tag_name has a specific text_value
    * search element details then reference attributes further up the tree, use ``..`` for each level up the tree

Below are example queries and outputs.

Output an XML Element
~~~~~~~~~~~~~~~~~~~~~

The simplest parsing simply returns an XML Element.

Using the XPath from the examples above

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag

the output from the explorer shows the tag XML elements along with a json snippet.

  .. image:: images/XML_explorer_element.png
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

  .. image:: images/XML_explorer_list_of_names.png
     :width: 600


Output a List Filtered on a Text Value
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Building on the example, filters can be used to limit the output. In this example we'll filter the output looking for
tags with color = color1.

The new XPath to query is

::

    /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag//color[text()='color1']/../@name

and the output is now a list of items, the tag names with color1.

  .. image:: images/XML_explorer_filter_text.png
     :width: 600

Let's break this down.

    * The ``//`` after tag is used to skip levels of the xpath, especially when we have multiple tag attribute names and values

    * The ``color[text()='color1']`` goes down to the color tag level and gets all elements with text value = color1

    * The ``/../@name`` uses the double dot notation to go up one level in the tree and grab the list of name values

This gives us the filtered list based on a color value.


