Basic Configuration With Set Commands
=====================================


Overview
--------

This tutorial is designed to help the user get familiar with using set commands to bring up and apply basic configs to their NGFW. By then end of this tutorial the user should be able to alter their firewall manually through the Command Line Interface(CLI) with set commands. All set/op commands that can be entered in the CLI manually can also be transformed into an automation playlist in the form of a skillet. This allows the user to run a series of set commands to easily configure their NGFW with just the click of a button. The configuration tutorial will create a simple configuration including:

  - An IP External Dynamic List (EDL) object
  - A tag object
  - Security rules (Inbound and Outbound) referencing the EDL and tag objects

This Basic Config with Set Commands tutorial will show the user how to:
  
  - Access and configure the Next Generation Firewall(NGFW) through the web UI and CLI
  - Capture configuration differences made on the NGFW into set commands and automation skillets
  - Learn how to use Panhandler tooling
  - Learn how to use the Skillet Line Interface(SLI) tool on the CLI
  - Learn the basics of using GitHub and repositories

The video below provides an end-to-end perspective for building a configuration skillet and can be used as a complement
to the documentation content.

.. raw:: html

    <iframe src="https://paloaltonetworks.hosted.panopto.com/Panopto/Pages/Embed.aspx?
    id=17392613-262a-4606-a11a-ab6c010b894e&autoplay=false&offerviewer=true&showtitle=true&showbrand=false&start=0&
    interactivity=all" width=720 height=405 style="border: 1px solid #464646;" allowfullscreen allow="autoplay"></iframe>


Navigation Menu
~~~~~~~~~~~~~~~

You can click on the hyperlink menu below to quickly navigate to different parts of the tutorial.

1. `Prerequisites`_

2. `Building Skillets with Set Commands`_

3. `Test and Troubleshoot`_

4. `Document`_


Prerequisites
-------------

Before moving forward with the tutorial, please ensure the following prerequisites have been fulfilled.

* Have an up and running NGFW Virtual Machine(VM)
* A GitHub_ account with access permissions to edit repository content, please refer to "Insert link to getting started page here"
* Docker_ desktop installed, active and running on your local machine, please refer to "Insert link to getting started page here"
* Ability to access the NGFW device via GUI[1][2], SSH/CLI[3] and API
* For users wishing to work through the command line have SLI_ set up and ready to go, please refer to "Insert link to getting started page here"

  * SLI can be set up locally on your machine to run quick and efficient commands on your local CLI. SLI is a CLI interface used for interacting with Skillets. Please refer to and follow the steps in the linked SLI_ page to get started
* For users wishing to work through the browser UI log into PanHandler_ and be able to import/run Skillets, please refer to "Insert link to getting started page here"
    
It may also be useful to review the following topics before getting started:

- :ref:`jinjaandskillets`

.. _PanHandler: https://panhandler.readthedocs.io/en/master/
.. _GitHub: https://github.com
.. _Docker: https://www.docker.com
.. _SLI: https://pypi.org/project/sli/

.. [1] Log in to the NGFW UI by entering this, *https://X.X.X.X* (with your NGFW's management IP replacing the X's), into the web browser URL bar.
.. [2] If you reach a warning page during this step, click advanced settings and choose the proceed to webpage option.
.. [3] Log in to the NGFW via CLI by opening a terminal/bash window on your local machine and entering this, *ssh {username}@{X.X.X.X}* (with your NGFW's management IP replacing the X's).

This tutorial will be split into 4 main sections below and can either be done by reading the document or by watching the tutorial videos. There is a video tutorial for achieving the intended results via use of the PanHandler UI tool and the SLI command line interface tool.


|
Building Skillets with Set Commands
-----------------------------------

Create the Configuration in the NGFW
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Before modifying the configuration, ensure you have a snapshot of the `before/baseline` configuration of your NGFW saved, 
    we will use this saved snapshot to perform an offline configuration difference later. To do this navigate through 
    **Device->Setup->Operations->Save named configuration snapshot** to save the current NGFW config.
    
    .. image:: /images/set_command_tutorial/save_config_snapshot.png
        :width: 600
|
    The tutorial examples use the GUI to create the external dynamic list(EDL), tag, and security rules. Before starting these steps,
    make sure you commit the most recent changes made to the NGFW, to do this click on the **Commit** button located at the top-right 
    of the NGFW GUI.
    
    .. image:: /images/set_command_tutorial/commit_button.png
        :width: 600
|    
    Now after committing we want to start making changes to our NGFW. First we want to configure the external-list object with a name,
    description, and source URL. To get to the `External Dynamic List` section on your NGFW navigate through the following, 
    **Objects->External Dynamic Lists->Add**. 
    
    .. image:: /images/set_command_tutorial/add_edl.png
        :width: 600 
    
    Once in the correct place make the necessary changes as seen below. Click the **OK** button to save the changes.

    .. image:: /images/set_command_tutorial/External_list.png
        :width: 600

|
    Next we need to configure the tag object with a name, color, and comments (description) and then click the **OK** button. Tag
    objects are found by clicking through the following, **Objects->Tags->Add**.
 
    .. image:: /images/set_command_tutorial/find_tag.png
        :width: 600
|        
    Once you have hit the add button make necessary changes as seen below and click the **OK** button.

    .. image:: /images/set_command_tutorial/tag_configure.png
        :width: 600
        
|
    .. TIP::
        The skillet will only add a single tag to the configuration.
        However, the GUI shows a color name while the set command is based on a color number.
        The use of multiple tag entries is used to extract the color values.
        So note that in some cases the GUI and set commands can use different values and we can use 
        sample configs like this to discover those values.
|

    Finally, configure inbound and outbound security rules referencing the tag and external-list. In order to add security rules please
    navigate through the following, **Policy->Security->Add**. Note that the rule names are prepended with the EDL name. In later 
    steps variables are used in the rule names to map the EDL and ensure rule names are unique.

    .. image:: /images/set_command_tutorial/navigate_security_policy.png
        :width: 800
|      
    Once you have hit the add button make necessary changes as seen below, please make sure you have all the configurations shown 
    below copied into your security policy.      

    .. image:: /images/set_command_tutorial/security_policy_add.png
        :width: 800
|
 
    If you want to be able to generate your set commands skillet in offline mode later in the tutorial, don't forget to commit and save
    a modified configuration snapshot of your NGFW here. With your baseline and modified configurations saved you can export the files to your 
    local machine for later use! You can do this by navigating to, **Devices->Setup->Operations->Export named configuration snapshot**.
  
    .. image:: /images/set_command_tutorial/export_snapshot.png
        :width: 800
|

Generate the Set Commands Skillet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    In this section of the tutorial we are going to use the PanHandler utility and our NGFW to create a set commands skillet. 
    To begin, start up PanHandler by clicking on the **PanHandler** tab at the top and then clicking on **Skillet Repositories**. 
    
    .. image:: /images/set_command_tutorial/panhandler_nav.png
        :width: 600
|    
    Scroll down until you find the `SkilletBuilder` repository and then click on the **Details** button. 
    
    .. image:: /images/set_command_tutorial/skilletbuilder_details.png
        :width: 600
|   
    Here you want to locate and click on the **Create Skillet** button.
    
    .. image:: /images/set_command_tutorial/create_skillet.png
        :width: 600
|       
    Now we want to extract the difference between the baseline and modified NGFW configurations as set commands. To do this directly from
    your connected NGFW find the box on this page that says `Generate Set Commands From PAN-OS` and then click on **Generate CLI**. 
    
    .. image:: /images/set_command_tutorial/generate_set_cli.png
        :width: 600
        
|        
    .. NOTE::
        There is also an option to upload previously saved NGFW XML files manually to the PanHandler SkilletBuilder utility from your local machine. 
        To do this you would have to find the box titled `Generate Set Commands From Uploaded Files` from the previous step and click on the 
        blue **Upload** button. On the resulting page titled `Skillet Generator` you can upload your previously saved NGFW configuration files 
        under the `Pre-Configuration` and `Post-Configuration` sections.
      
|
    Once at the `Skillet Generator` page fill in your NGFW information and click **Submit**.
    
    .. image:: /images/set_command_tutorial/skillet_generator_fill.png
        :width: 600
|        
        
    You will then end up at another `Skillet Generator` page where you will need to choose some NGFW configuration options to 
    pull from in a couple of drop-down menus. Under the `Pre-Configuration Source` menu, choose the baseline configuration.
    Under the `Post Configuration Source` menu choose your modified configuration that you want to get the config difference between.
    After the correct NGFW commit versions are chosen hit **Submit**.
    
    .. image:: /images/set_command_tutorial/pre_post_choose_cli.png
        :width: 600
|    
    After the files are added and submitted, the next stage of the workflow is a web form for the YAML file preamble attributes.
    Suggested tutorial inputs for this section are as follows:

      * Skillet ID: tag_edl_tutorial
      * Skillet Label: Tutorial skillet
      * Skillet description: The tutorial skillet demonstrates the use of various config snippets and variables
      * Skillet type: ``Template``
      * Branch: Local
      * Commit Message: Create Tutorial Skillet
      
    .. image:: /images/set_command_tutorial/preamble_yaml_fill.png
        :width: 600   
|
    Once everything has been entered, clicking on the blue **Submit** button results in a screen titled `Skillet Editor`. This page 
    will showcase parts of the skillet that you just created as well as a snippets section containing all of your set commands from
    the config diff.

    The rendered YAML file contains:

      * Preamble populated with the web form values
      * Placeholder variables section
      * Snippets section with set command entries where each diff is found

      
Working with Snippets and Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
      
    In section we will be editing the snippets and variables sections that were just rendered in the YAML file.
      
    To access the set commands found within the snippets you want to view the snippets in `edit` mode by clicking the blue **Edit** 
    button all the way on the right of the snippets section. 
      
    .. image:: /images/set_command_tutorial/snippets_edit.png
        :width: 600 
        
|          
    Upon clicking the **edit** button you will land at an `Edit template snippet` page showcasing all the set commands retrieved from
    the config diff. Here is where we can get into working with a cool templating language called `Jinja`_, to allow for user inputted
    value substitution within the variables in our skillets. Thankfully with this skillet editor tool there is a very simple and easy way
    to transform plain text within our set commands into Jinja variables. Click into the small blue **Edit** button near the bottom right
    of the screen again.
    
    .. image:: /images/set_command_tutorial/set_command_snippet_edit.png
        :width: 600
        
|       
    .. NOTE::
        Order matters with set commands! The *Generate Set CLI Commands* skillet won't always output set commands in the right order.
        For example it may output the commands in such a way that it will try to load in a security policy before the EDL is created, an
        example of this is shown in the screenshot below. As you can see the `set rulebase security rules` set commands are appearing before
        the set commands that create the edl. This would fail if you input it into the NGFW CLI since the EDL doesn't exist yet.
    
   .. toggle-header:: class
      :header: **Set Commands Out of Order Example**
          
          .. image:: /images/set_command_tutorial/out_of_order.png
              :width: 400 
        
|   
    This will take us to a page titled `Edit Text`, this is where we can make text substitutions for variables. For example if we 
    wanted to change all instances of the text "tag_name" into a jinja variable you would enter in "tag_name" to the left box and then
    whatever you wanted the variable to be called in the right box. It is best practice to name your variables something identifiable 
    and descriptive. Next hit the **Replace** button containing 2 arrows pointing in opposite directions to create your variables! Dont 
    forget to click **Update** twice to confirm and save your changes!
    
    .. image:: /images/set_command_tutorial/switch_variables.png
        :width: 600

    .. NOTE::
      For the purpose of this Tutorial you should have 6 variables in the variables section of the Skillet Editor. Please refer
      to the SkilletBuilder `variables`_ documentation for a more in depth look at the different kinds of variables and their use
      cases.

|
    Once the **Update** button has been pushed and changes have been made you will be brought back to the `Skillet Editor` screen from 
    before. Here you should see that the previously empty variables section has now been populated with your newly created variables. you
    can now click into the blue **Edit** buttons to the right of the variable names to edit their descriptions, names, etc. For example, 
    let's edit our `tag_color` variable to contain a dropdown menu option. For your convenience we have provided a handy table below to show 
    what tag colors map to what values.

    .. image:: /images/set_command_tutorial/skillet_editor_update.png
        :width: 600
    
    +-------------------------------------------------------------------------------------+
    | Tag Color Mappings                                                                  |
    +=====================================================================================+
    | Red - color1                                                                        |
    +-------------------------------------------------------------------------------------+
    | Green - color2                                                                      |
    +-------------------------------------------------------------------------------------+
    | Blue - color3                                                                       |
    +-------------------------------------------------------------------------------------+
    | Yellow - color4                                                                     |
    +-------------------------------------------------------------------------------------+
    | Copper - color5                                                                     |
    +-------------------------------------------------------------------------------------+
    | Orange - color6                                                                     |
    +-------------------------------------------------------------------------------------+
    | Purple - color7                                                                     |
    +-------------------------------------------------------------------------------------+
    | Gray - color8                                                                       |
    +-------------------------------------------------------------------------------------+
    
|
    On the `Edit Variable` page click on the **Variable Type** dropdown menu and choose the **Dropdown Select** option. From here you can type
    in key:value pairs similar to a dictionary and then click on the **+** sign on the right to add them as dropdown menu options for your
    variable color type. Add all the color options you would like and then hit **Update** at the bottom to save the changes in your variable.
    
    .. image:: /images/set_command_tutorial/dropdown.png
        :width: 600
    
    Back on the `Skillet Editor` page, we can save all aspects of our generated skillet by clicking the blue **Save** button at the bottom right 
    of the screen.
        
    .. image:: /images/set_command_tutorial/save_skillet.png
        :width: 600
     
|
    Now that the skillet has been saved in PanHandler it will show up as a skillet on the next page titled `Repository Detail for
    SkilletBuilder`. 
    
    .. image:: /images/set_command_tutorial/repo_detail_skilletbuilder.png
        :width: 600
    
|
    On this page simply scroll down until you find your saved skillet, in this case it should be called `Tutorial Skillet`. Locate the 
    skillet and click on the **Gear** icon to inspect the skillets raw YAML data file. Choosing to click into the **Gear** should allow 
    you to see the fully function skillets YAML file including all generated set commands within as well as the variables that were updated 
    prior.
    
    .. image:: /images/set_command_tutorial/inspect_tutorial.png
        :width: 600 
   
|
    You can also click the **Edit** button on this page to access your skillet in `edit` mode and make changes.
        
    .. image:: /images/set_command_tutorial/tutorial_edit.png
        :width: 600 
    
|
    Your raw skillet YAML file should look something like the screenshots below.
    
    .. toggle-header:: class
        :header: **Skillet Raw Yaml**

            .. image:: /images/set_command_tutorial/skillet_metadata1.png
              :width: 600
          |

            .. image:: /images/set_command_tutorial/skillet_metadata2.png
              :width: 600
          |
    
    At this point you should have a fully functioning set commands skillet! However we aren't done yet, you always
    want to be sure to test your skillet for any possible issues before committing it back to your repository. Please
    refer to the `Testing and Troubleshooting` section in this tutorial for more guidance on testing methods.
  
        
.. _`Jinja`: https://skilletbuilder.readthedocs.io/en/latest/building_blocks/jinja_and_skillets.html
.. _`variables`: https://skilletbuilder.readthedocs.io/en/latest/reference_examples/variables.html


|

Using SLI to Perform a Configuration Difference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    In this section we will be going over how to use the SLI tool in the CLI to get a config diff. First head into the folder in which
    you cloned the SLI repository, activate the venv and perform the pip install command. For more in depth guidance please refer to 
    `SLI documentation`_.
  
    .. image:: /images/set_command_tutorial/sli_setup.png
        :width: 600
      
|
    From here all that needs to be done is run following simple SLI command.
  
    .. code-block:: bash
  
      > sli diff -of set
    
    After entering this command you will be prompted to enter your NGFW information, after entering the correct information you will
    receive all of the config differences output as set commands as can be seen below.
  
    .. image:: /images/set_command_tutorial/sli_output.png
        :width: 600
      
|      
    From here you can copy all of these set commands and paste them into a .txt file in the same directory as your SLI cloned repo.
  
    .. image:: /images/set_command_tutorial/sli_set_txt.png
        :width: 600  
  
|
    While in that directory you can run SLI and pass in the .txt file containing all of the set commands to automatically configure the
    NGFW with all provided set commands.
  
    .. code-block:: bash
  
      > sli load_set -uc set_commands.txt
  
    .. image:: /images/set_command_tutorial/sli_load_txt.png
      :width: 600    
      
|
    .. NOTE:: 
      Another handy function that comes with SLI is its ability to locate errors in specific set commands. If any of the set commands
      entered in through SLI are faulty, SLI will error out and print the faulty set command line for your viewing pleasure!
    
    .. TIP::
        You can also add a -v to the end of the above command to make it look like, `sli load_set -uc {text_file} -v`. This will
        output all the set commands being passed to the NGFW as they SLI is running in place of the black loading bar showcasing
        % complete.
      
    At this point all configurations should have been made in your NGFW, simply log in to validate and commit the changes in your NGFW.

.. _`SLI documentation`: https://gitlab.com/panw-gse/as/sli


Test and Troubleshoot
---------------------

Debug
~~~~~

    Now that all the desired changes have been made to the Skillet, it is recommended to use the `Debug` tool to check for errors.

    At the bottom of the Skillet Editor page, click the green **Debug** button.

    .. image:: /images/set_command_tutorial/debug_button.png
        :width: 600  

    This tool allows you to do some quick testing of the snippets to make sure they function as expected.
    In the context section, enter values based on your information:

    .. image:: /images/set_command_tutorial/context_section.png
        :width: 600  

    In the 'Step Through Snippets' section click the **Play** button to execute the snippet.
    Expected output may look something like the screenshot below:

    .. image:: /images/set_command_tutorial/play_snippet.png
        :width: 600 

    Continue to step through the snippets. If you encounter an error, be sure to check the syntax in the 'Context' section.
    Look for missing quotes '"', colons ':', etc.

    Once you have finished debugging, click the orange **Dismiss** button towards the bottom to close the page.

Play the Skillet
~~~~~~~~~~~~~~~~

    On the Repository Details page, click on the Skillet in the 'Skillets' section.

    .. image:: /images/set_command_tutorial/test_skillet.png
        :width: 600 

    Now you should recognize all the variables that you added earlier on in the tutorial.
    Add your desired values for the variables. and click **Submit**.

    .. image:: /images/set_command_tutorial/render_template.png
        :width: 600 

    After submitting your customized variable names you will reach a page titled `Output`. Here you will be shown the output
    of your set command template skillet. You should see all the proper set commands with the respective variable names
    substituted where they should be. 

    .. image:: /images/set_command_tutorial/template_skillet_output.png
        :width: 600 

    If you receive errors messages, common issues may be:

      - Snippet load order
      - Set command load order, make sure set commands were loaded in the right order
      - Variable typos in the snippet section or not included in the variables section
      - YAML file invalidity
      
      
    .. TIP::
       YAML is notoriously finicky about whitespace and formatting. While it's a relatively simple structure and easy to learn,
       it can often also be frustrating to work with. A good reference to use to check that your
       YAML syntax is up to standard is the `YAML Lint site <http://www.yamllint.com/>`_.
       Test against a live device and fix/tune as needed.

    Continue to edit, push, and test the skillet until it is free of errors and performs as expected.


Commit and Save
~~~~~~~~~~~~~~~

  The skillet is now ready to be saved and committed to the GitHub repository.
  At the bottom of the Skillet Editor, enter a relevant commit message:

  **INSERT PIC HERE**

  Click 'Save'.

  Now your skillet should show up in the 'Skillets' section of the Repository Details.

  **INSERT PIC HERE**


Document
--------

    The final stage is to document key details about the skillet to provide contextual information to the user community.

    The skillet repo created has a placeholder README.md and earlier in the tutorial we created a README.md within
    the skillet directory. The main README gives an overview of the repo for any user viewing the page. The skillet
    directory README should provide skillet-specific details such as what the skillet does, variable input descriptions,
    and caveats and requirements.
    
    README.md uses the markdown format. Numerous examples can be found in the skillet files. There is also a
    wide array of `markdown cheat sheets`_ you can find using Google searches.
    Below are a few common markdown elements you can use in your documentation. Most EDIs can display the user view
    as you edit the markdown file.
    
.. _`markdown cheat sheets`: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

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
      To view markdown edits in existing GitHub repos, click on the README.md file, then use the ``Raw``
      option to display the output as raw markdown text. From here you can copy-paste or review formatting.
      
    Sample README.md file for the tutorial skillet. Paste into the skillet README file and push to Github.
    View the skillet repo to see the updated page text.






