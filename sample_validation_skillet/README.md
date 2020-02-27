# Validation Tutorial Sample Skillet

This sample does four tests:

* check that NTP servers are configured
* check that password complexity is enabled with a 12 char minimum password
* check that all url-filtering profiles block category malware
* check that all allow security policies include a profile or group

## check ntp server configuration

This uses ```capture_object``` for ntp configuration element and then a custom validation filter ```tag_present```
to look for the configuration tag <ntp-server-address> under primary and secondary server configuration

The test will pass if both are configured

## check password complexity

This uses ```capture_object``` for the password complexity element and then a custom validation filter ```element_value```
to check that the xml text is 'yes' for enabled and 'greater than or equal to 12' for the minimumm length.

The test will pass if enabled and the minimum length is >= 12

## check that all url-filtering profiles block category malware

This uses ```capture_list``` to create a list 'url_profiles_block_malware' of all url-filtering profiles
with malware set to block.

A second  ```capture_list``` is used to get all url-filtering profiles names, filter out the 'good profiles' with malware
set to block based on the 'url_profiles_block_malware' list, and put the remaining profiles in a new list 'url_profiles_not_blocking_malware'.

Ideally the list 'url_profiles_not_blocking_malware' should be empty so the test will pass if list length = 0.

The fail message will show a list of url-filtering profile names that do not have malware set to block.

## check that all allow security policies have a security profile or group

This uses ```capture_list``` to create a list 'security_policies_with_profile_or_group' for all security policies that
have a profile or profile group.

A second  ```capture_list``` is used to get all security policy names with action allow, filter out the 'good policies'
that are found in 'security_policies_with_profile_or_group' list, and put the remaining profiles in a
new list 'allow_security_policies_without_profile'.

Ideally the list 'allow_security_policies_without_profile' should be empty so the test will pass if list length = 0.

The fail message will show a list of security policy names with action allow yet do not have a security profile or group.



