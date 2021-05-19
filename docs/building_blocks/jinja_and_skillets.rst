.. _jinjaandskillets:

Jinja and Skillets
==================

Jinja is a templating language for Python and used within the skillet framework to:

    * allow variable value substitution
    * provide lightweight coding logic such as if and for
    * apply filters to format data
    * leverage filters for validation testing logic

  .. image:: /images/jinja_and_skillets/jinja_engine.png
     :width: 800

Content objects are collected from the skillet and passed through the rendering engine.


The video tutorial covers Jinja variables, if conditionals, and for loops.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=cc895e38-e07d-47d0-aad0-ab6b0110ea51&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

|

Jinja Variable
--------------

Variables are used in the Snippets sections of the .meta-cnc.yaml file and externally referenced text files to:

    * provide simple substitutions for values in an XML or set command configuration file
    * define variable-based XPaths such as Panorama templates and device-groups
    * create contextual output pass/fail messages in validation skillets

Variables are added using a ``{{ variable }}`` syntax.

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

Jinja For Loop
--------------

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

Jinja Filter
------------

Jinja filters have a few roles in skillets:

    1. reformat data
    2. boolean logic for validation tests
    3. output passwords as hashes

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=99d78d0b-0c16-4fe9-b43b-ab6d014c8971&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>

These filters can be `built-in filters`_ or custom skillet filters.

.. _built-in filters: https://jinja.palletsprojects.com/en/2.11.x/templates/#for

Filters are used by including `` | filter `` after a variable:


+----------------------------------------------+-------------------------------------------------+
| Variable | Filter example                    |  Filter action                                  |
+==============================================+=================================================+
| var | length                                 |  True if a list var has values                  |
+----------------------------------------------+-------------------------------------------------+
| var | length == 0                            |  True if a list var is empty                    |
+----------------------------------------------+-------------------------------------------------+
| var | md5_hash                               |  convert a password to a phash                  |
+----------------------------------------------+-------------------------------------------------+
| var | element_value('config_value') == 'yes' |  True if the XML config_value = yes             |
+----------------------------------------------+-------------------------------------------------+
| var | tag_present('config_tag')              |  True if the XML tag exists                     |
+----------------------------------------------+-------------------------------------------------+
| var | replace ("old", "new")                 |  replace a string or substring with a new value |
+----------------------------------------------+-------------------------------------------------+
| var | int                                    |  convert a string to an integer                 |
+----------------------------------------------+-------------------------------------------------+

Jinja Whitespace Control
------------------------

Care must usually be taken to ensure no extra whitespace creeps into your templates due to Jinja looping
constructs or control characters. For example, consider the following fragment:

.. code-block:: jinja

    <dns-servers>
    {% for member in CLIENT_DNS_SUFFIX %}
        <member>{{ member }}</member>
    {% endfor %}
    </dns-servers>

This fragment will result in blank lines being inserted where the `for` and `endfor` control tags are placed. To
ensure this does not happen and to prevent any unintentioal whitespace, you can use Jinja whitespace control like
so:

.. code-block:: jinja

    <dns-servers>
    {%- for member in CLIENT_DNS_SUFFIX %}
        <member>{{ member }}</member>
    {%- endfor %}
    </dns-servers>

.. note:: Note the '-' after the leading '{%'. This instructs jinja to remove these blank lines in the resulting
    parsed output template.
