"""Многоязычная поддержка"""

TRANSLATIONS = {
    "ru": {
        # Общее
        "app_title": "NET GUARDIAN ULTIMATE",

        # Сайдбар
        "menu_speed": "СПИДОМЕТР",
        "menu_control": "КОНТРОЛЬ",
        "menu_ports": "ПОРТЫ",
        "menu_torrent": "ТОРРЕНТЫ",
        "menu_stats": "СТАТИСТИКА",
        "menu_settings": "НАСТРОЙКИ",
        "menu_system": "СИСТЕМА",

        # Настройки
        "settings_title": "НАСТРОЙКИ",
        "settings_general": "ОСНОВНЫЕ НАСТРОЙКИ",
        "settings_autostart": "Автозапуск с Windows",
        "settings_minimize_tray": "Сворачивать в системный трей",
        "settings_language": "ЯЗЫК / LANGUAGE",
        "settings_theme": "ОФОРМЛЕНИЕ",
        "settings_theme_dark": "Тёмная",
        "settings_theme_light": "Светлая",
        "settings_restart_warning": "⚠️ ДЛЯ ПРИМЕНЕНИЯ ТЕМЫ ТРЕБУЕТСЯ ПЕРЕЗАПУСК",
        "settings_about": "О ПРОГРАММЕ",
        "settings_reset": "СБРОСИТЬ ВСЕ НАСТРОЙКИ",

        # Система
        "system_title": "СИСТЕМНЫЕ УТИЛИТЫ",
        "system_clean": "ОЧИСТКА СИСТЕМЫ",
        "system_clean_temp": "Очистить временные файлы",
        "system_disk": "АНАЛИЗ ДИСКА",
        "system_disk_button": "Найти большие файлы",
        "system_turbo": "ТУРБО-ОПТИМИЗАЦИЯ",
        "system_turbo_button": "Применить оптимизации",
        "system_startup": "АВТОЗАГРУЗКА",
        "system_startup_button": "Показать программы",
        "system_battery": "АККУМУЛЯТОР",
        "system_temperature": "ТЕМПЕРАТУРА",
        "system_info": "СИСТЕМНАЯ ИНФОРМАЦИЯ",
        "system_network_scan": "СЕТЕВОЙ СКАНЕР",
        "system_network_scan_button": "Сканировать сеть",

        # Контроль процессов
        "control_title": "УПРАВЛЕНИЕ ПРОЦЕССАМИ",
        "control_search": "Поиск процесса...",
        "control_total": "Всего процессов",
        "control_system": "Система",
        "control_page": "Страница",
        "control_of": "из",
        "control_showing": "Показано",
        "control_loading": "Загрузка процессов...",
        "control_not_found": "Ничего не найдено",
        "control_kill_confirm": "Завершить процесс?",
        "control_kill_warning": "Это действие необратимо!",
        "control_yes": "ЗАВЕРШИТЬ",
        "control_no": "ОТМЕНА",

        # Speedtest
        "speed_title": "СПИДОМЕТР",
        "speed_mbps": "Mbps",
        "speed_test_button": "ЗАПУСТИТЬ SPEEDTEST",
        "speed_testing": "ТЕСТИРУЕМ...",
        "speed_download": "Загрузка",
        "speed_upload": "Отдача",

        # Порты
        "ports_title": "УПРАВЛЕНИЕ ПОРТАМИ",
        "ports_port": "ПОРТ",
        "ports_protocol": "ПРОТОКОЛ",
        "ports_open": "ОТКРЫТЬ",
        "ports_close": "ЗАКРЫТЬ",
        "ports_rules": "АКТИВНЫЕ ПРАВИЛА",
        "ports_refresh": "ОБНОВИТЬ",

        # Торренты
        "torrent_title": "ЗАЩИТА ТОРРЕНТОВ",
        "torrent_desc": "Ограничение исходящего трафика",
        "torrent_modes": "БЫСТРЫЕ РЕЖИМЫ",
        "torrent_incognito": "ИНКОГНИТО",
        "torrent_night": "НОЧНОЙ",
        "torrent_quiet": "ТИХИЙ",
        "torrent_balance": "БАЛАНС",
        "torrent_stop": "STOP",
        "torrent_no_limit": "Нет ограничений",

        # Сообщения
        "msg_clean_complete": "Очистка завершена",
        "msg_limit_set": "Лимит установлен",
        "msg_limit_off": "Лимит отключён",
        "msg_process_killed": "завершён",
        "msg_error": "Ошибка",
        "yes": "ДА",
        "no": "НЕТ",
        "cancel": "ОТМЕНА",
        "close": "ЗАКРЫТЬ",
        "refresh": "ОБНОВИТЬ",
        "scan": "СКАНИРОВАТЬ",
        "scanning": "СКАНИРОВАНИЕ",
        "ready": "ГОТОВ",

        # Системная страница
        "system_clean_title": "🧹 ОЧИСТКА СИСТЕМЫ",
        "system_clean_button": "Очистить временные файлы",
        "system_disk_title": "📀 АНАЛИЗ ДИСКА",
        "system_turbo_title": "⚡ ТУРБО-ОПТИМИЗАЦИЯ",
        "system_startup_title": "🚀 АВТОЗАГРУЗКА",
        "system_network_title": "🌐 NET GUARDIAN SCAN",
        "system_network_button": "Сканировать сеть",
        "system_battery_title": "🔋 АККУМУЛЯТОР",
        "system_temperature_title": "🌡️ ТЕМПЕРАТУРА",
        "system_info_title": "💻 СИСТЕМНАЯ ИНФОРМАЦИЯ",
        "system_battery_charging": "Заряжается",
        "system_battery_discharging": "Разряжается",
        "system_battery_not_found": "Аккумулятор не обнаружен",
        "system_temp_not_found": "Датчики не найдены",
        "system_temp_loading": "Загрузка...",
        "system_clean_status": "Очистка...",
        "system_clean_done": "Удалено: {files} файлов, освобождено: {size} MB",
        "system_optimization_applying": "Применение оптимизаций...",
        "system_optimization_done": "Оптимизация завершена!",
        "system_analyzing": "Анализ диска...",
        "system_top_files": "ТОП-20 САМЫХ БОЛЬШИХ ФАЙЛОВ:",
    },

    "en": {
        # General
        "app_title": "NET GUARDIAN ULTIMATE",

        # Sidebar
        "menu_speed": "SPEEDOMETER",
        "menu_control": "CONTROL",
        "menu_ports": "PORTS",
        "menu_torrent": "TORRENT",
        "menu_stats": "STATISTICS",
        "menu_settings": "SETTINGS",
        "menu_system": "SYSTEM",

        # Settings
        "settings_title": "SETTINGS",
        "settings_general": "GENERAL SETTINGS",
        "settings_autostart": "Auto start with Windows",
        "settings_minimize_tray": "Minimize to system tray",
        "settings_language": "LANGUAGE",
        "settings_theme": "APPEARANCE",
        "settings_theme_dark": "Dark",
        "settings_theme_light": "Light",
        "settings_restart_warning": "⚠️ RESTART REQUIRED TO APPLY THEME",
        "settings_about": "ABOUT",
        "settings_reset": "RESET ALL SETTINGS",

        # System
        "system_title": "SYSTEM UTILITIES",
        "system_clean": "SYSTEM CLEANUP",
        "system_clean_temp": "Clean temporary files",
        "system_disk": "DISK ANALYZER",
        "system_disk_button": "Find large files",
        "system_turbo": "TURBO OPTIMIZATION",
        "system_turbo_button": "Apply optimizations",
        "system_startup": "STARTUP",
        "system_startup_button": "Show startup programs",
        "system_battery": "BATTERY",
        "system_temperature": "TEMPERATURE",
        "system_info": "SYSTEM INFORMATION",
        "system_network_scan": "NETWORK SCANNER",
        "system_network_scan_button": "Scan network",

        # Process Control
        "control_title": "PROCESS CONTROL",
        "control_search": "Search process...",
        "control_total": "Total processes",
        "control_system": "System",
        "control_page": "Page",
        "control_of": "of",
        "control_showing": "Showing",
        "control_loading": "Loading processes...",
        "control_not_found": "Nothing found",
        "control_kill_confirm": "Kill process?",
        "control_kill_warning": "This action is irreversible!",
        "control_yes": "KILL",
        "control_no": "CANCEL",

        # Speedtest
        "speed_title": "SPEEDOMETER",
        "speed_mbps": "Mbps",
        "speed_test_button": "RUN SPEEDTEST",
        "speed_testing": "TESTING...",
        "speed_download": "Download",
        "speed_upload": "Upload",

        # Ports
        "ports_title": "PORT MANAGEMENT",
        "ports_port": "PORT",
        "ports_protocol": "PROTOCOL",
        "ports_open": "OPEN",
        "ports_close": "CLOSE",
        "ports_rules": "ACTIVE RULES",
        "ports_refresh": "REFRESH",

        # Torrent
        "torrent_title": "TORRENT PROTECTION",
        "torrent_desc": "Limit outgoing traffic",
        "torrent_modes": "QUICK MODES",
        "torrent_incognito": "INCOGNITO",
        "torrent_night": "NIGHT",
        "torrent_quiet": "QUIET",
        "torrent_balance": "BALANCE",
        "torrent_stop": "STOP",
        "torrent_no_limit": "No limits",

        # Messages
        "msg_clean_complete": "Cleanup completed",
        "msg_limit_set": "Limit set",
        "msg_limit_off": "Limit disabled",
        "msg_process_killed": "killed",
        "msg_error": "Error",
        "yes": "YES",
        "no": "NO",
        "cancel": "CANCEL",
        "close": "CLOSE",
        "refresh": "REFRESH",
        "scan": "SCAN",
        "scanning": "SCANNING",
        "ready": "READY",

        "system_clean_title": "🧹 SYSTEM CLEANUP",
        "system_clean_button": "Clean temporary files",
        "system_disk_title": "📀 DISK ANALYZER",
        "system_turbo_title": "⚡ TURBO OPTIMIZATION",
        "system_startup_title": "🚀 STARTUP",
        "system_network_title": "🌐 NET GUARDIAN SCAN",
        "system_network_button": "Scan network",
        "system_battery_title": "🔋 BATTERY",
        "system_temperature_title": "🌡️ TEMPERATURE",
        "system_info_title": "💻 SYSTEM INFORMATION",
        "system_battery_charging": "Charging",
        "system_battery_discharging": "Discharging",
        "system_battery_not_found": "Battery not found",
        "system_temp_not_found": "Sensors not found",
        "system_temp_loading": "Loading...",
        "system_clean_status": "Cleaning...",
        "system_clean_done": "Deleted: {files} files, freed: {size} MB",
        "system_optimization_applying": "Applying optimizations...",
        "system_optimization_done": "Optimization completed!",
        "system_analyzing": "Analyzing disk...",
        "system_top_files": "TOP-20 LARGEST FILES:",
    }
}

class Language:
    _instance = None
    _current_lang = "ru"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_language(cls, lang):
        cls._current_lang = lang

    @classmethod
    def get(cls, key):
        return TRANSLATIONS.get(cls._current_lang, TRANSLATIONS["ru"]).get(key, key)

    @classmethod
    def get_lang(cls):
        return cls._current_lang