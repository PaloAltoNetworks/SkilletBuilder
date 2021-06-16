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
    terms more clear in this tutorial, the skillets that the playlist include snippets come from will be called sub-skillets.
    This means we will be constructing a playlists containing snippets from sub-skillets.

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
        4. Deploy a Next Generation Firewall and Panorama for testing with proper access to GUI and CLI (via SSH)

    .. _instructions here: https://panhandler.readthedocs.io/en/master/running.html#quick-start



Set Up the Submodule
-----------------

    In this tutorial we are using `ironskillet-components`_, which contains all of the sub-skillets for IronSkillet 9.1+.
    Each folder for the PAN-OS version has all of the panos and panorama sub-skillets, which are broken down into separate
    files by the xpath that the snippets use to push the configuration. This was do e to keep like snippets together, as
    well as group configurations by categories that could be included or excluded based on the preference of the user.
    A breakdown of which sub-skillets correspond to which configuration elements can be found in the
    `IronSkillet documentation`_. This tutorial uses the 10.0 panos and panorama sub-skillets to build
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

    The working tree of the repository (green square) and ``.gitmodules`` file (red quare) should look like the
    following after following the steps above:

      .. image:: /images/includes_tutorial/submodule_init_IDE.png
         :width: 800

    If you commit and push these changes to your repository, the submodules directory should look like the following:

      .. image:: /images/includes_tutorial/submodule_init_github.png
         :width: 800

Sub-Skillets in Submodule
~~~~~~~~~~~~~~~~~~~~~~~~~

    Looking at `ironskillet-components`_, there are a few best practices for sub-skillets to note. The first is the
    structure of the repository, with all sub-skillets easily grouped by PAN-OS version, and then by type (panos or
    panorama). This allows for easy tracking of all the sub-skillets and simple referencing later on. Second is
    the naming scheme, with all file names following ``file_name.skillet.yaml``. The ``.skillet.yaml`` file ending is
    important to identify that this is a sub-skillet that could be included in another playlist. It is recommended to
    keep the file names short, descriptive, and unique, as the name of the sub-skillet must be specified in a playlist include.

    .. _ironskillet-components: https://github.com/PaloAltoNetworks/ironskillet-components

    Inside each sub-skillet, the meta-data preamble structure is the same as any normal skillet would have. To keep naming conventions simple,
    it is recommended to use the same ``file_name`` specified as the external file name as the internal skillet ``name``
    in the header. Another handy attribute to include is the ``collection`` a sub-skillet should be included
    in. This is because it is possible to load repositories with many sub-skillets into PnaHandler, and it makes it much
    easier to find the sub-skillet you are looking for if they are sorted into descriptive collections.
    See :ref:`Metadata Attributes page<Metadata Attributes>` for more information on
    Preamble Attributes and further options to specify. The
    preamble for `panos_ngfw_device_setting_10_0.skillet.yaml <https://github.com/PaloAltoNetworks/ironskillet-components/blob/main/panos_v10.0/ngfw/panos_ngfw_device_setting_10_0.skillet.yaml>`_
    is included below to illustrate the practices mentioned above.

    .. code-block:: yaml

        name: panos_ngfw_device_setting_10_0
        label: PAN_OS NGFW Device - Setting
        description: |-
            reference device setting configuration snippets
        type: panos
        labels:
            collection:
              - IronSkillet 10.0 PAN-OS Snippets

    The last important best practice to mention is that each sub-skillet should include all information needed to run
    by itself. This means that any variables used or xml included in the snippet **must** be included directly in the
    sub-skillet. This allows each sub-skillet to be run and debugged by itself, and ensures that the playlist that
    includes the sub-skillet will be able to find all the information needed to run the snippet. Also, it is not possible
    to include a skillet include, which is why any xml must be directly specified within the snippets of a sub-skillet.

    When ``ironskillet-components`` is imported into PanHandler (as of the writing of this tutorial), the following
    collections are available. Each of the sub-skillets within these collections loaded can be run individually.

      .. image:: /images/includes_tutorial/ironskillet_components_collections.png
         :width: 800



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
          * ``ironskillet_panos_full_10_0.skillet.yaml``
          * ``ironskillet_panos_alert_only_10_0.skillet.yaml``
          * ``ironskillet_panorama_notshared_security_policies_10_0.skillet.yaml``

    Playlist file names should follow the pattern ``playlist_name.skillet.yaml``. This allows the skillet players
    (PanHandler, SLI) to recognize that it is a playlist and load the snippets accordingly. In this tutorial, playlist
    names will mention IronSkillet, the device type to be configured (panos or panorama), type of playlist, and the
    PAN-OS version. This gives an accurate description of what is included in the playlist without having to open it
    and try to decipher the skillet includes. See below for what the directory should look like after following these steps.

      .. image:: /images/includes_tutorial/playlist_creation.png
         :width: 400


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

    Now that the skillet has been pushed to GitHub, the skillet can be imported or loaded into one of the skillet
    player tools, such as PanHandler or SLI, for testing. This Tutorial will show how to test and debug using PanHandler.
    Testing involves three main components:

        1. User-facing variable menu
        2. Overall sequence of sub-skillets
        3. Overrides of any sub-skillet features

    Continue reading to see how to test these components in PanHandler.


Import the Playlist
~~~~~~~~~~~~~~~~~~



Debug and Play the Playlist
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
    - ``git submodule update --remote --merge``

LIVEcommunity
~~~~~~~~~~~~~~

  Playlists can be shared in the Live community as Community or Personal skillets. Community Skillets
  are expected to have a higher quality of testing, documentation, and ongoing support. Personal skillets
  can be shared as-is to create awareness and eventually become upgraded as Community Skillets.


Other Applications
------------------

- Submodules can be any developed skillets, or smaller skillets pre-built
- If don't want to use submodules, can add the sub-skillets directly to the host repository
