# Basic Validation Skillet elements

These are the basic checks done by the tutorial validation skillet

## does a named EDL exists

Uses `attribute_present` to look for an EDL by name

## is the correct url being used

Takes the input url variables and uses `element_value` to match that the
url value is configured properly

## edl update interval

Checks the update interval, aka 'recurring' to see if it matches the
input variable. This uses `tag_present` where the time interval is
a an xml tag

## is the edl used in the security rules

Uses `element_contains` to look at a named security rule and check
for the edl name

