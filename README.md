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

- <img width="1302" height="892" alt="image" src="https://github.com/user-attachments/assets/5e8ca67f-d6c8-4da9-a5be-ea1a5bbbd4b1" />

- <img width="1295" height="883" alt="image" src="https://github.com/user-attachments/assets/e835bd29-5e6c-4f26-9400-9dfd094709f7" />

- <img width="1301" height="878" alt="image" src="https://github.com/user-attachments/assets/a57cd53e-34f3-4173-afad-299c38c28d6e" />

- <img width="1295" height="875" alt="image" src="https://github.com/user-attachments/assets/9c163d9e-95db-4eb0-81fa-707116188dad" />

- <img width="1291" height="877" alt="image" src="https://github.com/user-attachments/assets/3d2bd4fa-6829-460e-b329-6e823c88618e" />

- <img width="1293" height="873" alt="image" src="https://github.com/user-attachments/assets/651a521d-ad70-46a1-8275-2be8b3cf38d7" />

- <img width="1293" height="884" alt="image" src="https://github.com/user-attachments/assets/369dff9d-f8a6-496a-b403-0c26d9b708cf" />

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
