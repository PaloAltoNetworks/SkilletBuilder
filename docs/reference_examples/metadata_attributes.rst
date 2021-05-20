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
    Globally unique identifier for the skillet referenced by skillet tools and workflows.

    .. note::

        The skillet name must not contain special characters such as '-' or '*' or spaces. Variable names can be any
        length and can consist of uppercase and lowercase letters ( A-Z , a-z ), digits ( 0-9 ), and the underscore
        character ( _ ). An additional restriction is that, although a variable name can contain digits, the first
        character of a variable name cannot be a digit.

label
~~~~~
    A short descriptive name identifying the skillet that is shown in PanHandler selection tiles.

description
~~~~~~~~~~~
    A contextual description of the skillet presented to the user. This may include quick caveats, reminders, and
    skillet intent.

type
~~~~
    One of the predefined :ref:`Skillet Types` allowing tools to determine how to play the skillet.

labels
~~~~~~
    Optional key/value pairs adding complimentary parameters that may not be implemented by all tools.
    See :ref:`Labels Attributes` below for currently supported PanHandler labels.

|
------------------------------------------------------

Labels Attributes
-----------------

Labels are key/value pairs attached to skillets. Labels are optional and allow adding additional parameters to Skillets
that may not be implemented by all utilities. Labels can be used for grouping, searching, sorting, and identifying skillets
beyond just a **name** attribute. Labels can be used to extend Skillet functionality in arbitrary ways going forward. This
behavior is very much influenced by BGPv4 labels and Kubernetes labels.

PanHandler recognizes the following labels:

collection
~~~~~~~~~~

    The **collection** label is used to group like skillets. A skillet may belong to multiple collections. The **collection**
    label value is a list of collection to which the skillet belongs. Skillets with no **collection** label will be placed
    in the *Unknown* Collection.

    .. code-block:: yaml

        labels:
          collection:
            - Example Skillets
            - Test Skillets
            - Validation Skillets


order
~~~~~

    PanHandler uses the **order** label to sort the skillets. Skillets without an **order** label are sorted alphabetically
    by their **label** attribute. Skillets with a lower **order** tag will be display before those with a higher **order** tag.

    .. code-block:: yaml

        labels:
          order: 10


help_link
~~~~~~~~~

    The **help_link** label can be used to display a link to additional documentation about a skillet. This will be shown
    in the *Help* dialog from the *?* icon in the top right hand corner of the skillet input form.

    .. code-block:: yaml

        labels:
          help_link: https://panhandler.readthedocs.io/en/master/variables.html


help_link_title
~~~~~~~~~~~~~~~

  The **help_link_title** will set the displayed title of the **help_link** in the Help dialog.

    .. code-block:: yaml

        labels:
          help_link: https://panhandler.readthedocs.io/en/master/variables.html
          help_link_title: All available Variable Documentation

|
------------------------------------------------------

Variables Attributes
--------------------

The **variables** section is used to define variables and web UI attributes.

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
    A name assigned to the variable.

    .. note::

        The variable name must not contain special characters such as '-' or '*' or spaces. Variable names can be any
        length and can consist of uppercase and lowercase letters ( A-Z , a-z ), digits ( 0-9 ), and the underscore
        character ( _ ). An additional restriction is that, although a variable name can contain digits, the first
        character of a variable name cannot be a digit.

description
~~~~~~~~~~~
    A description of the variable usage and can be displayed as part of a web form.

default
~~~~~~~
    A default value of the variable, which is typically set to a recommended value.

type_hint
~~~~~~~~~
    One of the predefined :ref:`variable types<Variables>` and associates to web form validation. Some variable types,
    such as dropdown, will use additional key/value pairs or source options for user selection.
    See :ref:`Variables` for a complete list of **type_hints** and dynamic UI elements.

source
~~~~~~
    Used in lieu of static key/value pairs in type hints such as dropdown to dynamically create user selections.
    See :ref:`variable_source` for details and examples.

toggle_hint
~~~~~~~~~~~
    Shows a field based on a reference field value. See :ref:`variable_toggle_hint` for details and examples.

|
------------------------------------------------------

Snippets Attributes
-------------------

name
~~~~
    Name of the snippet. Specifically for workflow type skillets, **name** references the Preamble **name** of a skillet
    to play.

cmd
~~~
    Command action to be performed. The default and values vary by skillet type. See :ref:`cmd Options` for additional details.

xpath
~~~~~
    The XPath used for *set*, *edit*, and *delete* **cmd** options for **panos/panorama**.

element
~~~~~~~
    The XML element used for *set*, *edit*, and *delete* **cmd** options for **panos/panorama**.

file
~~~~
    A skillet file to be read. This can either be a template file for **template** skillets, python file for
    **python3** skillets, or an XML file for **panos/panorama** skillets.

path
~~~~
    The URI path for **REST** skillets.

operation
~~~~~~~~~
    The REST operation, either POST or GET, for **REST** skillets.

headers
~~~~~~~
    The headers used as part of a REST API call in **REST** skillets.

output_type
~~~~~~~~~~~
    The data format for response outputs.

outputs
~~~~~~~
    The outputs assigned to a variable. The format is defined using :ref:`Capture Output` options.

input_type
~~~~~~~~~~
    Used in **python3** skillets to specify method for parsing arguments.

image
~~~~~
    Docker image type, such as Alpine.

label
~~~~~
    A descriptive text associated with a test in **validation** skillets.

severity
~~~~~~~~
    Indicates user-defined severity for a test in **validation** skillets.

fail_message
~~~~~~~~~~~~
    The output message when a test fails in **validation** skillets.

pass_message
~~~~~~~~~~~~
    The output message when a test passes in **validation** skillets.

test
~~~~
    A Boolean logic test that is evaluated for **validation** skillets.

documentation_link
~~~~~~~~~~~~~~~~~~
    A documentation reference associated to a test in **validation** skillets.

when
~~~~
    A conditional logic that only performs a test with when is *True*.

transform
~~~~~~~~~
    A dictionary that maps the output from one sub-skillet to the input of another in **workflow**
    skillets. See the `skilletlib Workflow with Transform`_ example skillet for formatting help.

    .. _skilletlib Workflow with Transform:https://github.com/PaloAltoNetworks/skilletlib/blob/master/example_skillets/workflow_transform/workflow_transform.skillet.yaml


|
------------------------------------------------------

cmd Options
-----------

set
~~~
    Merges element into the candidate configuration for **panos/panorama** skillets.

edit
~~~~
    Replaces configuration element with new element for **panos/panorama** skillets.

delete
~~~~~~
    Deletes part of the configuration for **panos/panorama** skillets.

get
~~~
    Pulls information from a device for **panos/panorama** skillets.

move
~~~~
    Moves a configuration element for **panos/panorama** skillets.

parse
~~~~~
    Parses an input file.

cli
~~~
    Run an operations CLI commands such as ``show system info`` for **panos/panorama/validation** skillets.

validate
~~~~~~~~
    Run a validation test for **validation** skillets.

validate_xml
~~~~~~~~~~~~
    TBD; validation

noop
~~~~
    TBD; validation

custom inputs
~~~~~~~~~~~~~
    In this case instead of a **cmd** option, the skillet includes a command line string, such as ``ansible playbook command``.


|
------------------------------------------------------

Snippet Attributes per Skillet Type
-----------------------------------

Below describes the fields for a snippet depending on the skillet type:

    * **docker**

        * **name** - name of this snippet
        * **image** - Docker image to run
        * **cmd** - the command to run inside of the Docker container
        * **when** - (Optional) conditional logic for snippets execution

    * **panos**, **panorama**, **panorama-gpcs**

        * **name** - name of this snippet
        * **cmd** - operation to perform. Default is ``set``. See the :ref:`cmd Options` for all available options.
        * **xpath** - XPath where this fragment belongs
        * **file** - path to the XML fragment to load and parse. Interchangeable with element
        * **element** - inline XML fragment to load and parse. Interchangeable with file
        * **when** - (Optional) conditional logic for snippets execution

        See Example here: :ref:`example_panos`

    * **pan_validation**

        * **name** - name of the validation test to perform
        * **cmd** - validate, validate_xml, noop, or parse. Default is validate
        * **test** - Boolean test to perform using Jinja2 expressions
        * **when** - (Optional) conditional logic for snippets execution

        See Example here: :ref:`example_validation`

    * **python3**

        * **name** - name of the script to execute
        * **file** - relative path to the python script to execute
        * **input_type** - Optional type of input required for this script. Valid options are 'cli' or 'env'.
          This will determine how user input variables will be passed into into the script. The default is **cli** and will
          pass variables as long form arguments to the script in the form of ``--username=user_input`` where ``username``
          is the name of the variable defined in the **variables** section and ``user_input`` is the value entered for
          that variable from the user. The other option, **env**, requires all defined variables to be set in the environment
          of the python process.
        * **when** - (Optional) conditional logic for snippets execution

        See Example here: :ref:`example_python`

    * **rest**

        * **name** - unique name for this rest operation
        * **path** - REST URL path component ``path: http://host/api/?type=keygen&user={{ username }}&password={{ password }}``
        * **operation** - type of REST operation (GET, POST, DELETE, etc)
        * **payload** - path to a Jinja2 template to load and parse to be send as POSTed payload. For ``x-www-form-urlencded``,
          this must be a json dictionary
        * **headers** - a dict of key value pairs to add to the http headers. For example, ``Content-Type: application/json``.
        * **when** - (Optional) conditional logic for snippets execution

        See Example here: :ref:`example_rest` and here: :ref:`example_rest_with_output`

    * **template**

        * **name** - name of this snippet
        * **file** - path to the Jinja2 template to load and parse
        * **template_title** - (Optional) title to include in rendered output
        * **when** - (Optional) conditional logic for snippets execution

    * **terraform**

        * None - snippets are not used for terraform

        See Example here: :ref:`example_terraform`

    * **workflow**

        * **name** - name of this sub-skillet to play
        * **when** - (Optional) conditional logic for sub-skillet execution
        * **transform** - (Optional) mapping of another snippet's output variable to this
          snippet's input variable.


