# 12-12-19 nembery@paloaltonetworks.com
import json
import os
import sys

from skilletlib import Panoply

# grab our two configs from the environment
base_config_path = os.environ.get("BASE_CONFIG", "")
latest_config_path = os.environ.get("LATEST_CONFIG", "")

with open(base_config_path, "r") as bcf:
    base_config = bcf.read()

with open(latest_config_path, "r") as lcf:
    latest_config = lcf.read()

# init the Panoply helper class, note we do not need connection information, as we only need offline mode
# to compare two configurations
p = Panoply()

# insert magic here
snippets = p.generate_skillet_from_configs(base_config, latest_config)

# check we actually have some diffs
if len(snippets) == 0:
    print(f"No changes found between {base_config} and {latest_config}")
    sys.exit(2)

# dump out our diffs here. Note, we will use output capturing in the skillet to capture this
print(json.dumps(snippets, indent=2))

# later gator
sys.exit(0)
