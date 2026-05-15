# Security Policy

NetGuardian can perform Windows system-level actions, so users should understand what it changes before running it as administrator.

## System-Level Features

The following features may require administrator rights:

- Windows Firewall port rules;
- QoS policies for torrent upload limiting;
- service changes in turbo optimization;
- system temporary folder cleanup;
- process termination.

## Reporting Issues

If you find a bug, unsafe behavior, or suspicious command execution, open a GitHub issue and include:

- Windows version;
- NetGuardian version or commit hash;
- exact action that caused the issue;
- relevant log file from `%USERPROFILE%\.netguardian_logs\`.

## Trust Notes

Users should prefer releases built from public source code. For public downloads, attach hashes and a VirusTotal link when possible.
