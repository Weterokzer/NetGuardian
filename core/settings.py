import json
import os
import atexit


class AppSettings:
    """Синглтон для настроек с автосохранением"""
    _instance = None
    _defaults = {
        "theme": "dark",
        "auto_start": False,
        "minimize_to_tray": True,
        "show_speed_in_tray": True,
        "monitoring_interval": 500,
        "processes_refresh_interval": 2000,
        "language": "ru",
        "last_tab": "speed"
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        self.config_file = os.path.expanduser("~/.netguardian_settings.json")
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = self._defaults.copy()
        else:
            self.data = self._defaults.copy()
        atexit.register(self.save)

    def save(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except:
            pass

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def get_language(self):
        return self.get("language", "ru")

    def set_language(self, lang):
        self.set("language", lang)