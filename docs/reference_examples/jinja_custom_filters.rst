Custom Jinja Filters
====================

Custom filters are used to simplify validation skillets by using a small set of filter options
to check the most common configuration components contained in tags, attributes, and element text values.

Review the :ref:`XML Basics` documentation for the XML terminology used in the custom filters.

Additional examples can be found in the `skilletlib examples directory`_

.. _skilletlib examples directory: https://github.com/nembery/skilletlib/tree/master/example_skillets


Capturing XML Objects
---------------------

In order to properly validate a config it is often necessary to convert the XML structure to an object, which
can then be used in a Jinja expression to perform basic logic and validation. The captured object is associated to
an XPath plus its corresponding XML element and assigned a variable name used in the custom filter.

Each custom filter example below shows its respective captured object for use in the filter.

When building skillets, the Builder needs to:

    * know the XPath for each object to capture
    * determine what part of the XML element will be referenced: attribute, tag, element text value
    * which custom filter to select based on the XML element reference
    * what conditions have to be met: a specific or range of values, item present or absent, etc.


Checking Attributes
-------------------

Attribute filters are most commonly used to check object names although other attributes can exist within the XML configuration.

.. code-block:: bash

    attribute_present(tag name, attribute name, attribute value)
    attribute_absent(tag name, attribute name, attribute value)

The attribute being checked in this example is the external-list entry name.
Therefore the input values for the attribute filters are:

    * tag name: <entry>
    * attribute name: 'name'
    * the attribute value of interest


A sample XML element found at XPath ``/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/external-list``
is used as reference for the attribute custom filters examples. The element will be a captured object variable called
``external-list``.

.. code-block:: xml

    <external-list>
      <entry name="tutorial_edl">
        <type>
          <ip>
            <recurring>
              <five-minute/>
            </recurring>
            <description/>
            <url>http://tutorial.com</url>
          </ip>
        </type>
      </entry>
      <entry name="my_edl">
        <type>
          <ip>
            <recurring>
              <five-minute/>
            </recurring>
            <description/>
            <url>http://my_url.com</url>
          </ip>
        </type>
      </entry>
    </external-list>


attribute_present
~~~~~~~~~~~~~~~~~

  Checks if an attribute value exists and returns True if the attribute value is found. This filter is
  used to ensure a named object or policy exists in the configuration. This item should be present as part
  of a best practice validation or other config skillets may have dependencies on this item.

  .. code-block:: bash

      external-list | attribute_present('entry', 'name', 'my_edl')
      external-list | attribute_absent('entry', 'name', 'new_edl')


  The first filter will return True since my_edl is in the external-list object. The second filter will return False since
  new_edl is not in the external-list object.


attribute_absent
~~~~~~~~~~~~~~~~

  Checks if an attribute value exists and returns True if the attribute value is not found. This filter is
  used to ensure a named object or policy does not already exist in the configuration. If the item exists
  it may cause config merge conflicts or override an existing configuration.

  .. code-block:: bash

      external-list | attribute_absent('entry', 'name', 'my_edl')
      external-list | attribute_absent('entry', 'name', 'new_edl')

  The first filter will return False since my_edl is in the external-list object.
  The second filter will return True since new_edl is not in the external-list object.


Checking an Element Value
-------------------------

Element value filters are most commonly used to check specific text values in the XML configuration.

.. code-block:: bash

    element_value('tag name') [expression] value

Any valid jinja expression can be used to evaluate the text value.

A sample XML element found at XPath ``/config/devices/entry[@name='localhost.localdomain']/deviceconfig/system``
will be used as reference for the element value custom filter example. The element will be a captured object variable called
``device_system``.

.. code-block:: xml

    <update-schedule>
      <anti-virus>
        <recurring>
          <hourly>
            <at>4</at>
            <action>download-and-install</action>
          </hourly>
        </recurring>
      </anti-virus>
      <wildfire>
        <recurring>
          <every-min>
            <action>download-and-install</action>
          </every-min>
        </recurring>
      </wildfire>
    </update-schedule>
    <snmp-setting>
      <access-setting>
        <version>
          <v3/>
        </version>
      </access-setting>
    </snmp-setting>
    <ntp-servers>
      <primary-ntp-server>
        <ntp-server-address>0.pool.ntp.org</ntp-server-address>
      </primary-ntp-server>
      <secondary-ntp-server>
        <ntp-server-address>1.pool.ntp.org</ntp-server-address>
      </secondary-ntp-server>
    </ntp-servers>
    <login-banner>You have accessed a protected system.
        Log off immediately if you are not an authorized user.
    </login-banner>
    <timezone>EST</timezone>

element_value
~~~~~~~~~~~~~

  Checks an element_value expression and returns True if the expression is true. This filter is
  used to check a specific value or range based on best practices or expected configuration settings.
  Various checks such as '==', '!=', '>=', and '<=' can be used in the filter.

  .. code-block:: bash

      device_system | element_value('update-schedule.wildfire.recurring.every-min.action') == 'download-and-install'
      device_system | element_value('timezone') == 'UTC'


  The first filter uses the ``dot notation`` to step down the tree to the wildfire dynamic update action.
  This allows a single captured object to be used for multiple tests instead of an explicit capture object
  for each test using a granular XPath. The filter will return True since the action for Wildfire updates is
  set to 'download-and-install'.

  The second filter will return False since the XML configuration for timezone is 'EST' and not 'UTC'.


Checking Tags
-------------

The tag filters are most commonly used to check specific tags that are used in the data structure as configuration values.

.. code-block:: bash

    tag_present('tag name')
    tag_absent('tag name')

The example below references the same ``device_system`` captured object used in the element_value example.

tag_present
~~~~~~~~~~~

  Checks for a tag name and returns True if the tag is found. This filter is
  used to check for a specific tag in cases where configuration values are tags instead of text values.
  In the device_system example the recurring interval for Wildfire updates is a tag shown as ``<every-min>``

  .. code-block:: bash

      device_system | tag_present('update-schedule.wildfire.recurring.every-min')
      device_system | tag_present('update-schedule.wildfire.recurring.every-hour')

  The filters use the ``dot notation`` to step down the tree to the wildfire recurring interval.
  This allows a single captured object to be used for multiple tests instead of an explicit capture object
  for each test using a granular XPath.

  The first filter will return True since the Wildfire update interval is
  set to 'every-min'. The second filter will return False since every-hour is not found.


  Other examples using tag_present from the same device_system capture object:

  .. code-block:: bash

    device_system | tag_present('snmp-setting.access-setting.version.v3') --> check if SNMP v3 configured
    device_system | tag_present('ntp-servers.primary-ntp-server') --> check if an NTP server is configured


tag_absent
~~~~~~~~~~

  Checks for a tag name and returns False if the tag is found. This filter is
  used to check for tag-based configuration components that should NOT exist in the configuration.
  In the device_system example the recurring interval for Wildfire updates is a tag shown as ``<every-min>``

  .. code-block:: bash

      device_system | tag_absent('update-schedule.wildfire.recurring.every-min')
      device_system | tag_absent('update-schedule.wildfire.recurring.every-hour')

  The filters use the ``dot notation`` to step down the tree to the wildfire recurring interval.
  This allows a single captured object to be used for multiple tests instead of an explicit capture object
  for each test using a granular XPath.

  The first filter will return False since the Wildfire update interval is
  set to 'every-min'. The second filter will return True since every-hour is not found.


Checking a Set of Element Values
--------------------------------

In some cases multiple values are contained with a portion of the configuration. These are often referenced in the
configuration file with <member> tags. Examples of multiple entries include:

    * zones, addresses, users, or tags assigned to a security policy
    * URL categories assigned to block or alert actions
    * interfaces assigned to a zone or virtual-router

To check multiple element values, the element_value_contents custom filter can search across all members to find a
specific value.

element_value_contains
~~~~~~~~~~~~~~~~~~~~~~

The inputs to the filter are the tag name and the search value.

.. code-block:: bash

    element_value_contains('tag name', 'search value')

This example checks a security rule to see if a specific destination address using an external-list is found. The XPath
for the Outbound Block Rule is
/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/rulebase/security/rules/entry[@name='Outbound Block Rule']

Below is an abbreviated XML element showing the <destination> content of interest.

.. code-block:: xml

    <entry name="Outbound Block Rule">
      <to>
        <member>any</member>
      </to>
      <from>
        <member>any</member>
      </from>
      <destination>
        <member>panw-highrisk-ip-list</member>
        <member>panw-known-ip-list</member>
        <member>panw-bulletproof-ip-list</member>
      </destination>
      <action>deny</action>
      <log-setting>default</log-setting>
      <tag>
        <member>Outbound</member>
      </tag>
    </entry>

The custom filter looks for the inclusion of the panw-bulletproof-ip-list EDL as a destination address.

  .. code-block:: bash

      security_rule_outbound_edl | element_value_contains('destination.member', 'panw-bulletproof-ip-list')

Since the member value is found a True result is returned.

Referencing the same example, other element_value_contains checks could be used for <to> or <from> zones and
<tag> members.













