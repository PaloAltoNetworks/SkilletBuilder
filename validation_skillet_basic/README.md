# Basic Validation Skillet elements

These are the basic checks done by the tutorial validation skillet.
The validation configuration uses the skilletBuilder tutorial configuration
in this repo with an EDL, tag, and security policy skillet.

## does a named EDL exists using a variable input value

Uses `attribute_present` to look for an EDL by matching a var input name and return `True` if found.

This is for the attribute validation where the value of interest is contained inside a tag.

```yaml
  - name: check_external_list_exists
    label: external-list {{ edl_name }} exists
    test: external_list | attribute_present('entry', 'name', edl_name)
    fail_message: did not find {{ edl_name }} in the configuration
```

## does a named EDL exists using a fixed name value

Uses `attribute_present` to look for an EDL by explicit name and return `True` if found. 

This is for the attribute validation where the value of interest is contained inside a tag.

```yaml
  - name: check_external_list_fixed
    label: fixed naming check - edl called some_edl exists
    test: external_list | attribute_present('entry', 'name', 'some_edl')
    fail_message: did not find edl called some_edl in the configuration
```

## does a named EDL not exist

Uses `attribute_absent` to look for an EDL by matching a var input name and return `False` if found.

This is for the attribute validation where the value of interest is contained inside a tag.
Absent is used when the desired state is to not have that attribute/object in the config file.

```yaml
  - name: check_external_list_missing
    label: external-list {{ edl_name }} is not already configured
    test: external_list | attribute_absent('entry', 'name', edl_name)
    fail_message: found external-list {{ edl_name }} already configured
```

## is the test url found

Uses `element_value`  and `==` to match the input url value and return `True` if the same.

Uses the `when` conditional such that this test is skipped if the named EDL
does not exist and the test is irrelevant.


```yaml
  - name: check_edl_url
    when: external_list | attribute_present('entry', 'name', edl_name)
    label: EDL url is configured
    test: external_list_named | element_value('type.ip.url') == edl_url
    fail_message: the edl url {{ edl_url }} is not configured
```

## is the test url not found

Uses `element_value` and `!=` to not match the input url value and return `True` if different.

Uses the `when` conditional such that this test is skipped if the named EDL
does not exist and the test is irrelevant.

```yaml
  - name: check_edl_not_url
    when: external_list | attribute_present('entry', 'name', edl_name)
    label: EDL url is different than input url
    test: external_list_named | element_value('type.ip.url') != edl_url
    fail_message: the edl url {{ edl_url }} is already configured
```

## edl update interval matches the var value
Uses `tag_present` to check a value that is an element tag embedded in the xpath
and return `True` if found.

Uses the `when` conditional such that this test is skipped if the named EDL
does not exist and the test is irrelevant.

The ~ is used to concatenate a string and input variable edl_recurring to
send a complete string for validation. If a variable is not used, it would just
be a single string surrounded by quotes.

```yaml
  - name: check_edl_recurring_interval
    when: external_list | attribute_present('entry', 'name', edl_name)
    label: EDL update interval is {{ edl_recurring }}
    test: external_list_named | tag_present('type.ip.' ~ edl_recurring)
    fail_message: the edl is not configured for {{ edl_recurring }} updates
```

## edl update interval matches a fixed value
Uses `tag_present` to check a value that is an element tag embedded in the xpath
and return `True` if found.

Uses the `when` conditional such that this test is skipped if the named EDL
does not exist and the test is irrelevant.

```yaml
  - name: check_edl_recurring_interval_fixed
    when: external_list | attribute_present('entry', 'name', edl_name)
    label: EDL update interval is five-minute - fixed as five minutes
    test: external_list_named | tag_present('type.ip.five-minute')
    fail_message: the edl is not configured for five-minute updates
```

## edl update interval does not match the var value
Uses `tag_absent` to check a value that is an element tag embedded in the xpath
and return `False` if found.

Uses the `when` conditional such that this test is skipped if the named EDL
does not exist and the test is irrelevant.

The ~ is used to concatenate a string and input variable edl_recurring to
send a complete string for validation. If a variable is not used, it would just
be a single string surrounded by quotes.

```yaml
  - name: check_edl_not_recurring_interval
    when: external_list | attribute_present('entry', 'name', edl_name)
    label: EDL update interval is NOT {{ edl_recurring }}
    test: external_list_named | tag_absent('type.ip.{{ edl_recurring }}')
    fail_message: an existing recurring value of {{ edl_recurring }} already exists
```

## is the edl used in an inbound security rule

Uses `element_value_contains` to check a value found in the xpath with multiple
entries and return `True` if found.

Uses the `when` conditional such that this test is skipped if the named EDL
does not exist and the test is irrelevant.

```yaml
  - name: security_rules_inbound_edl
    when: external_list | attribute_present('entry', 'name', edl_name)
    label: EDL in associated inbound security policy
    test: security_rule_inbound_edl | element_value_contains('source.member', edl_name)
    fail_message: the edl {{ edl_name }} is used in an inbound security rule
```

## is the edl used in an outbound security rule

Uses `element_value_contains` to check a value found in the xpath with multiple
entries and return `True` if found.

Uses the `when` conditional such that this test is skipped if the named EDL
does not exist and the test is irrelevant.

```yaml
  - name: security_rules_outbound_edl
    when: external_list | attribute_present('entry', 'name', edl_name)
    label: EDL in associated outbound security policy
    test: security_rule_outbound_edl | element_value_contains('destination.member', edl_name)
    fail_message: the edl {{ edl_name }} is used in an outbound security rule
```

