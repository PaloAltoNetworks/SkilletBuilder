Skillets and GitHub
===================

:ref:`The Skillet Framework` uses GitHub as the primary option for storing skillets.

 Click below to jump to a specific section:

 1. `Create a New Github Repository`_

 2. `Add SSH Keys from PanHandler into Github`_

 3. `Import a Repository into PanHandler`_

 4. `Create a Skillet Directory`_

 5. `Use Submodules`_

Create a New GitHub Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Login to GitHub and select **New** to add a new repository.

 .. image:: /images/skillet_utilities/new_repo_button.png
  :width: 300
|
  Enter details for the repo. Adding a ``README.md`` file and an MIT license are recommended. You can also add a ``.gitignore``
  file, primarily to ignore pushing any EDI directories such as .idea/ used by PyCharm.

    .. image:: /images/skillet_utilities/create_repo_settings.png
      :width: 600
|
  Once the repository is created, click the green **Code** button to clone either the HTTPS or SSH URL. For the purposes
  of working with PanHandler and later tutorials, the SSH option is recommended. Click the **Clipboard** button to copy
  the URL.

    .. image:: /images/skillet_utilities/clone_ssh_link.png
      :width: 400
|
Add SSH Keys from PanHandler into GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  If you are using the SSH URL to import a GitHub repository into PanHandler, you must add your PanHandler SSH keys into
  your GitHub account.

  In PanHandler, navigate to the top right of the page to find the 'paloalto' user settings.
  Click the *dropdown menu* and select **View SSH Public Key**.

    .. image:: /images/skillet_utilities/view_ssh_public_key.png
      :width: 250
|
  On this screen you should see your ssh key. Copy the entire key (include 'ssh-rsa' at the beginning and 'PAN_CNC' at
  the end.

    .. image:: /images/skillet_utilities/copy_ssh_key.png
      :width: 600
|
  Navigate back to GitHub. In the top right, click the *dropdown menu* next to your user icon and click **Settings**.

    .. image:: /images/skillet_utilities/github_settings.png
      :width: 200
|
  Find the *SSH and GPG keys* settings and click the green **New SSH key** button.

    .. image:: /images/skillet_utilities/github_new_ssh_key.png
      :width: 500
|
  Give the SSH key a title and paste the key copied from PanHandler. Click the green **Add SSH key** button.

    .. image:: /images/skillet_utilities/github_add_key.png
      :width: 600
|
Import a Repository into PanHandler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Please refer to the instructions above in order to copy the GitHub repository link to your clipboard.
  Navigate to PanHandler. Click the *PanHandler* dropdown menu in the top left corner and select **Import Skillets**.

    .. image:: /images/skillet_utilities/panhandler_dropdown.png
      :width: 250
|
  Scroll down the page and locate the *Import Repository* Section. Enter the name of the repository and paste the URL
  you copied from the above step. Click **Submit**. Make sure you are using the SSH URL as opposed to the HTTPS URL.

    .. image:: /images/skillet_utilities/import_skillet.png
      :width: 700
|
Create a Skillet Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Prerequisites for creating a skillet directory:

  - A new repository created on GitHub
  - Text editor/IDE of choice (PyCharm, Sublime, etc.)

  From the steps above, make sure that you've cloned the link for the repo you just created.
  In a terminal/bash shell enter the following:

  .. code-block:: bash

    > git clone {GitHub repository link}

  This will add a directory to your local machine with the contents of the repository.
  Open this directory in your text editor/IDE. If you don't already have a ``README.md`` file, you can add one now.
  Follow the 'Configuration Tutorial' to learn what to add in the ``README.md`` file.

  Create a sub-directory that will contain the skillet content. Name the sub-directory something relevant to the skillet
  that will be created here.

  Add a file with the name ``.skillet.yaml`` inside the sub-directory and another ``README.md``.

    .. image:: /images/skillet_utilities/skillet_directory_files.png
      :width: 400

  Leave these files blank for now; they will be populated later on in the tutorial.


Use Submodules
~~~~~~~~~~~~~~

A submodule is a reference within a host Github repository that points to a specific commit in an external repository.
Submodules are used to include external content in a repository in a manner that can be easy updates and referenced.
In terms of skillets, the Playlist Include skillet framework uses submodules to reference

To initiate a submodule within a host repository, use the command ``git submodule init <submodule_clone_link>``. This is
similar to cloning a repository to a host machine. The contents of the submodule repository will be 'copied' to the
working tree of the host repository and will be viewable if the host repository is cloned. It is recommended to navigate
to a folder within the host repository before initiating a submodule to keep your working tree clean. On GitHub, the
submodule will appear similarly to the ones below.

  .. image:: /images/skillet_framework/submodule_in_repository.png
     :width: 800

When a submodule is added to a host repository for the first time, a new ``.gitmodules`` file will be created automatically.
This file contains information about the connection between the submodule and host repository. Adding more than one
submodule will create additional entries in the ``.gitmodules`` file.

An example of an entry in the ``.gitmodules`` file is:

.. code-block:: yaml

    [submodule "submodules/ironskillet-components"]
        path = submodules/ironskillet-components
        url = https://gitlab.com/panw-gse/as/ironskillet-components.git

Submodules are tied to a specific commit when initiated, so they will need to be updated to pull the newest
content from the submodule repository as needed. This can be done using the ``git submodule update`` command. This will
update all submodules added within a host repository to the latest commit.