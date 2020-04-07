Jinja and Skillets
==================

Jinja a templating language for Python and used within the skillet framework to:

    * allow variable substitution
    * provide lightweight coding logic like if and for
    * apply filters to format data
    * leverage filters for validation testing logic

  .. image:: images/jinja_engine.png
     :width: 800

Content objects are collected from the skillet and associated files then passed through the rendering engine.

|

Jinja Variables
---------------

Variables are used in the Snippets sections of the .meta-cnc.yaml file and externally referenced text files to:

    * provide simple substitutions for values in an XML or set command configuration file
    * define variable-based XPaths such as Panorama templates and device-groups
    * create contextual output pass/fail messages in validation skillets

Variables are added to using a ``{{ variable }}`` syntax.

The example below uses three variables: tag_name, tag_color, and tag_description

.. code-block:: yaml

        snippets:
          - name: object_tag
            xpath: /config/devices/entry[@name="localhost.localdomain"]/vsys/entry[@name="vsys1"]/tag
            element: |-
                <entry name="{{ tag_name }}">
                  <color>{{ tag_color }}</color>
                  <comments>{{ tag_description }}</comments>
                </entry>

The skillet player captures the variable values with output as a rendered XML element.

.. code-block:: xml

        entry name="block_rule">
          <color>color1</color>
          <comments>block rules based on EDL destinations</comments>
        </entry>

|

Jinja If Conditional
--------------------

If conditionals can be used in a skillet to decide if part of an element is rendered based on a variable value.

In this example a dropdown is used in the metadata file to input dhcp or static IP addressing.

.. code-block:: yaml

    variables:
      - name: MGMT_TYPE
        description: firewall management IP type
        default: dhcp-client
        type_hint: dropdown
        dd_list:
          - key: dhcp-client
            value: dhcp-client
          - key: static
            value: static
      - name: MGMT_IP
        description: NGFW management IP
        default: 192.0.2.6
        type_hint: ip_address
      - name: MGMT_MASK
        description: NGFW management netmask
        type_hint: ip_address
        default: 255.255.255.0
      - name: MGMT_DG
        description: NGFW management default gateway
        default: 192.0.2.7
        type_hint: ip_address

Below is the XML element with the if conditional embedded. The conditionals are placed within ``{% if content %}``
using `built-in Jinja expressions`_.

    .. _built-in Jinja expressions: https://jinja.palletsprojects.com/en/2.11.x/templates/#expressions


Choosing MGMT_TYPE = static will include the IP address, netmask, and gateway elements while ignoring the DHCP configuration.
If the selection is DHCP the inverse is true with only the DHCP settings rendered.

.. code-block:: xml

    <type>
      {%- if MGMT_TYPE == "static" %}
        <static/>
      {% elif MGMT_TYPE == "dhcp-client" %}
        <dhcp-client>
         <send-hostname>yes</send-hostname>
         <send-client-id>no</send-client-id>
         <accept-dhcp-hostname>no</accept-dhcp-hostname>
         <accept-dhcp-domain>no</accept-dhcp-domain>
        </dhcp-client>
      {% else %}
        <dhcp-client>
         <send-hostname>yes</send-hostname>
         <send-client-id>no</send-client-id>
         <accept-dhcp-hostname>no</accept-dhcp-hostname>
         <accept-dhcp-domain>no</accept-dhcp-domain>
        </dhcp-client>
      {% endif %}
    </type>
    {%- if MGMT_TYPE == "static" %}
    <ip-address>{{ MGMT_IP }}</ip-address>
    <netmask>{{ MGMT_MASK }}</netmask>
    <default-gateway>{{ MGMT_DG }}</default-gateway>
    {% endif %}

Here is the output if static is selected:

.. code-block:: xml

    <type>
        <static/>
    </type>
    <ip-address>192.0.2.6</ip-address>
    <netmask>255.255.255.0</netmask>
    <default-gateway>192.0.2.7</default-gateway>

And the output if dhcp-client is selected:

.. code-block:: xml

    <type>
        <dhcp-client>
         <send-hostname>yes</send-hostname>
         <send-client-id>no</send-client-id>
         <accept-dhcp-hostname>no</accept-dhcp-hostname>
         <accept-dhcp-domain>no</accept-dhcp-domain>
        </dhcp-client>
    </type>

|

Jinja For Loops
---------------

For loops can be used in a skillet to capture a list of information and iterate over the list as multiple entries.

In this example a list of serial numbers are onboarded to Panorama.

.. code-block:: yaml

    variables:
      - name: serial_number
        description: Device serial number
        default: 12345
        type_hint: list
        help_text: basic onboarding to panorama; click + to add additional devices

Below is the XML element with the for loop embedded. The conditionals are placed within ``{% for content %}``
using `Jinja built-in for loop logic`_.

    .. _Jinja built-in for loop logic: https://jinja.palletsprojects.com/en/2.11.x/templates/#for


.. code-block:: xml

    {% for item in serial_number %}
        <entry name="{{ item }}"/>
    {% endfor %}


The rendered output element is:

.. code-block:: xml


    <entry name="1234567890"/>
    <entry name="1234567891"/>
    <entry name="1234567892"/>

adding in each serial number in the variable list.

|

Jinja Filters
-------------



| syntax
built-in filters: https://jinja.palletsprojects.com/en/2.11.x/templates/#list-of-builtin-filters
custom filters for validations