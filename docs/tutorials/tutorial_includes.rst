Playlist Includes
=================

|

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
    playlist model for IronSkillet works. This uses a submodule called `ironskillet-components <https://github.com/PaloAltoNetworks/ironskillet-components>`_
    that is used to build
    several playlists that contain different content groups of the IronSkillet configuration. By using a submodule, it
    is easy to update the sub-skillets in one place, and have the playlists pull the latest snippets available. To make
    terms more clear in this tutorial, the skillets that the playlist include snippets come from will be called sub-skillets.
    This means we will be constructing a playlists containing snippets from sub-skillets.


    The final repository built from this tutorial can be viewed `here <https://github.com/madelinemccombe/Playlist_Includes_Tutorial>`_.


    .. raw:: html

        <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=52cb2d2e-8e09-420e-8af6-ad58012843e3&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&captions=false&interactivity=all"
        height="405" width="720" style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>
|

    Click below to jump to a specific section of the tutorial:
      1. `Prerequisites`_
      2. `Set Up the Submodule`_
      3. `Build the Playlist`_
      4. `Test and Troubleshoot`_
      5. `Document`_
      6. `Other Applications`_

|

Prerequisites
-------------

    Before moving forward with the tutorial, you will need the following:

        1. Create a GitHub repository, :ref:`instructions here<Create a New GitHub Repository>`
        2. Open your repository in a text editor or IDE
        3. Install or Update PanHandler using Docker,  `instructions here`_
        4. Deploy a Next Generation Firewall and Panorama for testing with proper access to GUI and CLI (via SSH)

    .. _instructions here: https://panhandler.readthedocs.io/en/master/running.html#quick-start

|

Set Up the Submodule
--------------------

    In this tutorial we are using `ironskillet-components <https://github.com/PaloAltoNetworks/ironskillet-components>`_,
    which contains all of the sub-skillets for IronSkillet 9.1+.
    Each folder for the PAN-OS version has all of the ``panos`` and ``panorama`` sub-skillets, which are broken down into separate
    files by the XPath that the snippets use to push the configuration. This was done to keep like snippets together, as
    well as group configurations by categories that could be included or excluded based on the preference of the user.
    A breakdown of which sub-skillets correspond to which configuration elements can be found in the
    `IronSkillet documentation <https://iron-skillet.readthedocs.io/en/docs_master/panos_template_guide.html>`_. This
    tutorial uses the 10.0 ``panos`` and ``panorama`` sub-skillets to build several configuration playlists.

|

Add the Submodule
~~~~~~~~~~~~~~~~~

    To add this submodule to the new repository that will contain the playlists, use the following steps:

      * Open the new repository in your IDE or text editor of choice
      * Create a new folder in the root directory called **Submodules**
      * Navigate into that folder
      * Run ``git submodule add https://github.com/PaloAltoNetworks/ironskillet-components.git``


    This will add a copy of the files at that specific commit to your working directory. A ``.gitmodules`` file will
    automatically appear, containing the information about the submodule just added. The sub-skillets from the submodule
    are now able to be included in a playlist. See the :ref:`Git Submodules Overview<Use Submodules>` for more
    information on submodules and how they work.

    The working tree of the repository (green square) and ``.gitmodules`` file (red square) should look like the
    following after following the steps above:

      .. image:: /images/includes_tutorial/submodule_init_IDE.png
         :width: 800

    If you commit and push these changes to your repository, the submodules directory should look like the following:

      .. image:: /images/includes_tutorial/submodule_init_github.png
         :width: 800

    The final repository built from this tutorial can be viewed `here <https://github.com/madelinemccombe/Playlist_Includes_Tutorial>`_.
    If trying to explore the submodule in the tutorial example after cloning, the submodule will need to be initiated and
    updated beforehand. To do this, follow these steps.
        * Clone the repository
        * Open the repository (in an IDE, or ``cd`` in a terminal)
        * Run ``git submodule init``
        * Run ``git submodule update``

    This will use the ``.gitmodules`` file to initiate the ironskillet-components repo in the submodules folder, and then
    pull down the latest commit.

|

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
    it is recommended to use the same ``file_name`` specified as the external file name as the internal skillet **name**
    in the header. Another handy attribute to include is the **collection** a sub-skillet should be included
    in. This is because it is possible to load repositories with many sub-skillets into PanHandler, and it makes it much
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

    When **ironskillet-components** is imported into PanHandler (as of the writing of this tutorial), the following
    collections are available. Each of the sub-skillets within these collections loaded can be run individually.

      .. image:: /images/includes_tutorial/ironskillet_components_collections.png
         :width: 800

    Another best practice to mention is that each sub-skillet should include all information needed to configure all snippets
    by itself. This means that any variables used or XML included in the snippet **must** be included directly in the
    sub-skillet. This allows each sub-skillet to be run and debugged individually, and ensures that the playlist that
    includes the sub-skillet will be able to find all the information needed to run the snippet. Also, it is not possible
    to include a skillet include, which is why any XML must be directly specified within the snippets of a sub-skillet.

    The final recommendation for sub-skillets pertains to the individual snippets within the sub-skillet. Each of the
    snippets in a sub-skillet should include a piece of XML small enough to encompass one action. For example,
    each of the IronSkillet antivirus security profiles are broken down into their own snippets. For the five profiles (Alert-Only,
    Inbound, Outbound, Internal, and Exception), there exists a snippet that can then be included or not included in a playlist.
    This subsetting of information is important to provide granularity in choosing what can be included or excluded from
    a playlist down the road.
    See the `panos_ngfw_profile_antivirus_10_0.skillet.yaml <https://github.com/PaloAltoNetworks/ironskillet-components/blob/main/panos_v10.0/ngfw/panos_ngfw_profile_antivirus_10_0.skillet.yaml>`_
    for more in depth information.

    .. WARNING::
        All snippets and sub-skillets within a submodule repository **must** have unique names. This is required for
        referencing later in playlist includes.

|

Build the Playlist
------------------

    A playlist is nearly identical to any other skillet, with the main difference being the variable and snippet includes.
    This means that the format and headers will be the same as a normal skillet. The following section will walk through
    how to build out a playlist, and show examples of how to include snippets from a sub-skillet in various ways.

|

Set Up the Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Open the new repository in your IDE or text editor of choice
* Create a new folder in the root directory called **Playlists**
* Navigate into that folder
* Create three new files with the following names

    * ``ironskillet_panos_full_10_0.skillet.yaml``
    * ``ironskillet_panos_alert_only_10_0.skillet.yaml``
    * ``ironskillet_panorama_notshared_security_policies_10_0.skillet.yaml``
|


    Playlist file names should follow the pattern ``playlist_name.skillet.yaml``. This allows the skillet players
    (PanHandler, SLI) to recognize that it is a playlist and load the snippets accordingly. In this tutorial, playlist
    names will mention IronSkillet, the device type to be configured (``panos`` or ``panorama``), type of playlist, and the
    PAN-OS version. This gives an accurate description of what is included in the playlist without having to open it
    and try to decipher the skillet includes. See below for what the directory should look like after following these steps.

      .. image:: /images/includes_tutorial/playlist_creation.png
         :width: 400

|

Playlist Preamble
~~~~~~~~~~~~~~~~~

    Each playlist should have a preamble, just like any skillet or sub-skillet. Since there a lot of sub-skillets,
    snippets, and playlists to keep track of with this model and with this tutorial, it is recommended to keep a
    consistent naming scheme. With the sub-skillet names following ``file_name.skillet.yaml``, it is highly recommended
    to use the ``file_name`` portion as the internal skillet or playlist name.

    For example, the playlist file ``ironskillet_panos_full_10_0.skillet.yaml`` would have an internal name of
    ``ironskillet_full_10_0``. Similarly, one of the sub-skillets named ``panos_ngfw_device_system_10_0.skillet.yaml``
    would have an internal skillet name of ``panos_ngfw_device_system_10_0``. This makes it easy to know how to reference
    the sub_skillets in the playlist using skillet includes.

    Specifying the **label**, **description**, **type**, and **collection** are also highly recommended, as they allow
    for easier viewing of the playlists once loaded into PanHandler, and is generally good practice for documentation. In
    particular, the **type** is very important, as that tells the skillet player of your choice what type of snippets
    will be included in a configuration.

    The playlist preambles should look like the following:

    **PAN-OS Full Skeleton**

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


    **PAN-OS Alert Only Skeleton**

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

    **Panorama Not-Shared Security Policies Skeleton**

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
    options to specify. The ``variables:`` and ``snippets:`` sections are blank for now, but will be added to in the
    following sections.

    .. TIP::
        YAML is notoriously finicky about whitespace and formatting. While it's a relatively
        simple structure and easy to learn, it can often also be frustrating to work with.
        A good reference to use to check your YAML syntax is the
        `YAML Lint site <http://www.yamllint.com/>`_.

|

Including Snippets
~~~~~~~~~~~~~~~~~~

    There are different use cases for include snippets from sub-skillets in a playlist. The main ways are listed below, and
    will be highlighted when building out the playlists in the following section:
      * Load entire sub-skillet as is
      * Load only certain snippets from a sub-skillet
      * Load and change the element of snippets in a sub-skillet
      * Load and change XPath of snippets in a sub-skillet (particularly useful with different panorama setups)

**Case 1: Load entire sub-skillet as is**

    To include an entire sub-skillet into a playlist, in the **snippet** section of the *playlist*, create entries that
    have a **name** and **include** set to the internal sub-skillet name defined in the preamble of the sub-skillet. In
    this example, all of the snippets from the Device System sub-skillet will be included in the playlist. Any variables
    in the sub-skillet are included by default.

    .. code-block:: yaml

        snippets:
            - name: panos_ngfw_device_system_10_0
              include: panos_ngfw_device_system_10_0

**Case 2: Load only certain snippets from a sub-skillet**

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


**Case 3: Change the element of a snippet in a sub-skillet**

    Sometimes, there may be one snippet in a sub-skillet that has XML changes needed for a playlist that will overwrite
    the sub-skillet snippet. This can easily be
    done through overwriting the element attribute of the snippet from the sub-skillet. In this example the login banner
    snippet was changed from the default in the Device System sub-skillet, but the other five snippets were kept as is.

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

    .. WARNING::
        Notice that there is an ``include_variables: all`` attribute before the ``include_snippets:``. This is because there
        are variables used in the other snippets that need to be carried over into the playlist. When making overrides to
        snippets using ``include_snippets:``, this is a **required step**.


**Case 4: Change XPath of a snippet in a sub-skillet**

    Similar to the above example, sometimes the XPath of a snippet will need to be changed due to panorama configuration
    (Shared or Not-Shared). The
    XPath specifies where in the XML the element should be placed, which can change due to how the device is set up.
    Panorama in particular often has a different XPath depending if it is a shared or not-shared setup. See
    `IronSkillet Documentation <https://iron-skillet.readthedocs.io/en/docs_master/panorama_template_guide.html>`_ for
    more information about this. In `ironskillet-components <https://github.com/PaloAltoNetworks/ironskillet-components>`_,
    the shared XPath was chosen as the default for the **xpath** attribute in the panorama sub-skillets. In this example,
    a Not-Shared playlist is being built, so the XPath will have to be changed to the not-shared version for some
    sub-skillets. Each snippet in the sub-skillet must be individually included and have the XPath 'overwritten', even
    though the XPath for all snippets in the file might be changing to the same path.

    .. code-block:: yaml

        snippets:
          - name: panorama_tag_10_0
            include: panorama_tag_10_0
            include_snippets:
              - name: ironskillet_tag_ironskillet_version
                xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/tag

    .. NOTE::
        Notice that there is a new ``DEVICE_GROUP`` variable introduced in the changed XPaths. This variable will need to be
        included in the playlist ``variables:`` section.


**Add Snippets to Playlists**

    Using the processes explained above, the sub-skillets should now be added to the playlist as follows:

    .. toggle-header:: class
      :header: **PAN-OS Full Playlist [show/hide snippets]**

          .. code-block:: yaml

            snippets:

              # IronSkillet baseline
              # general device system and setting configs
              - name: panos_ngfw_device_system_mgmt_ip_10_0
                include: panos_ngfw_device_system_mgmt_ip_10_0
              - name: panos_ngfw_device_system_dns_10_0
                include: panos_ngfw_device_system_dns_10_0
              - name: panos_ngfw_device_system_10_0
                include: panos_ngfw_device_system_10_0
              - name: panos_ngfw_device_setting_10_0
                include: panos_ngfw_device_setting_10_0
              - name: panos_ngfw_mgt_config_users_10_0
                include: panos_ngfw_mgt_config_users_10_0
              - name: panos_ngfw_password_complexity_10_0
                include: panos_ngfw_password_complexity_10_0
              # shared log settings and profile
              - name: panos_ngfw_shared_log_settings_10_0
                include: panos_ngfw_shared_log_settings_10_0
              - name: panos_ngfw_shared_log_settings_email_profile_10_0
                include: panos_ngfw_shared_log_settings_email_profile_10_0
              - name: panos_ngfw_shared_log_settings_email_system_critical_10_0
                include: panos_ngfw_shared_log_settings_email_system_critical_10_0
              # tag object
              - name: panos_ngfw_tag_10_0
                include: panos_ngfw_tag_10_0
                # log settings
              - name: panos_ngfw_log_settings_profiles_10_0
                include: panos_ngfw_log_settings_profiles_10_0
              - name: panos_ngfw_log_settings_profiles_email_10_0
                include: panos_ngfw_log_settings_profiles_email_10_0
              # security profiles and profile groups
              - name: panos_ngfw_profile_custom_urlFiltering_10_0
                include: panos_ngfw_profile_custom_urlFiltering_10_0
              - name: panos_ngfw_profile_decryption_10_0
                include: panos_ngfw_profile_decryption_10_0
              - name: panos_ngfw_profile_antivirus_10_0
                include: panos_ngfw_profile_antivirus_10_0
              - name: panos_ngfw_profile_spyware_10_0
                include: panos_ngfw_profile_spyware_10_0
              - name: panos_ngfw_profile_vulnerability_10_0
                include: panos_ngfw_profile_vulnerability_10_0
              - name: panos_ngfw_profile_file-blocking_10_0
                include: panos_ngfw_profile_file-blocking_10_0
              - name: panos_ngfw_profile_urlFiltering_10_0
                include: panos_ngfw_profile_urlFiltering_10_0
              - name: panos_ngfw_profile_wildfire_analysis_10_0
                include: panos_ngfw_profile_wildfire_analysis_10_0
              - name: panos_ngfw_profile_group_10_0
                include: panos_ngfw_profile_group_10_0
              # rulebase
              - name: panos_ngfw_rulebase_default_security_rules_10_0
                include: panos_ngfw_rulebase_default_security_rules_10_0
              - name: panos_ngfw_rulebase_security_10_0
                include: panos_ngfw_rulebase_security_10_0
              - name: panos_ngfw_rulebase_decryption_10_0
                include: panos_ngfw_rulebase_decryption_10_0
              - name: panos_ngfw_zone_protection_10_0
                include: panos_ngfw_zone_protection_10_0
              # reports and email
              - name: panos_ngfw_reports_simple_10_0
                include: panos_ngfw_reports_simple_10_0
              - name: panos_ngfw_report_group_simple_10_0
                include: panos_ngfw_report_group_simple_10_0
              - name: panos_ngfw_email_scheduler_10_0
                include: panos_ngfw_email_scheduler_10_0


    .. toggle-header:: class
      :header: **PAN-OS Alert Only Playlist [show/hide snippets]**

          .. code-block:: yaml

            snippets:

              # tag object
              - name: panos_ngfw_tag_10_0
                include: panos_ngfw_tag_10_0
                include_snippets:
                  - name: ironskillet_tag_ironskillet_version
              # security profiles and profile groups
              - name: panos_ngfw_profile_custom_urlFiltering_10_0
                include: panos_ngfw_profile_custom_urlFiltering_10_0
                include_snippets:
                  - name: ironskillet_custom_url_category_allow
              - name: panos_ngfw_profile_decryption_10_0
                include: panos_ngfw_profile_decryption_10_0
              - name: panos_ngfw_profile_antivirus_10_0
                include: panos_ngfw_profile_antivirus_10_0
                include_snippets:
                  - name: ironskillet_antivirus_alert_all
              - name: panos_ngfw_profile_spyware_10_0
                include: panos_ngfw_profile_spyware_10_0
                include_variables: all
                include_snippets:
                  - name: ironskillet_spyware_alert_all
              - name: panos_ngfw_profile_vulnerability_10_0
                include: panos_ngfw_profile_vulnerability_10_0
                include_snippets:
                  - name: ironskillet_vulnerability_alert_all
              - name: panos_ngfw_profile_file-blocking_10_0
                include: panos_ngfw_profile_file-blocking_10_0
                include_snippets:
                  - name: ironskillet_file_blocking_alert_all
              - name: panos_ngfw_profile_urlFiltering_10_0
                include: panos_ngfw_profile_urlFiltering_10_0
                include_snippets:
                  - name: ironskillet_url_alert_all
              - name: panos_ngfw_profile_wildfire_analysis_10_0
                include: panos_ngfw_profile_wildfire_analysis_10_0
                include_snippets:
                  - name: ironskillet_wildfire_alert_all
              - name: panos_ngfw_profile_group_10_0
                include: panos_ngfw_profile_group_10_0
                include_snippets:
                  - name: ironskillet_profile_group_alert_all


    .. toggle-header:: class
      :header: **Panorama Not-Shared Security Policies Playlist [show/hide snippets]**

          .. code-block:: yaml

            snippets:

              # tag object
              - name: panorama_tag_10_0
                include: panorama_tag_10_0
                include_snippets:
                  - name: ironskillet_tag_ironskillet_version
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/tag
              # security profiles
              - name: panorama_profiles_custom_url_category_10_0
                include: panorama_profiles_custom_url_category_10_0
                include_snippets:
                  - name: ironskillet_custom_url_category_block
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/custom-url-category
                  - name: ironskillet_custom_url_category_allow
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/custom-url-category
                  - name: ironskillet_custom_url_category_no_decrypt
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/custom-url-category
              - name: panorama_profiles_decryption_10_0
                include: panorama_profiles_decryption_10_0
                include_snippets:
                  - name: ironskillet_decryption_profile
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/decryption
              - name: panorama_profiles_virus_10_0
                include: panorama_profiles_virus_10_0
                include_snippets:
                  - name: ironskillet_antivirus_alert_all
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/virus
                  - name: ironskillet_antivirus_outbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/virus
                  - name: ironskillet_antivirus_inbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/virus
                  - name: ironskillet_antivirus_internal
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/virus
                  - name: ironskillet_antivirus_exception
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/virus
              - name: panorama_profiles_spyware_10_0
                include: panorama_profiles_spyware_10_0
                include_variables: all
                include_snippets:
                  - name: ironskillet_spyware_outbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/spyware
                  - name: ironskillet_spyware_inbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/spyware
                  - name: ironskillet_spyware_internal
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/spyware
                  - name: ironskillet_spyware_alert_all
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/spyware
                  - name: ironskillet_spyware_exception
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/spyware
              - name: panorama_profiles_vulnerability_10_0
                include: panorama_profiles_vulnerability_10_0
                include_snippets:
                  - name: ironskillet_vulnerability_outbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/vulnerability
                  - name: ironskillet_vulnerability_inbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/vulnerability
                  - name: ironskillet_vulnerability_internal
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/vulnerability
                  - name: ironskillet_vulnerability_alert_all
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/vulnerability
              - name: panorama_profiles_file_blocking_10_0
                include: panorama_profiles_file_blocking_10_0
                include_snippets:
                  - name: ironskillet_file_blocking_outbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/file-blocking
                  - name: ironskillet_file_blocking_inbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/file-blocking
                  - name: ironskillet_file_blocking_internal
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/file-blocking
                  - name: ironskillet_file_blocking_alert_all
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/file-blocking
              - name: panorama_profiles_url_filtering_10_0
                include: panorama_profiles_url_filtering_10_0
                include_snippets:
                  - name: ironskillet_url_outbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/url-filtering
                  - name: ironskillet_url_alert_all
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/url-filtering
                  - name: ironskillet_url_exception
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/url-filtering
              - name: panorama_profiles_wildfire_analysis_10_0
                include: panorama_profiles_wildfire_analysis_10_0
                include_snippets:
                  - name: ironskillet_wildfire_outbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/wildfire-analysis
                  - name: ironskillet_wildfire_inbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/wildfire-analysis
                  - name: ironskillet_wildfire_internal
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/wildfire-analysis
                  - name: ironskillet_wildfire_alert_all
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profiles/wildfire-analysis
              - name: panorama_profile_group_10_0
                include: panorama_profile_group_10_0
                include_snippets:
                  - name: ironskillet_profile_group_outbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profile-group
                  - name: ironskillet_profile_group_inbound
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profile-group
                  - name: ironskillet_profile_group_internal
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profile-group
                  - name: ironskillet_profile_group_alert_all
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profile-group
                  - name: ironskillet_profile_group_default
                    xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/profile-group

    |

    .. NOTE::
        It is not currently possible to include another include. This means that a playlist cannot effectively include a
        snippet from another playlist that already has a ``include_snippets:`` defined. If this needs to be done, instead
        try referencing the same sub-skillets directly in both playlists.

|

Including Variables
~~~~~~~~~~~~~~~~~~~

    Generally when including snippets from a sub-skillet, all of the variables from the sub-skillet should be loaded as
    well, since they are needed to execute the snippets. This is the default action when loading an entire sub-skillet.
    However, if only certain snippets are loaded, or if changes to the snippet are made in the playlist, it is important to
    specify how variables are included. Basically, anytime the ``include_snippets:`` attribute is used, ``include_variables:``
    should also be specified, as long as there are variables in the sub-skillet to include.

    Take the XPath override example from the previous section:

    .. code-block:: yaml

        snippets:
          - name: panorama_tag_10_0
            include: panorama_tag_10_0
            include_snippets:
              - name: ironskillet_tag_ironskillet_version
                xpath: /config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{{DEVICE_GROUP}}']/tag

    The ``panorama_tag_10_0`` sub-skillet does not have any variables in it, so in this case, an ``include_variables:`` is
    not necessary. However, if including snippets from a different sub-skillet, and ``include_variables: all`` should be
    added right above the ``include_snippets:``.

    This also highlights another important factor, which is that any *new* variables introduced to the playlist in
    snippet changes must be included in the ``variables:`` section of the playlist. Here, the **DEVICE_GROUP** variable should be
    added to the Panorama Not-Shared Security Profile playlist as follows:

    .. code-block:: yaml

        variables:
          - name: DEVICE_GROUP
            description: Device-group name for Panorama
            default: sample_devicegroup
            type_hint: text
            help_text: creates a sample device-group with IronSkillet configuration elements


    There are a few other use cases that might come up:

      * Menu options for custom loads (checkboxes in a workflow)
      * When conditional includes
      * See the `Workflow Tutorial <https://skilletbuilder.readthedocs.io/en/latest/tutorials/tutorial_workflow.html#add-variables-to-the-skillet>`_ for more examples of variable usage

|

Test and Troubleshoot
---------------------

    Now that the skillet has been pushed to GitHub, the skillet can be imported or loaded into one of the skillet
    player tools, such as PanHandler or SLI, for testing. This Tutorial will show how to test and debug using PanHandler.
    Make sure to `update PanHandler to the latest release <https://panhandler.readthedocs.io/en/master/running.html#quick-start>`_,
    as playlists are a new feature.

    Testing playlists involves three main components:

        1. User-facing variables
        2. Overall sequence of sub-skillets
        3. Overrides of any sub-skillet features

    Continue reading to see how to test these components in PanHandler.

|

Import the Playlists
~~~~~~~~~~~~~~~~~~~~

    First, import the repository into PanHandler. The **Import Playlists** option in the PanHandler Menu will take you
    this page. Then fill out the *Repository Name* (can be anything you want) and the *URL*, and hit the **Submit** button.

        .. image:: /images/includes_tutorial/import_playlist_panhandler.png
         :width: 800

    If the repository did load correctly, then it should take you to the **Repository Detail** page. This page has
    a Details overview section, a preview of the latest commits to the repository, the skillets (and playlists) found
    and loaded from the repository, and links to the collections found from the skillets. An option to checkout a
    different branch from the default is all the way at the bottom of the page.

    If the playlist did not load correctly into PanHandler, an error message should pop up
    naming the playlist and snippet where the error occurred. This could be due to an incorrect name reference, missing
    variables, or general YAML syntax errors. If this happens, fix what was named in the error, commit/push those changes,
    and then hit the **Update To Latest** button (green oval) at the top of the repository **Details** page.

        .. image:: /images/includes_tutorial/repository_details_panhandler.png
         :width: 800


    .. WARNING::
        If there are other repositories (for example PANW IronSkillet) already loaded into PanHandler that have
        the same skillet names as the playlists, the new playlists will not load. This will not throw an error, so it will
        appear that the new repository loaded correctly, but it could be missing playlists. To fix this, remove both repositories
        with duplicate names and try importing the playlist repository again.

|

Debug and Play the Playlist
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Once the repository is loaded into PanHandler without any errors, there are a few playlist-specific features that
    should be double checked. To play a playlist, click on the name of the playlist from the repository **Details** page,
    or the Collection page the playlist belongs to (**IronSkillet Playlists** in this tutorial).


    All variables loaded into a skillet will show up in the first menu when evaluating the playlist. The correct
    variable menus are shown below for each playlist.

    **PAN-OS Full**

        .. image:: /images/includes_tutorial/panos_full_variables.png
         :width: 800

    **PAN-OS Alert Only**

        .. image:: /images/includes_tutorial/alert_only_variables.png
         :width: 800

    **Panorama Not-Shared Security Policies**

        .. image:: /images/includes_tutorial/panorama_variables.png
         :width: 800

    After hitting the **Submit** button at the bottom right of the variables menu, the **Target Information** menu will
    show up. Here, a valid NGFW or Panorama IP, username, and password should be inputted. **DO NOT HIT SUBMIT**, but
    instead click the **Debug** button (pink box). This opens up a super helpful menu that shows how the XML snippets
    rendered from the playlist and variables specified. This **Debug** view will be used to double-check three
    important aspects of playlists below.

        .. image:: /images/includes_tutorial/debug_button_panhandler.png
         :width: 800

    The **Debug** view has a section for each snippet that is included in the playlist. Each of these sections is broken
    out into the snippet name (blue text), JSON format of what is being loaded, the XPath the configuration will be pushed
    to (pink text), and then the XML to be pushed (red and black text). An example is shown below for the IronSkillet
    version tag snippet in the **PAN-OS Alert Only** playlist.

        .. image:: /images/includes_tutorial/debug_overview.png
         :width: 800

    .. NOTE::
        The blue text is formatted so that is joins the name of the sub-skillet and the name of the snippet with a period.
        In the example above, the ``ironskillet_tag_ironskillet_version`` snippet was pulled from the ``panos_ngfw_tag_10_0``
        sub-skillet. This is useful when tracking the location of an error when debugging.

    **Check variables loaded correctly**

        The first way to check this is through the variable menus shown above. Each menu should list out all variables
        expected to be included in the playlist, along with any characteristics specified for the variable. If variables
        are not showing up in the menu as expected, make sure that there is an ``include_variables:`` specified in the snippet
        that the variables are pulling from. Alternatively, try adding the variable to the ``variables:`` section of the
        playlist.

        The second way to check the variables is on the **Debug** page. All XML snippets shown (red and black text) should have
        the variables populated according to what was specified in the variable menu. No ``{{ VARIABLE_NAME }}`` text should
        be left. For example, in the **PAN-OS Full** playlist, The primary and secondary DNS servers have been specified.

            .. image:: /images/includes_tutorial/dns_variable_load.png
             :width: 800


    **Check XML snippets and XPaths loaded correctly**

        When only including certain snippets from a sub-skillet, it is good practice to confirm that *only* those snippets were
        loaded from the playlist. Using the **PAN-OS Alert-Only** playlist, it is easy to confirm that only the Alert profiles
        were loaded for each of the Security Policy sub-skillets. There should be 10 snippets total (8 alert policies, alert
        profile group, and the IronSkillet tag). When scrolling down the **Debug** page, there should only be 10 sections
        that start with the blue text header (which indicates 10 snippets loaded).


    **Confirm XPath and XML overrides**

        If specifying a different XPath or XML for a snippet than is pre-defined in the sub-skillet, it is a good idea to
        confirm that those changes went through. For XPaths, this is simple to view on the **Debug** page, as each snippet
        loaded has the XPath tied to it in pink text. As can be seen below, the Not-Shared Panorama XPaths for device group
        went through, and the variable loaded in correctly.

            .. image:: /images/includes_tutorial/xpath_override.png
             :width: 800

        Any XML overrides specified can also be confirmed in the same manner as the XPath. Double check that the XML
        loaded matches what is explicitly written in the playlist versus what would normally be included from the sub-skillet.


    Some common errors are:

        * Using the incorrect sub-skillet or snippet name in an ``include_snippets:`` attribute
        * Not including all variables needed
        * Using the same name between sub-skillets and playlists, or between separate repositories loaded in PanHandler

|

Edit, Push, Test
~~~~~~~~~~~~~~~~

    As changes are made to the skillets while debugging, the following steps should be taken to see the changes reflected
    in PanHandler:
        * Commit and Push changes from the IDE/code editor to GitHub
        * In PanHandler open up the **Imported Repositories** page using the **Skillet Repositories** menu option (blue box)

    Once on the **Imported Repositories** page, there are two options to update:

    1. Open up the playlist repository using the Details button (green box below) and click the **Update to Latest** button (green oval below) OR

    2. Click the **Update All Repositories** button (purple box below)


    *Imported Repositories Page*

        .. image:: /images/includes_tutorial/panhandler_imported_repositories.png
         :width: 800

    *Details Page*

        .. image:: /images/includes_tutorial/repository_details_panhandler.png
         :width: 800

|

Document
--------

    The final stage is to document key details about the skillet to provide contextual information
    to the user community. Documentation is especially important when using the Playlist Framework, as there is
    additional content being included and referenced through the submodule and sub-skillets.

|

README.md
~~~~~~~~~

    The playlist repository has an empty placeholder ``README.md`` that should give an overview of the solution.
    The ``README.md`` should provide skillet-specific details such as what the playlist does, variable input descriptions,
    and caveats and requirements. Some playlist-specific information to include:

    * Information about the submodules and the content they contain
    * A reminder that when cloning a repository with a submodule, existing submodules will need to be initiated and updated before use. To do this, run the following commands:

        * Clone the repository ``git clone <clone_link>``
        * ``git submodule init``
        * ``git submodule update``

    * Remind users to update the submodule as needed, since that is not done automatically as new commits are released. To do this, run the following commands:

        * Open the playlist repository
        * Run ``git submodule update --remote --merge``
        * Commit and Push any changes


    ``README.md`` uses the markdown formatting language. Numerous examples can be found in the skillet files. There is also a
    wide array of `markdown cheat sheets`_ you can find using Google searches.
    Below are a few common markdown elements you can use in your documentation. Most IDEs can display the user view
    as you edit the markdown file.

    .. _markdown cheat sheets: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

        +-------------------------------------------------------------------------------------+
        | Markdown syntax options                                                             |
        +=====================================================================================+
        | `#, ##, ###` for header text levels (H1, H2, H3, etc.)                              |
        +-------------------------------------------------------------------------------------+
        | `**text**` for bold text                                                            |
        +-------------------------------------------------------------------------------------+
        | `*text*` or `_text_` to underline                                                   |
        +-------------------------------------------------------------------------------------+
        | `1. text` to create numbered lists                                                  |
        +-------------------------------------------------------------------------------------+
        | `* text`, `+ text`, `- text` for bullet style lists                                 |
        +-------------------------------------------------------------------------------------+
        | `[text](url)` for inline web links                                                  |
        +-------------------------------------------------------------------------------------+
        | \`test\` to highlight a text string                                                 |
        +-------------------------------------------------------------------------------------+
        | \`\`\`text block - one or more lines\`\`\` to create a highlighted text block       |
        +-------------------------------------------------------------------------------------+

    .. TIP::
        To view markdown edits for existing GitHub repos, click on the README.md file, then use the **Raw**
        option to display the output as raw markdown text. From here, you can copy and paste or review formatting.

    Paste this sample ``README.md`` file into your repository and push to GitHub.

    .. code-block:: md

        # Sample Playlist Includes Skillet

        This is used in the training material as part of the Playlist Includes tutorial.

        The solution utilizes three playlists:

        1. A full IronSkillet PAN-OS 10.0 configuration
        2. An Alert-Only Security Profiles IronSkillet PAN-OS 10.0 configuration
            * only includes Alert-Only Security Profiles
            * the IronSkillet version tag is included for documentation purposes
        3. A IronSkillet Not-Shared Panorama 10.0 Security Profiles configuration
            * only includes Security Profiles for a Not-Shared Panorama configuration
            * the IronSkillet version tag is included for documentation purposes

        These playlists were based off of some of the playlists in the
        [IronSkillet 10.1 branch](https://github.com/PaloAltoNetworks/iron-skillet/tree/panos_v10.1/playlists).
        Check out the [README](https://github.com/PaloAltoNetworks/iron-skillet/blob/panos_v10.1/playlists/README.md)
        for more information on the playlists and content they contain.

        Configuration elements in the playlists pull from the
        [ironskillet-components](https://github.com/PaloAltoNetworks/ironskillet-components) submodule, which has several
        sub-skillets. All skillet-player tools (PanHandler, SLI, etc.) will be able to read in the snippets from the
        sub-skillets in the submodule using the `include_snippets` attribute in the playlists. However, the submodule
        has a few steps for upkeep when using content locally.

        When cloning this repository, the submodule will need to be initiated and updated before being able to use it.
        To do this, run the following commands:
        * Clone the repository: `git clone <clone_link>`
        * Initiate the submodule: `git submodule init`
        * Update the submodule to the latest commit: `git submodule update`

        It is also recommended to update the submodule as needed (not done automatically as new commits are released). It
        is necessary to commit and push changes in order to see the latest commit pulled into a skillet player. This
        can be done using the following steps:
        * Open the repository
        * Update the submodule: `git submodule update --remote --merge`
        * Commit and Push any changes


    **Support Policy Text**

        Skillets are not part of Palo Alto Networks supported product so the policy text is appended to the
        README file to specify skillets are not supported. Sample text to copy/paste is found in the `SkilletBuilder repo README`_

    .. _SkilletBuilder repo README: https://raw.githubusercontent.com/PaloAltoNetworks/SkilletBuilder/master/README.md

|

LIVEcommunity
~~~~~~~~~~~~~~

  Playlists can be shared in the Live community as Community or Personal skillets. Community Skillets
  are expected to have a higher quality of testing, documentation, and ongoing support. Personal skillets
  can be shared as-is to create awareness and eventually become upgraded as Community Skillets.

|

Other Applications
------------------

    With the Playlist Framework, there are many new options for how skillets can be built. A few further ideas to spark
    inspiration are listed below.
        * Any repo with developed skillets can be added as a submodule
        * Existing skillets can be broken into smaller sub-skillets and included in a playlist
        * If submodules are too complex, the sub-skillets can be added directly to the host repository
        * Playlist Includes can see any sub-skillets within the playlist repository directory or submodule
        * More than one submodule can be added to a repository

    Feel free to reach out with any questions! See the :ref:`Feedback Section<SkilletBuilder Feedback>`
    for more information on how to do so.
