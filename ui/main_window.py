import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.pages.speed_page import SpeedPage
from ui.pages.control_page import ControlPage
from ui.pages.ports_page import PortsPage
from ui.pages.torrent_page import TorrentPage
from ui.pages.stats_page import StatsPage
from ui.pages.settings_page import SettingsPage


class MainWindow(ctk.CTk):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("🛡️ NET GUARDIAN ULTIMATE v3.0")
        self.geometry("1400x900")
        self.minsize(1200, 700)

        # Настройка сетки
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Создаём сайдбар
        self.sidebar = Sidebar(self, self.switch_page)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Контентная область
        self.content_frame = ctk.CTkFrame(self, fg_color="#0a0a0f")
        self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        # Страницы
        self.pages = {
            "speed": SpeedPage(self.content_frame, self.app),
            "control": ControlPage(self.content_frame, self.app),
            "ports": PortsPage(self.content_frame, self.app),
            "torrent": TorrentPage(self.content_frame, self.app),
            "stats": StatsPage(self.content_frame, self.app),
            "settings": SettingsPage(self.content_frame, self.app)
        }

        # Показываем последнюю активную страницу
        last_tab = self.app.settings.get("last_tab", "speed")
        self.switch_page(last_tab)

        # При закрытии окна
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def switch_page(self, page_id):
        for page in self.pages.values():
            page.grid_forget()
        self.pages[page_id].grid(row=0, column=0, sticky="nsew")
        self.app.settings.set("last_tab", page_id)
        # Обновляем активную кнопку в сайдбаре
        self.sidebar.set_active(page_id)

    def on_closing(self):
        if self.app.settings.get("minimize_to_tray", True) and TRAY_AVAILABLE:
            self.withdraw()  # Сворачиваем в трей
        else:
            self.app.quit()