# SkilletBuilder
Docs and tutorial for Skillet template building

The main documentation provides generic manual instruction for template
creation.

There is also a tutorial branch walking the user through an example
Skillet use case.

## Quick start

You can use Appetizer to quickly spin up a Skillet Builder container to test these
tools:

```bash
docker run -it --rm -p 8088:8080 -e 'REPO=https://github.com/PaloAltoNetworks/SkilletBuilder.git' \
  -e 'BRANCH=develop' \ 
  --name "Skillet Builder" registry.gitlab.com/panw-gse/as/appetizer
```

## Usage in Panhandler

These tools require the latest Panhandler container, which can be found in the
[Panhandler Docs](https://panhandler.readthedocs.io/en/master/running.html#quick-start).


## Support Policy
The code and templates in the repo are released under an as-is, best effort,
support policy. These scripts should be seen as community supported and
Palo Alto Networks will contribute our expertise as and when possible.
We do not provide technical support or help in using or troubleshooting the
components of the project through our normal support options such as
Palo Alto Networks support teams, or ASC (Authorized Support Centers)
partners and backline support options. The underlying product used
(the VM-Series firewall) by the scripts or templates are still supported,
but the support is only for the product functionality and not for help in
deploying or using the template or script itself. Unless explicitly tagged,
all projects or work posted in our GitHub repository
(at https://github.com/PaloAltoNetworks) or sites other than our official
Downloads page on https://support.paloaltonetworks.com are provided under
the best effort policy.
