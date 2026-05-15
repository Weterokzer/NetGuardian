import subprocess
import os
import sys
import winreg


class SystemHelper:
    """Системные утилиты"""

    @staticmethod
    def add_to_startup():
        """Добавление в автозагрузку"""
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "net_guardian.py"))
        if getattr(sys, "frozen", False):
            command = f'"{sys.executable}"'
        else:
            python_path = sys.executable
            if os.path.basename(python_path).lower() == "python.exe":
                pythonw_path = os.path.join(os.path.dirname(python_path), "pythonw.exe")
                if os.path.exists(pythonw_path):
                    python_path = pythonw_path
            command = f'"{python_path}" "{script_path}"'

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                            winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "NetGuardian", 0, winreg.REG_SZ, command)

    @staticmethod
    def remove_from_startup():
        """Удаление из автозагрузки"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0,
                                winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, "NetGuardian")
        except FileNotFoundError:
            pass

    @staticmethod
    def is_in_startup():
        """Проверка в автозагрузке"""
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run") as key:
                winreg.QueryValueEx(key, "NetGuardian")
                return True
        except FileNotFoundError:
            return False

    @staticmethod
    def restart_as_admin():
        """Перезапуск с правами администратора"""
        if sys.platform == 'win32':
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(0)
