# Sample Workflow Skillet

This is used in the training material as part of the SkilletBuilder
[Workflow tutorial](https://skilletbuilder.readthedocs.io/en/latest/tutorials/tutorial_workflow.html).

The solution utilizes three skillets:

1. A validation skillet to verify the running configuration
2. A configuration skillet to configure:
    * tag: create a tag using inputs for name, description, and color
    * external-list: create an edl using inputs for name, description, and url
    * security policies: inbound and outbound security policies referencing the edl and tag names
3. A template skillet to output the workflow end

The configuration skillet was taken from the Configuration Tutorial for Skillet Builder documentation 
(https://skilletbuilder.readthedocs.io/en/latest/tutorials/tutorial_configuration.html#).

## Workflow Sequence 

This workflow skillet begins by prompting the user to input the workflow menu options, described below.

Depending on the *assess_options* result, a validation skillet will be run next to verify that an 
External Dynamic List object is configured for the *edl_url* inputted by the user. In addition,
it will validate that two security policies exist denying traffic from and to the EDL object. 

Next, the workflow prompts the user to fill in forms about the EDL and tag information. With this information, 
the automation pushes a configuration that creates a tag object, EDL object, and two security policies. 

Again, depending on the *assess_options* result, the same validation skillet will be run. 

Finally, a template skillet is executed that outputs a **Workflow Completed** message, so the user is 
clear about the workflow's end. 


## Variables

### Main Workflow Menu Options:

* *TARGET_IP*: IP of firewall to validate and configure
* *TARGET_USERNAME*: Username of firewall management user
* *TARGET_PASSWORD*: Password of the above user
* *edl_url*: URL used for the External Dynamic List
* *assess_options*: Checkbox for validation skillet execution orders (beginning and/or 
  end of the workflow)

### Configuration Sub-Skillet Options:

* *tag_name*: Name of a newly created tag that is used in the security rules
* *tag_description*: Text field to describe the tag
* *tag_color*: Dropdown menu mapping color names to color numbers (required in the XML configuration)

* *edl_name*: Name of the newly created External Dynamic List
* *edl_description*: Text field used to describe the External Dynamic List

The 'recurring' value for the EDL is set to *five-minutes*. This could be added as a variable but for this example, the
value is considered a recommended practice so not configurable in the skillet.

The EDL type is set to IP since used in the security policy and is not configurable in the skillet.

### Configuration Sub-Skillet Security Policy Referencing Variables

The security policy does not have its own variables asking for rule name, zones, or actions. The rules are
hardcoded with 'any' for most attributes and action as _deny_ to block traffic matching the EDL IP list.

The security rule names use the EDL name followed by '-in' and '-out' to create unique security policies for each
EDL. This is denoted in the yaml file with ```{{ edl_name }}``` included in the rule name.

