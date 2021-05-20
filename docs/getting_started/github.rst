Skillets and GitHub
===================

  :ref: `The Skillet Framework` uses GitHub as the primary option for storing skillets.

Create a New GitHub Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Login to GitHub and select 'New' to add a new repository.

  **INSERT PIC HERE**

  Enter details for the repo. Adding a README.md file and an MIT license are recommended. You can also add a .gitignore
  file, primarily to ignore pushing any EDI directories such as .idea/ used by PyCharm.

  **INSERT PIC HERE**

  Once the repository is created, click the green 'Code' button to clone either the HTTPS or SSH URL. For the purposes
  of working with PanHandler and later tutorials, the SSH option is recommended. Click the 'Clipboard' button to copy
  the URL.

  **INSERT PIC HERE**

Add SSH Keys from PanHandler into GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  If you are using the SSH URL to import a GitHub repository into PanHandler, you must add your PanHandler SSH keys into
  your GitHub account.

  In PanHandler, navigate to the top right of the page to find the 'paloalto' user settings.
  Click the dropdown menu and locate the 'View SSH Public Key' option.

  **INSERT PIC HERE**

  On this screen you should see your ssh key. Copy the entire key (include 'ssh-rsa' at the beginning and 'PAN_CNC' at
  the end.

  **INSERT PIC HERE**

  Navigate back to GitHub. In the top right, click the dropdown menu next to your user icon and click 'Settings'.
  Find the 'SSH and GPG keys' settings and click the green 'New SSH key' button.

  **INSERT PIC HERE**

  Give the SSH key a title and paste the key copied from PanHandler. Click the green 'Add SSH key' button.

  **INSERT PIC HERE**

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
  Open this directory in your text editor/IDE. If you don't already have a README.md file, you can add one now.
  Follow the 'Configuration Tutorial' to learn what to add in the README file

  **INSERT PIC HERE**

  Create a sub-directory that will contain the skillet content. Name the sub-directory something relevant to the skillet
  that will be created here.

  Add a file with the name '.skillet.yaml' inside the sub-directory and another README.md.

  **INSERT PIC HERE**

  Leave these files blank for now; they will be populated later on in the tutorial.


Use Submodules
~~~~~~~~~~~~~~

Coming Soon...