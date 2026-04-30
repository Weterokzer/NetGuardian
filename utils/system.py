import subprocess
import os
import sys


class SystemHelper:
    """Системные утилиты"""

    @staticmethod
    def add_to_startup():
        """Добавление в автозагрузку"""
        script_path = os.path.abspath("net_guardian.py")
        python_path = sys.executable
        cmd = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v NetGuardian /t REG_SZ /d "{python_path} {script_path}" /f'
        subprocess.run(cmd, shell=True, capture_output=True)

    @staticmethod
    def remove_from_startup():
        """Удаление из автозагрузки"""
        cmd = 'reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v NetGuardian /f'
        subprocess.run(cmd, shell=True, capture_output=True)

    @staticmethod
    def is_in_startup():
        """Проверка в автозагрузке"""
        try:
            cmd = 'reg query HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v NetGuardian'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return "NetGuardian" in result.stdout
        except:
            return False

    @staticmethod
    def restart_as_admin():
        """Перезапуск с правами администратора"""
        if sys.platform == 'win32':
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(0)