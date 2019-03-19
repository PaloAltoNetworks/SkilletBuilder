SkilletBuilder start to finish
==============================

This is the complete list of steps for template creation, testing, and publishing. The assumption is a new github repo
owned by the user, PAN-OS NGFW as the configured device, and panhandler for testing.

Examples will also use pycharm for template and metadata creation although any text editor can be used.


Creating a new github repository
--------------------------------

CONSIDER A SKELETON REPO WITH A FORK VS NEWLY CREATED REPO. DOING NEW REPO HERE TO CAPTURE STEPS.

1. If new to github go to github.com to create a new user account

2. Once logged in, go to https://github.com/new to add a new repo

ADD IN NEW REPO IMAGE

3. Enter a repo name, description. Can choose private initially. `Create Repo`
* include README.md for quick description
* MIT license??

4. From the new repo page, click the green button for `Clone or download' and copy the repo clone info

ADD IN CLONE REPO IMAGE


Creating a local github repo
----------------------------

OPTIONS OTHER THAN GITHUB TO EDIT AND TEST?? PANHANDLER IS GITHUB ONLY FOR SKILLET LOADING

Assume git is installed on the local machine. Additional links for this??
Also the user should install pycharm or have a text editor available. Preferred is an xml and yaml friendly editor.

5. go to a projects or user directory enter 'git clone' and paste the repo name from step 4

This copies the remote repo to your local machine for editing. Note the directory used to archive the repo.


Quick commands for git
----------------------

By default git and github use the master branch. It is easy to create and switch
between branches for various software releases, testing, etc.

* `git branch` shows the branch you are currently editing

* `git status` shows modified files, branch status

* `git pull origin {branch name}` downloads the latest updates from the remote repo

* `git checkout {branch name}` switches between branches

* `git checkout -b {branch name}` creates a new local branch and switches to that branch


Creating a new branch for editing and testing
---------------------------------------------

This example uses pycharm for template editing and management. Pycharm makes it easy to edit and view templates,
autosaves changes, and has an integrated terminal window for git commands and repo management.

6. Run `pycharm` and open the directory for the newly cloned repo

7. Open the `terminal` panel found in View > Tool Windows if not visible in the current window

For new templates we will use a non-master branch specific to the sample data

8. `git checkout -b sample` creates a new branch called `sample`

Use `git branch` to validate the current branch name.

9. Create a new directory in the repo directory using a simple, descriptive name

This repo has a directory called `sample` with reference metadata and xml files.

You are now ready to build a skillet related to the new directory name.

Configure the NGFW with GUI or CLI
----------------------------------

This stage is based on user preference, GUI or CLI. It is also where the expertise of the user to create the configuration
is key to have all elements captured for the new skillet.


10. Before adding the new template configuration, locally save the fw configuration (eg. skillet-baseline.xml)

11. Configure the new skillet changes noting all elements of the configuration that have been modified


Add the .meta-cnc.yaml file
---------------------------

This section adds the base metadata file in preparation for variable and snippet additions

12. Create or copy an existing .meta-cnc.yaml file (eg. the one in the samples directory)

13. Edit the header information (name, label, description, group)

The variables and snippets sections will be populated in the following steps.

Grab the xml elements
---------------------

The API configuration requires the use of xml config elements and the associated xpaths. This reference shows how to
grab these using the CLI console.

The xml config snippets will be added to the skillet directory. Variables to be added in future steps. The xpath and
xml file names will be added to the .meta-cnc.yaml file to set load order, where to add into the NGFW config, and
the xml config element to add.

14. SSH or use console access to the NGFW

15. Once logged in, use `debug cli on` to assist with xpath capture

16. Also use `set cli config-output xml` to show config output in xml format

17. In configure mode, enter `show {config section}` to output xml and xpath

INSERT THE XML AND XPATH CONSOLE IMAGE

18. Copy the xpath for the first config element

Example shows /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag

19. Paste into .meta-cnc.yaml under the snippets section, xpath entry.

20. Add the associated name (eg. tag) and to-be-added filename (eg. tag.xml)

INSERT IMAGE FROM SAMPLE YAML FILE SHOWING THE SNIPPETS SECTION

Reference:

snippets:
  - name: tag
    xpath: /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/tag
    file: tag.xml

21. Repeat steps 17-20 for all of the config snippets specific to the new skillet


Adding variables to the skillet configuration
---------------------------------------------

Variables allow for deployment-specific values to be entered by the user with the help of the panhandler UI.

22. In each of the xml snippet files, replace existing text with the `{{ variable_name }}` notation.

The variable names can be reused across xml files when the same value is to be used.

23. Compile a list of all variables

Use of grep -r '{{' . |  cut -d'{' -f3 | awk '{ print $1 }' | sort -u  to create a quick list

24. Add all variables into the variables section of the .meta-cnc.yaml file including description, default and type_hint

The default and type_hint are used by panhandler to auto-generate web form fields.


Review the skillet directory information
----------------------------------------

Before saving to github and testing with panhandler, review the skillet information.

* .meta-cnc.yaml values
    + skillet name, label are set properly and unique
    + variables have all been added with correct defaults and type_hints
    + snippets with xml files and xpaths are added using first guess load order

* xml files
    + snippets have variables inserted
    + no overlap between xml element and xpath


Commit and push to github
-------------------------

At this stage, the local git data must be pushed to github to add to panhandler.

25. from the repo directory use `git add .` to add changes to repo commits

26. enter `git commit -m " {a message based on the change} " to commit changes to git

27. enter `git push origin {branch name} to upload changes to github


Import the repo to panhandler
-----------------------------

Full documentation is at panhandler.readthedocs.io

Make sure docker is installed on the local machine.

28. enter `docker run -t -p 80:80 paloaltonetworks/panhandler:latest`

or `docker run -t -p 9999:80 paloaltonetworks/panhandler:latest` to use 9999 in the event port 80 is used on the local
machine.

This will pull down and run panhandler on the local machine. The -t runs docker in terminal mode showing the output
of the panhandler code including xpath loading information. This is useful for troubleshooting template loading.

29. access panhandler using a local browser, http://localhost:80 or http://localhost:9999 (match to docker run port)

30. Login using paloalto/panhandler

31. Click on the lock to set the local environment (top right of the panhandler window)

32. If a non lab-in-a-box firewall being configured (eg. 192.168.55.10) clone the pan-os env. Enter name/description.

33. Enter TARGET_IP and ip address and update. Also username/password as required.

34. `Load` this environment to tell panhandler what firewall to be configured

35. Choose 'import template' to add a new repo

36. Enter the repo description, link (see step 4), and branch to import.

Once loaded you can go to PANHANDLER > REPOSITORIES to see loaded repos. From the newly imported repo you can see the
metadata lists (aka the menu options in the library) and update the repo when changes need to be pulled from the repo.

Run the Skillet to test
-----------------------

Ensure the firewall is up and running. The panhandler environment must match firewall parameters (IP, username, password)

37. Select PANHANDLER > TEMPLATE LIBRARY to see the list of skillets by type (eg. Panorama, PAN-OS, templates)

38. Choose the template type (eg. PAN-OS)

39. From the list select the skillet to be loaded

40. Enter form data and step through the form fields

41. Validate the IP, username, password for the device to be configured and Submit

42. Monitor the docker terminal to validate all skillets load.

Troubleshooting the skillet
---------------------------

If an error, the message will indicate which xml snippet failed to load.

The output messages look like xpath, present, xpath, etc. Typically the 'is present' message indicates the prior
xpath/xml snippet successfully loaded. Either a specific message from the api or a system message will be specific to
the next xpath/xml element in the load order. Focus here

Typical xml errors to look at:

* incorrect xpath
* errors in the xml snippet
* overlap of the xpath and the xml config (example 'tag' at th end of the xpath and <tag> in the xml snippet
* mismatch between config elements and sw version (loading 8.1 config into an 8.0 firewall)
* syntax error in the .meta-cnc.yaml file (it is very specific about spaces, alignment)
* load order issues (eg. xml element references an object that isn't loaded yet)
* incorrect variables names in the xml file vs what is listed in the .meta-cnc.yaml file

If errors are found:

For changes to the configuration, start with steps 14-20 to make GUI/CLI changes then update the local xml element. The
same steps to validate the xpath for the config snippets.

If variable changes required, use steps 22-24 to check variables and update the .meta-cnc.yaml file

Once changes are made, use steps 25-27 to add/commit/push changes to github. Then go to PANHANDLER > REPOSITORIES and
choose the `Detail` of the tested repo. In the repo details, select `Update to Latest` to retrieve the changes pushed
to github.

Once the repo is updated, follow steps 37-42 to rerun the API configuration and look for errors.

The Skillet is ready to go
--------------------------

Once the skillet has been tested using the prior steps and successfully loads and works on the NGFW, you are ready to
share your skillet.

?? What to do here to publish the repo and share ??

Sanctioned vs Unsanctioned
Move repo to public or if a fork, merge back to the mothership
Box/Loop tools to submit and have published to github
