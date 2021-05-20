Building and Testing with SLI
=============================

  Please refer to the `SLI Documentation <https://pypi.org/project/sli/>`_ for more information on installing and using SLI

Install SLI
~~~~~~~~~~~

  In a terminal/bash shell enter the following to create a virtual python environment and install SLI.

  .. code-block:: bash

      > mkdir {directory name of your choice}
      > cd {directory from step above}
      > python3 -m venv ./venv (Create the venv)
      > source ./venv/bin/activate (Activate the venv)
      > pip install sli


Use SLI to Perform a Configuration Difference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  SLI can extract the difference between two configuration files.
  See instructions above for installing SLI locally on your machine.

  To get the difference between two configs in XML format, run the following command:

  .. code-block:: bash

    > sli diff -of xml

  After entering this command, you will be prompted to enter your NGFW information. After entering the correct
  information you will receive the configuration differences between the candidate and running configs output as
  XML (seen below).

  **INSERT PIC HERE**

  You can utilize these XML snippets to create a skillet.


Play a Skillet with SLI
~~~~~~~~~~~~~~~~~~~~~~~

  Clone your skillet in the SLI directory you are currently working in.

  .. code-block:: bash

     > git clone {skillet repo}


  To load and view the skillets available in the current working directory, type the following:

  .. code-block:: bash

    > sli load


  You can also specify a skillet directory by:

  .. code-block:: bash

    > sli load -sd {skillet directory}


  To play the skillet, type the following:

  .. code-block:: bash

    > sli configure --name {name of skillet}


  To specify a directory when playing the skillet enter:

  .. code-block:: bash

    > sli configure -sd {skillet directory} --name {name of skillet}


  After entering this command, you will be prompted to enter your NGFW information and the values to the variables
  in the skillet.

  **INSERT PIC HERE**

  .. NOTE::
    If tag_color is a variable in the skillet, you must enter the color number (color1, color2, etc.) and NOT
    the actual color, otherwise the skillet will not work. Please refer to the color mappings table in the configuration
    tutorial.



