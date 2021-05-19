Metadata Attributes
===================

Complete listing of all metadata attributes used in skillets.

|

Preamble Attributes
-------------------

The preamble is the top section of the skillet providing identifying items, help text, and collection information.

.. code-block:: yaml

    name: sample_validation_skilletbuilder
    label: Sample Validation Skillet

    description: |
      Short set of validations for skilletBuilder training tutorial with ntp check, password complexity,
      URL filtering for malware, and security allow rules with profiles or groups

    type: pan_validation
    labels:
      collection:
        - Skillet Builder
        - Validation
      order: 10
      help_link: https://skilletbuilder.readthedocs.io/en/latest/reference_examples/builder_tools.html#sample-validation-skillet
      help_link_title: SkilletBuilder sample validation skillet


name
~~~~
    unique identifier for the skillet referenced by skillet tools and workflows

label
~~~~~
    short descriptive name identifying the skillet; shown in panHandler selection tiles

description
~~~~~~~~~~~
    contextual description of the skillet presented to the user. May include quick caveats, reminders, and
    skillet intent.

type
~~~~
    one of the predefined :ref:`Skillet Types` allowing tools to determine how to play the skillet

labels
~~~~~~
    optional key/value pairs adding additional parameters that may not be implemented by all tools
    see :ref:`Labels Attributes` for currently supported panHandler labels

|

Labels Attributes
-----------------

Labels are key/value pairs attached to skillets. Labels are optional and allow adding additional parameters to Skillets
that may not be implemented by all Tools. Labels can be used for grouping, searching, sorting, and identifying skillets
beyond just a 'name' attribute. Labels can be used to extend Skillet functionality in arbitrary ways going forward. This
behaviour is very much influenced by BGPv4 labels and Kubernetes labels.

Panhandler recognizes the following labels:

collection
~~~~~~~~~~

  The `collection` label is used to group like Skillets. A skillet may belong to multiple collections. The collection
  label value is a list of collection to which the skillet belongs. Skillets with no `collection` label will be placed
  in the *Unknown* Collection.

.. code-block:: yaml

    labels:
      collection:
        - Example Skillets
        - Test Skillets
        - Validation Skillets


order
~~~~~

  Panhandler uses the 'order' label to sort the Skillets. Skillets without an 'order' label are sorted alphabetically
  by their 'label' attribute. Skillets with a lower 'order' tag will be display before those with a higher 'order' tag.

.. code-block:: yaml

    labels:
      order: 10


help_link
~~~~~~~~~

  The `help_link` label can be used to display a link to additional documentation about a skillet. This will be shown
  in the 'Help' dialog from the '?' icon in the top right hand corner of the Skillet input form.

.. code-block:: yaml

    labels:
      help_link: https://panhandler.readthedocs.io/en/master/variables.html


help_link_title
~~~~~~~~~~~~~~~

  The `help_link_title` will set the displayed title of the `help_link` in the Help dialog.

.. code-block:: yaml

    labels:
      help_link: https://panhandler.readthedocs.io/en/master/variables.html
      help_link_title: All available Variable Documentation

|

Variables Attributes
--------------------

The variables section is used to define variables and web UI attributes.

.. code-block:: yaml

    variables:
      - name: INTF_UNTRUST
        description: internet Interface
        default: ethernet1/1
        type_hint: dropdown
        source: interface_names
      - name: INTF_TRUST
        description: internal Interface
        default: ethernet1/2
        type_hint: dropdown
        source: interface_names
      - name: IP_12
        description: internal interface ip address
        default: 192.168.45.20/24
        type_hint: text
      - name: tag_color
        description: tag color
        default: red
        type_hint: dropdown
        dd_list:
          - key: green
            value: color2
          - key: orange
            value: color6
          - key: red
            value: color1

name
~~~~
    name assigned to the variable

    .. note::

        The variable name must not contain special characters such as '-' or '*' or spaces. Variable names can be any
        length and can consist of uppercase and lowercase letters ( A-Z , a-z ), digits ( 0-9 ), and the underscore
        character ( _ ). An additional restriction is that, although a variable name can contain digits, the first
        character of a variable name cannot be a digit.

description
~~~~~~~~~~~
    description of the variable usage and can be displayed as part of a web form

default
~~~~~~~
    default value of the variable; typically set to a recommended value

type_hint
~~~~~~~~~
    type of variable and associates to web form validation; some variable types such as dropdown will
    use additional key/value pairs or source options for user selection;
    See :ref:`Variables` for a complete list of type_hints and dynamic UI elements

source
~~~~~~
    used in lieu of static key/value pairs in type hints such as dropdown to dynamically create user selections;
    See :ref:`variable_source` for details and examples

toggle_hint
~~~~~~~~~~~
    show a field based on a reference field value; See :ref:`variable_toggle_hint` for details and examples

|

Snippets Attributes
-------------------

name
~~~~
    name of the snippet; for workflow reference the name of a skillet to play

cmd
~~~
    command action to be performed; default and values vary by skillet type; :ref:`cmd Options` for details

xpath
~~~~~
    XPath used for set, edit, and delete cmd options (TODO: validate this content);
    panos/panorama

element
~~~~~~~
    XML element used for configuration; cmd = set or edit;
    panos/panorama

file
~~~~
    skillet file to be read; template file, python file

path
~~~~
    URI path; REST

operation
~~~~~~~~~
    POST or GET operation; REST

headers
~~~~~~~
    headers used as part of a REST API call; REST

output_type
~~~~~~~~~~~
    data format for response outputs

outputs
~~~~~~~
    outputs assigned to a variable; format is defined using :ref:`Capture Output` options

input_type
~~~~~~~~~~
    used in python skillets to specify method for parsing arguments

image
~~~~~
    docker image type such as alpine

label
~~~~~
    description text associated to a test; validation

severity
~~~~~~~~
    indicates user-defined severity for a test; validation

fail_message
~~~~~~~~~~~~
    output message when a test fails; validation

pass_message
~~~~~~~~~~~~
    output message when a test passes; validation

test
~~~~
    boolean test to perform; validation

documentation_link
~~~~~~~~~~~~~~~~~~
    documentation reference associated to a test; validation

when
~~~~
    conditional logic that only performs a test with when is True

|


cmd Options
-----------

set
~~~
    merge element into the candidate configuration; panos/panorama

edit
~~~~
    replace configuration element with new element; panos/panorama

delete
~~~~~~
    delete part of the configuration; panos/panorama

get
~~~
    pull information from a device; panos/panorama

move
~~~~
    move a configuration element; panos/panorama

parse
~~~~~
    parse an input file; all???

cli
~~~
    run an operations CLI commands such as 'show system info'; panos/panorama/validation

validate
~~~~~~~~
    run a validation test; validation

validate_xml
~~~~~~~~~~~~
    TBD; validation

noop
~~~~
    TBD; validation

custom inputs
~~~~~~~~~~~~~
    in this case instead of a cmd option, the skillet includes a command line string; eg ansible playbook command





