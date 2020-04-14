Testing Skillets with PanHandler
================================

Since panHandler supports all skillet types and supports the SkilletBuilder tools, it is recommended for skillet design,
build, and test.

For first time panHandler users, reference the `panHandler Quickstart Guide`_ in the Live Skillet District.

    .. _panHandler Quickstart Guide: https://live.paloaltonetworks.com/t5/Skillet-Tools/Install-and-Get-Started-With-Panhandler/ta-p/307916

|

Loading the Master or Develop Versions
--------------------------------------

PanHandler runs in a Docker container, the master build tagged as 'latest'.

There is also a develop branch with new features and updates. Although not the recommended release, some users may
want to work with develop and explore new features. Some skillets being developed may also be dependent on newer features.

Checking your Current Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can check your panHandler version on the Welcome page. The bottom center will show the version. You will either see
a version number or ``DEV`` if running a develop version.

Under the version is a notification message showing if you have the most recent version of PanHandler.


Updating or Running the Dev Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script will install or update to the latest 'dev' image for Panhandler. This is recommended for developers
or power-users who understand this code may be unstable and not all features may work all the time.

.. code-block:: bash

    curl -s -k -L http://bit.ly/34kXVEn  | bash


Updating or Running the Master Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This script will install or update to the latest 'master' image for Panhandler. This is the version used
by users as the official version.

.. code-block:: bash

    curl -s -k -L http://bit.ly/2xui5gM | bash


You can toggle between the two versions by running one of the curl commands


When switching between dev and latest clear the cache with:

::

    http://localhost:9999/clear_cache

|

Pruning Images
--------------

Over time you may accumulate panHandler image files especially if moving between develop and master versions.

You can view the images with:

::

    docker images

If you see multiple panHandler images you can recover disk space using:

::

    docker image prune

This will remove all unused images.

|

Playing Skillets from the Repo Detail Page
------------------------------------------

Instead of going back and forth between the repo detail andcollections page, you can run skillets from the repo Detail page.

  .. image:: images/panhandler_repo_detail.png
     :width: 600

    1. click ``Update to Latest`` to import the latest repo changes
    2. check that your updates were imported reviewing messages in the ``Latest Updates`` section
    3. play the skillet by clicking the label in the ``Metadata files`` section

This allows you to refresh and play all from a single page.

|

Using Environments to Switch between Devices
--------------------------------------------

Instead of entering in the target IP address, user and password information when playing a skillet you can create
panHandler environments for each target devices. This is especially useful if you are switching between a NGFW
and Panorama or have multiple lab or cloud devices for test.

Checkout the `panHandler Environment documentation`_ for more details about configuring and using Environments.

    .. _panHandler Environment documentation: https://panhandler.readthedocs.io/en/master/environments.html#


|

Testing with the SkilletBuilder Tools
-------------------------------------

Various :ref:`Skillet Builder Tools` allow for testing and debug. Import into panHandler and look for the Skillet Builder
collection.

Key test tools include:

    * Skillet Test Tool to load yaml-based skillets to a device without Github interactions
    * Configuration Explorer to look at configuration elements based on XPath

|

Checking Variable Values with Context
-------------------------------------

Choose ``View Context`` from the top right pulldown in panHandler.

The output will be a current list of variable names and the current value cached in panHandler. This is useful to
check variable values especially when testing logic conditionals.

|

Using Template Skillets to View Values
--------------------------------------

When creating workflows or wanting to see how panHandler handles values, you can create a simple :ref:`template` skillet for
testing.

Variables can be added into the template text file as ``{{ variable }}`` and when rendered, the screen output will show
any text include the variable values.

This can also be used to help format any messaging outputs that use variables.

|

Using Local Variables to Test Workflow Logic
--------------------------------------------

In workflow development you may be using a value from a validation, panos, rest or other skillet as input to another skillet.
This second skillet may have conditionals based on the output from the first skillet.

To manually create a pass/fail or true/false condition you can temporarily add a type_hint = text variable to the second
skillet. When that skillet is played you will see the passed value in the web form and can then edit that value when
playing the skillet.

This alleviates the need to constantly update the queried device with different configurations in order to test the workflow
and associated logic conditions.

