# Use Case Agnostic samples as example

### .meta-cnc.yaml

Metadata file used by panhandler to

* set menu labels and help descriptions

* variable names, default, and web field form types

* snippet load order, xpaths, and associated xml files

### tag.xml and hostname.xml

Sample xml files to be loaded with the associated xpaths and load order.

The xml files also use the jinja ```{{ variable_name }}``` notation
with the variable names captured in the .meta-cnc.yaml file.



