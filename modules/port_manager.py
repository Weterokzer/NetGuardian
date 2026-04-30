import subprocess


class PortManager:
    """Управление портами через Windows Firewall"""

    def __init__(self):
        self.opened_ports = []
        self.cache = {}
        self.cache_time = 0

    def open_port(self, port, protocol="TCP"):
        try:
            cmd = f'netsh advfirewall firewall add rule name="NG_Port_{port}" dir=in action=allow protocol={protocol} localport={port}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            if "ОК" in result.stdout or "OK" in result.stdout:
                if port not in self.opened_ports:
                    self.opened_ports.append(port)
                self.cache = {}
                return True, f"Порт {port}/{protocol} открыт"
            return False, result.stdout
        except Exception as e:
            return False, str(e)

    def close_port(self, port):
        try:
            cmd = f'netsh advfirewall firewall delete rule name="NG_Port_{port}"'
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
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
            cmd = 'netsh advfirewall firewall show rule name=all dir=in | findstr "NG_Port"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            rules = result.stdout if result.stdout else "Нет активных правил"
            self.cache['rules'] = rules
            self.cache_time = current_time
            return rules
        except:
            return "Ошибка получения правил"

    def is_port_open(self, port):
        """Проверка открыт ли порт"""
        return port in self.opened_ports