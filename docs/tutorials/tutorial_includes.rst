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
        3. Install or Update PanHandler using Docker,  `instructions here`_
        4. Deploy a Next Generation Firewall and Panorama for testing with proper access to GUI and CLI (via SSH)

    .. _instructions here: https://panhandler.readthedocs.io/en/master/running.html#quick-start



Set Up the Submodule
--------------------

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

    When ``ironskillet-components`` is imported into PanHandler (as of the writing of this tutorial), the following
    collections are available. Each of the sub-skillets within these collections loaded can be run individually.

      .. image:: /images/includes_tutorial/ironskillet_components_collections.png
         :width: 800

    Another best practice to mention is that each sub-skillet should include all information needed to configure all snippets
    by itself. This means that any variables used or xml included in the snippet **must** be included directly in the
    sub-skillet. This allows each sub-skillet to be run and debugged individually, and ensures that the playlist that
    includes the sub-skillet will be able to find all the information needed to run the snippet. Also, it is not possible
    to include a skillet include, which is why any xml must be directly specified within the snippets of a sub-skillet.

    The final recommendation for sub-skillets pertains to the individual snippets within the sub-skillet. Each of the
    snippets in a sub-skillet should include a piece of xml small enough to encompass one action. For example,
    each of the IronSkillet antivirus security profiles are broken down into their own snippets. For the five profiles (alert-only,
    inbound, outbound, internal, and exception), there exists a snippet that can then be included or not included in a playlist.
    This subsetting of information is important to provide granularity in choosing what can be included or excluded from
    a playlist down the road.
    See the `panos_ngfw_profile_antivirus_10_0.skillet.yaml <https://github.com/PaloAltoNetworks/ironskillet-components/blob/main/panos_v10.0/ngfw/panos_ngfw_profile_antivirus_10_0.skillet.yaml>`_
    for more in depth information.

    .. NOTE::
        All snippets and sub-skillets within a submodule repository **must** have unique names. This is required for
        referencing later in playlist includes.



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

    Each playlist should have a preamble, just like any skillet or sub-skillet. Since there a lot of sub-skillets,
    snippets, and playlists to keep track of with this model and with this tutorial, it is recommended to keep a
    consistent naming scheme. With the sub-skillet names following ``file_name.skillet.yaml``, it is highly recommended
    to use the ``file_name`` portion as the internal skillet or playlist name.

    For example, the playlist file ``ironskillet_panos_full_10_0.skillet.yaml`` would have an internal name of
    ``ironskillet_full_10_0``. Similarly, one of the sub-skillets named ``panos_ngfw_device_system_10_0.skillet.yaml``
    would have an internal skillet name of ``panos_ngfw_device_system_10_0``. This makes it easy to know how to reference
    the sub_skillets in the playlist using skillet includes.

    Specifying the ``label``, ``description``, ``type``, and ``collection`` are also highly recommended, as they allow
    for easier viewing of the playlists once loaded into PanHandler, and is generally good practice for documentation. In
    particular, the ``type`` is very important, as that tells the skillet player of your choice what type of snippets
    will be included in a configuration.

    The playlist preambles should look like the following:

    **PAN-OS Full PLaylist**

    .. code-block:: yaml

        name: ironskillet_panos_full_10_0
        label: IronSkillet PAN-OS 10.0
        description: |-
          group of snippets for ironskillet 10.0
        type: panos
        labels:
          collection:
            - IronSkillet Playlists

        variables:

        snippets:


    **PAN-OS Alert Only Playlist**

    .. code-block:: yaml

        name: ironskillet_panos_alert_only_10_0
        label: IronSkillet Alert-Only 10.0
        description: |-
          group of alert only policies for ironskillet 10.0
        type: panos
        labels:
          collection:
            - IronSkillet Playlists

        variables:

        snippets:

    **Panorama Not-Shared Security Policies Playlist**

    .. code-block:: yaml

        name: ironskillet_panorama_notshared_security_policies_10_0
        label: IronSkillet Panorama Not-Shared Security Policies 10.0
        description: |-
          group of security policies for panorama not-shared ironskillet 10.0
        type: panorama
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

    There are different ways to include snippets from sub-skillets in a playlist. The main ways are listed below, and
    will be highlighted when building out the playlists in the following section:
      * Load entire sub-skillet as is
      * Load only certain snippets from a sub-skillet
      * Load and change the element of snippets in a sub-skillet
      * Load and change xpath of snippets in a sub-skillet (particularly useful with different panorama setups)

**Load entire sub-skillet as is**

    To include an entire sub-skillet into a playlist, in the **snippet** section of the *playlist*, create entries that
    have a **name** and **include** set to the internal sub-skillet name defined in the preamble of the sub-skillet. In
    this example, all of the snippets from the Device System sub-skillet will be included in the playlist. Any variables
    in the sub-skillet are included by default.

    .. code-block:: yaml

        snippets:
            - name: panos_ngfw_device_system_10_0
            include: panos_ngfw_device_system_10_0

**Load only certain snippets from a sub-skillet**

    If only certain snippets within a sub-skillet should be included in a playlist, still specify the **name** and **include**
    of the entry in the **snippet** section of the *playlist* like the above example. Then, add an **include_snippets**
    attribute and list out each name of the snippets from the sub-skillet to be included. In this example, only the Alert Only
    Antivirus security profile is included from the Antivirus sub-skillet.


    .. code-block:: yaml

        snippets:
            - name: panos_ngfw_profile_antivirus_10_1
            include: panos_ngfw_profile_antivirus_10_1
            include_snippets:
              - name: ironskillet_antivirus_alert_all

    .. NOTE::
        Any variables in the sub-skillet must be specifically included when choosing a subset of snippets to include.
        This is covered in the :ref:`Including Variables<Including Variables>` section of this tutorial.


**Change the element of a snippet in a sub-skillet**

    Sometimes, there may be one snippet in a sub-skillet that has XML changes needed in a playlist. This can easily be
    done through overwriting the element attribute of the snippet from the sub-skillet. In this example the login banner
    snippet was changed from the default in the Device System sub-skillet, but the other five snippets were kept as is.
    Notice that there is an ``include_variables: all`` attribute before the ``include_snippets:``. This is because there
    are variables used in the other snippets that need to be carried over into the playlist. When making overrides to
    snippets using ``include_snippets:``, this is a required step.

    .. code-block:: yaml

        snippets:
            - name: panos_ngfw_device_system_10_0
            include: panos_ngfw_device_system_10_0
            include_variables: all
            include_snippets:
              - name: ironskillet_device_system_dynamic_updates
              - name: ironskillet_device_system_snmp
              - name: ironskillet_device_system_ntp
              - name: ironskillet_device_system_timezone
              - name: ironskillet_device_system_hostname
              - name: ironskillet_device_system_login_banner
                element: |-
                    <login-banner>You have accessed a protected system.
                    If not authorized, log off immediately.</login-banner>


**Change xpath of a snippet in a sub-skillet**

    Similar to the above example, sometime the xpath of a snippet will need to be changed due to device configuration. The
    xpath specifies where in the XML the element should be placed, which can change due to how the device is set up.
    Panorama in particular often has a different xpath depending if it is a shared or not-shared setup. See
    `IronSkillet Documentation <https://iron-skillet.readthedocs.io/en/docs_master/panorama_template_guide.html>`_ for
    more information about this. In `ironskillet-components <https://github.com/PaloAltoNetworks/ironskillet-components>`_,
    the shared xpath was chosen as the default for the xpath attribute in the panorama sub-skillets. In this example,
    a Not-Shared playlist is being built, so the xpath will have to be changed to the not-shared version for some
    sub-skillets. Each snippet in the sub-skillet must be individually included and have the xpath 'overwritten', even
    though the xpath for all snippets in the file might be changing to the same path.

    .. code-block:: yaml

        snippets:
            - name: panorama_device_mgt_config_10_0
            include: panorama_device_mgt_config_10_0
            include_variables: all
            include_snippets:
              - name: ironskillet_device_mgt_users
                xpath: /config/devices/entry[@name='localhost.localdomain']/template-stack/entry[@name='{{ STACK }}']/config/mgt-config
              - name: ironskillet_device_mgt_password_complexity
                xpath: /config/devices/entry[@name='localhost.localdomain']/template-stack/entry[@name='{{ STACK }}']/config/mgt-config

    .. NOTE::
        Notice that there is a new ``STACK`` variable introduced in the changed xpaths. This variable will need to be
        included in the playlist ``variables:`` section.



Including Variables
~~~~~~~~~~~~~~~~~~~

    Generally when including snippets from a sub-skillet, all of the variables from the sub-skillet should be loaded as
    well, since they are needed to execute the snippets. This is the default action when loading an entire sub-skillet,
    but if only certain snippets are loaded, or if changes to the snippet are made in the playlist, it is important to
    specify how variables are included. Basically, anytime the ``include_snippets:`` attribute is used, ``include_variables:``
    should also be specified, as long as there are variables in the sub-skillet to include.

    Take the xpath override example from the previous section:

    .. code-block:: yaml

        snippets:
            - name: panorama_device_mgt_config_10_0
            include: panorama_device_mgt_config_10_0
            include_variables: all
            include_snippets:
              - name: ironskillet_device_mgt_users
                xpath: /config/devices/entry[@name='localhost.localdomain']/template-stack/entry[@name='{{ STACK }}']/config/mgt-config
              - name: ironskillet_device_mgt_password_complexity
                xpath: /config/devices/entry[@name='localhost.localdomain']/template-stack/entry[@name='{{ STACK }}']/config/mgt-config

    This also highlights another important factor, which is that any **new** variables introduced to the playlist in
    snippet changes must be included in the ``variables:`` section of the playlist. Here, the STACK variable should be
    added to the Not-Shared DGTemplate playlists as follows:

    .. code-block:: yaml

        variables:
          - name: STACK
            description: Template stack name for Panorama
            default: sample_stack
            type_hint: text
            help_text: creates a sample template stack with IronSkillet configuration elements


    Other use cases that might come up are:
      * menu options for custom loads (checkboxes in a workflow)
      * when conditional includes



Test and Troubleshoot
---------------------

    Now that the skillet has been pushed to GitHub, the skillet can be imported or loaded into one of the skillet
    player tools, such as PanHandler or SLI, for testing. This Tutorial will show how to test and debug using PanHandler.
    Make sure to `update to the latest release <https://panhandler.readthedocs.io/en/master/running.html#quick-start>`_,
    as playlists are a new feature.

    Testing playlists involves three main components:

        1. User-facing variables
        2. Overall sequence of sub-skillets
        3. Overrides of any sub-skillet features

    Continue reading to see how to test these components in PanHandler.


Import the Playlists
~~~~~~~~~~~~~~~~~~~~

    Import the playlists into PanHandler (see menu for location to do this below), and open the
    **IronSkillet Playlists** collection from either the *Skillet Collections* or *Skillet Repositories* page.

        .. image:: /images/includes_tutorial/import_playlist_panhandler.png
         :width: 800

    .. NOTE::
        If there are other repositories (for example PANW IronSkillet) already loaded into PanHandler that have
        the same skillet names as the playlists, the new playlists will not load. To fix this, remove both repositories
        with duplicate names and try importing the playlist repository again.


Debug and Play the Playlist
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
