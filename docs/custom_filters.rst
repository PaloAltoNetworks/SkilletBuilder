Custom Jinja Filters
====================

Custom filters are used to simplify XML output testing in validation skillets.

Review the :ref:`XML Basics` documentation for terminology used in the custom filters.

Examples can be found in the `skilletlib examples directory`_

.. _skilletlib examples directory: https://github.com/nembery/skilletlib/tree/master/example_skillets

This XML element found at XPath ``/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/external-list``
will be used as reference for the custom filters examples. The element will be a captured object variable called
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


attribute_absent
----------------

  Checks if an attribute value exists and returns True if the attribute value is not found. This filter is
  used to ensure a named object or policy does not already exist in the configuration. If the item exists
  it may cause config merge conflicts or override an existing configuration.

  .. code-block:: bash

      external-list | attribute_absent('entry', 'name', 'my_edl')
      external-list | attribute_absent('entry', 'name', 'new_edl')

  The first filter will return False since my_edl is in the external-list object. The second filter will return True since
  new_edl is not in the external-list object.

attribute_present
-----------------

  Checks if an attribute value exists and returns True if the attribute value is found. This filter is
  used to ensure a named object or policy exists in the configuration. This item should be present as part
  of a best practice validation or other config skillets may have dependencies on this item.

  .. code-block:: bash

      external-list | attribute_present('entry', 'name', 'my_edl')
      external-list | attribute_absent('entry', 'name', 'new_edl')


  The first filter will return True since my_edl is in the external-list object. The second filter will return False since
  new_edl is not in the external-list object.

element_value
-------------

  Checks an element_value expression and returns True if the expression is true. This filter is
  used to check a specific value or range based on based practices or expected configuration settings.
  Various checks such as '==', '!=', '>=', and '<=' can be used in the filter.

  .. code-block:: bash

      external-list-tutorial_edl | element_value('type.ip.url') == 'http://tutorial.com'
      external-list-tutorial_edl | element_value('type.ip.url') == 'http://unknown.com'


  The first filter will return True since tutorial.com is found in the variable object. The second filter will return
  False since unknown.com is not found.

.. NOTE::

    The sample XPath has been appended with ``/entry[@name='tutorial_edl']``
    to check the text value for a specific entry.

.. NOTE::

    You can use the dot notation with tag names to step down the tree. In this example, the element_value looks down
    into <type>, <ip>, <url> to find the url text for the tutorial_edl entry.


tag_absent
----------

  Checks for a tag name and returns False if the tag is found. This filter is
  used to check for a specific tag in cases where configuration values are tags instead of text values.
  In this example the recurring interval for external-list updates is a tag shown as ``<five-minute>``

  .. code-block:: bash

      external-list-tutorial_edl | tag_absent('type.ip.recurring.five-minute')
      external-list-tutorial_edl | tag_absent('type.ip.recurring.hourly')


  The first filter will return False since five-minute is found in the variable object. The second filter will return
  True since hourly is not found.

.. NOTE::

    The sample XPath has been appended with ``/entry[@name='tutorial_edl']``
    to check the text value for a specific entry.

.. NOTE::

    You can use the dot notation with tag names to step down the tree. In this example, the element_value looks down
    into <type>, <ip>, <recurring> to find the update interval for the tutorial_edl entry.

tag_present
-----------

  Checks for a tag name and returns True if the tag is found. This filter is
  used to check for a specific tag in cases where configuration values are tags instead of text values.
  In this example the recurring interval for external-list updates is a tag shown as ``<five-minute>``

  .. code-block:: bash

      external-list-tutorial_edl | tag_present('type.ip.recurring.five-minute')
      external-list-tutorial_edl | tag_present('type.ip.recurring.hourly')


  The first filter will return True since five-minute is found in the variable object. The second filter will return
  False since hourly is not found.

.. NOTE::

    The sample XPath has been appended with ``/entry[@name='tutorial_edl']``
    to check the text value for a specific entry.

.. NOTE::

    You can use the dot notation with tag names to step down the tree. In this example, the element_value looks down
    into <type>, <ip>, <recurring> to find the update interval for the tutorial_edl entry.


element_value_contains
----------------------

TODO with example that may not be the current EDL example








