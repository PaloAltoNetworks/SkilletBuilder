Capture Output
==============

Various models for capturing output to variables used in:

    * validation tests
    * dynamic menu options
    * text render outputs


capture_list
------------

  Use to capture a list of values. This example creates a list of all URL-filtering profile names and stores them
  in the varilable 'url_filtering_profiles'.

  .. code-block:: yaml

      # get list of all url profiles for debug example
      - name: url_filtering_profiles
        capture_list: |-
          /config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/profiles/url-filtering/entry/@name

  Using a sample IronSkillet configuration, the output list is

  .. code-block:: json

    url_filtering_profiles = [
      "Outbound-URL",
      "Alert-Only-URL",
      "Exception-URL"
    ]


capture_object
--------------

  Use to capture an XML element as a dict object. This example creates the dict using all password-complexity
  configuration elements and stores it in a dict variable called 'password_complexity'.

  .. code-block:: yaml

     - name: password_complexity
        capture_object: /config/mgt-config/password-complexity

  Using a sample IronSkillet configuration, the output dict in json format is

  .. code-block:: json

    password_complexity = {
      "password-complexity": {
        "enabled": "yes",
        "minimum-length": "12",
        "minimum-uppercase-letters": "1",
        "minimum-lowercase-letters": "1",
        "minimum-numeric-letters": "1",
        "minimum-special-characters": "1",
        "block-username-inclusion": "yes",
        "password-history-count": "24",
        "new-password-differs-by-characters": "3"
      }
    }


capture_value
-------------

  Use to capture a single value and store as a variable. This example captures the value of the password-complexity
  enabled setting and stores it in a variable called 'password_complexity_enabled'.

  .. code-block:: yaml

    - name: password_complexity_enabled
      capture_value: /config/mgt-config/password-complexity/enabled/text()


  Using a sample IronSkillet configuration, the captured value is

  .. code-block:: json

    password_complexity_enabled = "yes"


capture_pattern
---------------

TODO: define and determine if still used