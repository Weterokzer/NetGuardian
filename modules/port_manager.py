from utils.system_ops import run_command


class PortManager:
    """Управление портами через Windows Firewall"""

    def __init__(self):
        self.opened_ports = []
        self.cache = {}
        self.cache_time = 0

    def open_port(self, port, protocol="TCP"):
        try:
            result = run_command([
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name=NG_Port_{port}", "dir=in", "action=allow",
                f"protocol={protocol}", f"localport={port}",
            ], timeout=8, admin_required=True)
            if result.ok:
                if port not in self.opened_ports:
                    self.opened_ports.append(port)
                self.cache = {}
                return True, f"Порт {port}/{protocol} открыт"
            return False, result.message
        except Exception as e:
            return False, str(e)

    def close_port(self, port):
        try:
            result = run_command([
                "netsh", "advfirewall", "firewall", "delete", "rule",
                f"name=NG_Port_{port}",
            ], timeout=8, admin_required=True)
            if not result.ok:
                return False, result.message
            if port in self.opened_ports:
                self.opened_ports.remove(port)
            self.cache = {}
            return True, f"Порт {port} закрыт"
        except Exception as e:
            return False, str(e)

    def list_rules(self):
        """Кэшированный список правил"""
        import time
        current_time = time.time()
        if current_time - self.cache_time < 2:
            return self.cache.get('rules', "Нет активных правил")

        try:
            result = run_command([
                "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
                "netsh advfirewall firewall show rule name=all dir=in | Select-String NG_Port | ForEach-Object { $_.Line }",
            ], timeout=8)
            rules = result.stdout if result.stdout else "Нет активных правил"
            self.cache['rules'] = rules
            self.cache_time = current_time
            return rules
        except Exception:
            return "Ошибка получения правил"

    def is_port_open(self, port):
        """Проверка открыт ли порт"""
        return port in self.opened_ports
