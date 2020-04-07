Switching between Latest and Develop Containers
===============================================

PanHandler runs in a Docker container, the main build tagged as 'latest'.

There is also a develop branch with new features and updates. Although not the recommended release, some users may
want to work with develop and explore new features. Some skillets being developed may also be dependent on newer features.


Updating or Running the Dev Version
-----------------------------------

This script will install or update to the latest 'dev' image for Panhandler. This is recommended for developers
or power-users who understand this code may be unstable and not all features may work all the time.

.. code-block:: bash

    curl -s -k -L http://bit.ly/34kXVEn  | bash


Updating or Running the Master Version
--------------------------------------

This script will install or update to the latest 'master' image for Panhandler. This is the version used
by users as the official version.

.. code-block:: bash

    curl -s -k -L http://bit.ly/2xui5gM | bash


You can toggle between the two versions by running one of the curl commands


When switching between dev and latest clear the cache with:

::

    http://localhost:9999/clear_cache

Pruning Images
--------------

If switching between versions and upgrading over time you may accumulate panHandler image files.

You can view the images with:

::

    docker images

If you see multiple panHandler images you can recover disk space using:

::

    docker image prune

This will remove all unused images.

