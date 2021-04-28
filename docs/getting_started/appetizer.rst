Building and Testing with Appetizer
===================================

Quickstart
~~~~~~~~~~

Appetizer is a docker image the builds a simple GUI driven web app for any git repository
that contains skillets. This makes is very easy to try out automation tools that use skillets.

.. code-block:: bash

    docker run -it --rm -p 9000:8080 -e 'REPO=https://github.com/PaloAltoNetworks/SkilletBuilder.git' \
      -e 'BRANCH=develop' \
      --name "Skillet Builder" registry.gitlab.com/panw-gse/as/appetizer

In the above example, the local port `9000` will be used to access the generated Skillet Builder application.
