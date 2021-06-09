Playlist Includes
=================

Overview
--------

    This tutorial is geared toward skillet developers that want to be able to reuse pieces of a skillet multiple times.
    This can be done by creating a playlist with skillet includes. Skillet includes allow snippets from other skillets
    to be referenced and included in the playlist. This solution is recommended for the following use cases:

      * Creating several skillets that are similar, but have minor content differences
      * Recreating skillets that already exist, but with minor tweaks
      * Keeping a skillet up to date with latest content releases
      * Pulling together content from multiple skillets

    This Playlist Includes tutorial highlights the first three use cases. The focus of this tutorial will show how the
    playlist model for IronSkillet works. This uses a submodule called `ironskillet-components`_ that is used to build
    several playlists that contain different content groups of the IronSkillet configuration. By using a submodule, it
    is easy to update the sub-skillets in one place, and have the playlists pull the latest snippets available. To make
    references more clear, the skillets that the playlist include snippets come from will be called sub-skillets
    throughout this tutorial.

    .. _ironskillet-components: https://github.com/PaloAltoNetworks/ironskillet-components


    .. NOTE::
        Video walkthrough coming soon!

|

    Click below to jump to a specific section of the tutorial:
      1. `Prerequisites and Set Up`_
      2. `Set Up the Submodule`_
      3. `Build the Playlist`_
      4. `Test and Troubleshoot`_
      5. `Document`_
      6. `Other Applications`_

|

Prerequisites and Set Up
------------------------

    Before moving forward with the tutorial, you will need the following:

        1. Create a GitHub repository, :ref:`instructions here<Create a New GitHub Repository>`
        2. Open your repository in a text editor or IDE
        3. Install PanHandler using Docker,  `instructions here`_
        4. Install SLI using a Python virtual environment, :ref:`instructions here<Install SLI>`
        5. Deploy a Next Generation Firewall for testing with proper access to GUI and CLI (via SSH)

    .. _instructions here: https://panhandler.readthedocs.io/en/master/running.html#quick-start



Set Up the Submodule
-----------------

    In this tutorial we are using `ironskillet-components`_, which contains all of the sub-skillets for IronSkillet 10.0+.
    Each folder for the version has all of the panos and panorama sub-skillets, which are broken down by the xpath that
    the snippets use to push the configuration. A breakdown of which sub-skillets correspond to which configuration
    elements can be found in the `IronSkillet documentation`_. This tutorial uses the 10.0 panos sub-skillets to build
    several configuration playlists.

    .. _ironskillet-components: https://github.com/PaloAltoNetworks/ironskillet-components
    .. _IronSkillet documentation: https://iron-skillet.readthedocs.io/en/docs_master/panos_template_guide.html

Add the Submodule
~~~~~~~~~~~~~~~~~

    To add this submodule to the new repository that will contain the playlists, use the following steps:
      * Open the new repository in your IDE or text editor of choice
      * Create a new folder in the root directory called **Submodules**
      * Navigate into that folder
      * Run ``git submodule init https://github.com/PaloAltoNetworks/ironskillet-components.git``

    This will add a copy of the files at that specific commit to your working directory. A ``.gitmodules`` file will
    automatically appear, containing the information about the submodule just added. The sub-skillets from the submodule
    are now able to be included in a playlist. See the :ref:`git submodule overview<Use Submodules>` for more
    information on submodules and how they work.

Sub-Skillets in Submodule
~~~~~~~~~~~~~~~~~~~~~~~~~

    - Basically mini-skillets
    - Same header structure
    - Collections
    - Can be run individually
    - File names are like ``file_name.skillet.yaml``
    - Includes all variables needed to use the snippets


Build the Playlist
------------------

    A playlist is nearly identical to any other skillet, with the main difference being the variable and snippet includes.
    This means that the format and headers will be the same as a normal skillet. The following section will walk through
    how to build out a playlist, and show examples of how to include snippets from a sub-skillet in various ways.

Set Up the Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

      * Open the new repository in your IDE or text editor of choice
      * Create a new folder in the root directory called **Playlists**
      * Navigate into that folder
      * Create three new files with the following names
          * ``ironskillet_full_10_0.skillet.yaml``
          * ``ironskillet_alert_only_10_0.skillet.yaml``
          * ``ironskillet_panorama_notshared_security_policies_10_0.skillet.yaml``

    Playlist file names should follow the pattern ``playlist_name.skillet.yaml``. This allows the skillet players
    (PanHandler, SLI) to recognize that it is a playlist and load the snippets accordingly.


Playlist Preamble
~~~~~~~~~~~~~~~~~~~~~~~~~~

    Link to Configuration Tutorial
    Each playlist should have a Preamble, just like any skillet or sub-skillet

    Since there a lot of sub-skillets, snippets, and playlists to keep track of with this model and with this tutorial,
    it is recommended to choose a consistent naming scheme. With the file names following ``file_name.skillet.yaml``,
    it is suggested to use the ``file_name`` portion as the internal skillet or playlist name. For example, the playlist
    file ``ironskillet_full_10_0.skillet.yaml`` would have an interal name of ``ironskillet_full_10_0``. Similarly one of
    the sub-skillets named ``panos_ngfw_device_system_10_0.skillet.yaml`` would have an internal skillet name of
    ``panos_ngfw_device_system_10_0``. This makes it easy to know how to reference the snippets from the sub-skillet

    All headers should look like the following:

    .. code-block:: yaml

        name: ironskillet_full_10_0
        label: IronSkillet 10.0
        description: |-
          group of snippets for ironskillet 10.0
        type: panos
        labels:
          collection:
            - IronSkillet Playlists

        variables:

        snippets:

    See :ref:`Metadata Attributes page<Metadata Attributes>` for more information on Preamble Attributes and further
    options to specify. The ``variables:`` and `` snippets:`` sections are blank for now, but will be added to in the
    following sections.


Including Snippets
~~~~~~~~~~~~~~~~~~

    There are different ways to include snippets from sub-skillets. The main ways are listed below.
      * Load entire sub-skillet as is
      * Load only certain snippets from a sub-skillet
      * Load and change the element of snippets in a sub-skillet
      * Load and change xpath of snippets in a sub-skillet (particularly with different panos/panorama setups)

    .. code-block:: yaml

        - name: panos_ngfw_device_system_10_0
        include: panos_ngfw_device_system_10_0

        - name: panos_ngfw_profile_antivirus_10_1
        include: panos_ngfw_profile_antivirus_10_1
        include_snippets:
          - name: ironskillet_antivirus_alert_all

        - name: panos_ngfw_device_system_10_0
        include: panos_ngfw_device_system_10_0
        include_variables: all
        include_snippets:
          - name: ironskillet_device_system_dynamic_updates
            element: |-
                <>

        - name: panorama_device_mgt_config_10_0
        include: panorama_device_mgt_config_10_0
        include_variables: all
        include_snippets:
          - name: ironskillet_device_mgt_users
            xpath: /config/devices/entry[@name='localhost.localdomain']/template-stack/entry[@name='{{ STACK }}']/config/mgt-config
          - name: ironskillet_device_mgt_password_complexity
            xpath: /config/devices/entry[@name='localhost.localdomain']/template-stack/entry[@name='{{ STACK }}']/config/mgt-config

Including Variables
~~~~~~~~~~~~~~~~~~~

    Generally when including snippets from a sub-skillet, all of the variables from the sub-skillet should be loaded as
    well, since they are needed to execute the snippets. This is the default action when loading an entire sub-skillet,
    but if only certain snippets are loaded, or if changes to the snippet are made in the playlist, it is important to
    specify how variables are included. The following are some scenarios where this will need to be addressed.
      *

    Need to specify variables in the playlist file for any variables seen
      * menu options for custom loads
      * when conditional includes
      * xpath changes



Test and Troubleshoot
---------------------


Import the Skillet
~~~~~~~~~~~~~~~~~~

Debug and Play the Skillet
~~~~~~~~~~~~~~~~~~~~~~~~~~

Things to look for

- Variables loaded correctly
- xpath and xml snippets loaded correctly
- any overrides go through

Common errors

-
-
-

Edit, Push, Test
~~~~~~~~~~~~~~~~


Document
--------

- The final stage is to document key details about the playlist to provide contextual information to the user community.
- Add documentation to allow others to know


README.md
~~~~~~~~~

- Include information about the submodules included and the content they contain.
- Remind users to update the submodule as needed, since that is not done automatically as new commits are released.

LIVEcommunity
~~~~~~~~~~~~~~

  Playlists can be shared in the Live community as Community or Personal skillets. Community Skillets
  are expected to have a higher quality of testing, documentation, and ongoing support. Personal skillets
  can be shared as-is to create awareness and eventually become upgraded as Community Skillets.


Other Applications
------------------

- Submodules can be any developed skillets, or smaller skillets pre-built
- If don't want to use submodules, can add the sub-skillets directly to the host repository
