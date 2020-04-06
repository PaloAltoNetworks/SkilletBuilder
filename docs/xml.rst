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

Paths and Xpaths
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

Using the same path model for XML and calling it the ``xpath`` (well because it is XML) then you are able to define
where in the configuration data you need to make edits or read information using tags instead of folders.

In the XML example above, the user data is kept at ``/config/mgt-config/users``.  So the xpath is just a chain of tags
separated by '/' stating where a piece of data is located in the file.

**Attributes and Values in the Xpath**

When multiple tags exist in the configuration with the same tag, the attribute and value are used to specific which
folder or tag you want to work with. When required ``[@attribute="value"]`` is included after the tag.

A couple of examples are below.

::

    /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag

This xpath includes two attributes for the localhost name and the vsys name. Using the vsys example, this configuration is
specific to vsys1 while other vsys names could be referenced where needed.

::

    /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag/entry[@name="Outbound"]


Going deeper in the configuration the attribute name and value are used to specific a tag of interest. In this example
a tag named Outbound.


Finding the Xpath
~~~~~~~~~~~~~~~~~

Knowing the xpath is key for most of the configuration and validation skillets. Here are a few ways to find the xpath
for a specific element.

Web UI Debug
^^^^^^^^^^^^

Show example of the debug, make a change, and look for cmd = set or edit

Web UI API Explorer
^^^^^^^^^^^^^^^^^^^

Show example of the explorer

CLI Debug
^^^^^^^^^

Example of debug cli on and show/set commands.


SkilletBuilder Tools
^^^^^^^^^^^^^^^^^^^^

Use of the generator, xml preview and config diffs to find xpaths



Parsing XML
-----------

Config Explorer

xml parsing details to get elements, values, and lists


