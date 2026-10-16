# Security

The package reads local files and writes reports to stdout. It never uses a Home Assistant token, network API or actuator. Treat real input and reports as private: entity IDs, source identifiers and timestamps can still reveal household details.

Use the GitHub repository's private vulnerability reporting when enabled. If unavailable, open an issue containing only a request for a private reporting channel, not vulnerability details or secrets. Do not attach real exports to public issues.

The v0.1 line receives security fixes on its newest patch release. Reports should include version, minimal synthetic reproducer and impact. Input is size/depth/node bounded; YAML aliases, anchors, explicit tags and duplicate keys are rejected. Unknown contract fields are rejected. Raw parser exception text and unreadable file paths are not echoed in CLI errors.

A valid report does not certify electrical safety, counter accuracy or safe automation policy. Source timestamps and physical declarations remain trusted operator input. Do not use this software as the only protection for pumps, valves, charging equipment or other loads.


## Private reports and handling

Use [the private vulnerability form](https://github.com/ha-homelab/ha-meter-contracts/security/advisories/new)
or email **alvit.work@gmail.com**. Include the affected revision, impact and a
minimal synthetic reproduction. Never send live credentials or household data.
The latest source on the 0.1 maintenance line receives fixes; update to the latest
reviewed revision before filing a report when possible.

The maintainer aims to acknowledge reports within 14 days, assess severity and
reproduce them privately, agree on disclosure timing with the reporter, and test
the fix before release. Confirmed critical issues are addressed immediately;
other medium-or-higher issues should be fixed within 60 days. Release notes list
available CVE/GHSA identifiers and upgrade instructions. Reporters receive credit
unless they request anonymity. If the first contact receives no response, retry
the other private channel. There is currently no independent security team or
backup maintainer; [governance](GOVERNANCE.md) records that limitation.
