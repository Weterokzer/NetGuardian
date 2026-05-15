from utils.system_ops import run_command


class TorrentProtect:
    """Защита торрент-трафика через QoS"""

    def __init__(self):
        self.current_limit = 0
        self.policy_name = "NG_Limit"

    def set_limit(self, speed_kbps):
        """Установка ограничения скорости"""
        try:
            if speed_kbps > 0:
                # Удаляем старое правило
                self.remove_limit()
                # Создаём новое
                result = run_command([
                    "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                    f"New-NetQosPolicy -Name '{self.policy_name}' -ThrottleRateMbps {speed_kbps / 1000} -NetworkProfile All -ErrorAction Stop",
                ], timeout=8, admin_required=True)
                if not result.ok:
                    return False, result.message
                self.current_limit = speed_kbps
                return True, speed_kbps
            else:
                if self.remove_limit():
                    return True, 0
                return False, "Не удалось отключить лимит"
        except Exception as e:
            return False, str(e)

    def remove_limit(self):
        """Удаление ограничения"""
        try:
            result = run_command([
                "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                f"Get-NetQosPolicy -Name '{self.policy_name}' -ErrorAction SilentlyContinue | Remove-NetQosPolicy -Confirm:$false -ErrorAction Stop",
            ], timeout=8, admin_required=True)
            if not result.ok:
                return False
            self.current_limit = 0
            return True
        except Exception:
            return False

    def get_current_limit(self):
        """Получение текущего лимита"""
        return self.current_limit

    def get_mode_name(self):
        """Название режима по скорости"""
        modes = {
            0: "Выключено",
            1: "Инкогнито",
            50: "Ночной",
            200: "Тихий",
            500: "Баланс"
        }
        return modes.get(self.current_limit, f"Кастомный ({self.current_limit} Kbps)")
