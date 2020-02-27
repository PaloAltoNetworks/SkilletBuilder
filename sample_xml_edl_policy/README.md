# Sample Configuration Skillet

This is used in the training material as part of the tutorial.

The skillet has 3 xml elements:

* tag: create a tag using inputs for name, description, and color
* external-list: create an edl using inputs for name, description, and url
* security policies: inbound and outbound security policies referencing the edl and tag names

## variables

tag_name: name of a newly created tag and used in the security rules
tag_description: text field to describe the tag
tag_color: dropdown mapping color names to color numbers (required in the xml configuration)

edl_name: name of the newly created external-list
edl_description: text field used to describe the external-list
edl_url: url used for the external-list

The 'recurring' value for the EDL is set to five-minutes. This could be added as a variable but for this example, the
value is considered a recommended practice so not configurable in the skillet.

The EDL type is set to IP since used in the security policy and is not configurable in the skillet.

## security policy referencing variables

The security policy does not have its own variables asking for rule name, zones, or actions. The rules are
hardcoded with 'any' for most attributes and action as deny to block traffic matching the EDL IP list.

The security rule names use the EDL name followed by '-in' and '-out' to create unique security policies for each
EDL. This is denoted in the yaml file with ```{{ edl_name }}``` included in the rule name.

