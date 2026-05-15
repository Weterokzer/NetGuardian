# NetGuardian Ultimate

NetGuardian Ultimate is a Windows desktop utility for network monitoring, speed testing, firewall port rules, torrent upload limiting, process control, and basic system maintenance.

The project is written in Python with CustomTkinter and is focused on a simple, dark, all-in-one control panel for everyday Windows users.

![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4?logo=windows)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-20c997)

## Features

- Realtime network speed monitor.
- Speedtest with saved JSON history.
- Download and upload charts.
- Process list with search, pagination, memory and CPU usage.
- Safer process termination with protected system processes.
- Windows Firewall port rule management.
- Torrent upload limiting through Windows QoS policies.
- Startup app viewer.
- Local network scanner.
- TEMP cleanup with safer skipping of fresh files.
- System info, battery, disk usage and temperature panels.
- Dark UI with tray support.
- Russian and English language options.

## Screenshots

Screenshots will be added in the next release. Recommended views:

- Speedometer
- Process control
- Ports
- Torrent protection
- Statistics
- Settings
- System utilities

## Important Safety Notes

Some features change Windows system settings:

- opening or deleting firewall rules;
- creating or removing QoS policies;
- stopping services in turbo optimization;
- terminating processes;
- cleaning temporary files.

Run the app as administrator only when you need these system-level actions. The app should show a clear error when administrator rights are required.

## Installation From Source

```bash
git clone https://github.com/Weterokzer/NetGuardian.git
cd NetGuardian
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python net_guardian.py
```

## Build EXE

PyInstaller is used for the Windows build.

```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller NetGuardian.spec --noconfirm
```

The compiled app will appear here:

```text
dist/NetGuardian.exe
```

For GitHub, upload the `.exe` through **Releases**, not directly into the source tree.

## Logs And Local Data

NetGuardian stores local user data outside the repository:

```text
%USERPROFILE%\.netguardian_logs\
%USERPROFILE%\.netguardian_settings.json
%USERPROFILE%\.netguardian_history.json
```

## Hotkeys

| Hotkey | Action |
|---|---|
| `Ctrl+1` | Speedometer |
| `Ctrl+2` | Process control |
| `Ctrl+3` | Ports |
| `Ctrl+4` | Torrent protection |
| `Ctrl+5` | Statistics |
| `Ctrl+6` | Settings |
| `Ctrl+7` | System utilities |
| `F5` | Restart app |
| `Esc` | Exit |

## Project Status

This is an active personal project. It is usable, but some Windows system features may behave differently depending on permissions, Windows edition, antivirus settings, and installed network components.

## License

MIT License. See [LICENSE](LICENSE).
