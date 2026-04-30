import customtkinter as ctk
import sys
import os
import subprocess
import shutil
import logging
from datetime import datetime
from core.workers import BackgroundWorker
from core.settings import AppSettings
from ui.tray import SystemTray, TRAY_AVAILABLE

# ========== ЛОГИРОВАНИЕ ==========
log_dir = os.path.expanduser("~/.netguardian_logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"netguardian_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class NetGuardianApp:
    def __init__(self):
        try:
            self.settings = AppSettings()
            from core.language import Language
            lang = Language()
            lang.set_language(self.settings.get_language())
            self.worker = BackgroundWorker()

            theme = self.settings.get("theme", "dark")
            ctk.set_appearance_mode(theme)
            ctk.set_default_color_theme("dark-blue")

            self.main_window = ctk.CTk()
            self.main_window.title("🛡️ NET GUARDIAN ULTIMATE")
            self.main_window.geometry("1300x850")
            self.main_window.minsize(1000, 700)

            self.tray = None
            if TRAY_AVAILABLE:
                self.tray = SystemTray(self)
                if self.tray.setup():
                    import threading
                    self.tray_thread = threading.Thread(target=self.tray.run, daemon=True)
                    self.tray_thread.start()

            self.init_ui()
            self.setup_hotkeys()

            # ПРАВИЛЬНЫЙ protocol
            self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)

            logger.info("Приложение успешно запущено")
        except Exception as e:
            logger.error(f"Ошибка при инициализации: {e}", exc_info=True)
            raise

    def setup_hotkeys(self):
        """Горячие клавиши"""
        try:
            self.main_window.bind('<Control-1>', lambda e: self.switch_page("speed"))
            self.main_window.bind('<Control-2>', lambda e: self.switch_page("control"))
            self.main_window.bind('<Control-3>', lambda e: self.switch_page("ports"))
            self.main_window.bind('<Control-4>', lambda e: self.switch_page("torrent"))
            self.main_window.bind('<Control-5>', lambda e: self.switch_page("stats"))
            self.main_window.bind('<Control-6>', lambda e: self.switch_page("settings"))
            self.main_window.bind('<Control-7>', lambda e: self.switch_page("system"))
            self.main_window.bind('<F5>', lambda e: self.restart_app())
            self.main_window.bind('<Escape>', lambda e: self.on_closing())
            logger.debug("Горячие клавиши установлены")
        except Exception as e:
            logger.error(f"Ошибка установки горячих клавиш: {e}")

    def init_ui(self):
        try:
            from ui.sidebar import Sidebar
            from ui.pages.speed_page import SpeedPage
            from ui.pages.control_page import ControlPage
            from ui.pages.ports_page import PortsPage
            from ui.pages.torrent_page import TorrentPage
            from ui.pages.stats_page import StatsPage
            from ui.pages.settings_page import SettingsPage
            from ui.pages.system_page import SystemPage

            self.main_window.grid_columnconfigure(1, weight=1)
            self.main_window.grid_rowconfigure(0, weight=1)

            self.sidebar = Sidebar(self.main_window, self.switch_page)
            self.sidebar.grid(row=0, column=0, sticky="nsew")

            self.content_frame = ctk.CTkFrame(self.main_window, fg_color="transparent")
            self.content_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure(0, weight=1)

            self.pages = {
                "speed": SpeedPage(self.content_frame, self),
                "control": ControlPage(self.content_frame, self),
                "ports": PortsPage(self.content_frame, self),
                "torrent": TorrentPage(self.content_frame, self),
                "stats": StatsPage(self.content_frame, self),
                "settings": SettingsPage(self.content_frame, self),
                "system": SystemPage(self.content_frame, self)
            }

            last_tab = self.settings.get("last_tab", "speed")
            self.switch_page(last_tab)
            logger.info("Интерфейс загружен")
        except Exception as e:
            logger.error(f"Ошибка загрузки интерфейса: {e}", exc_info=True)

    def switch_page(self, page_id):
        for page in self.pages.values():
            page.grid_forget()
        if page_id in self.pages:
            self.pages[page_id].grid(row=0, column=0, sticky="nsew")
            self.settings.set("last_tab", page_id)
            if hasattr(self, 'sidebar'):
                self.sidebar.set_active(page_id)
            # Обновляем язык на текущей странице
            if hasattr(self.pages[page_id], 'refresh_texts'):
                self.pages[page_id].refresh_texts()

    def restart_app(self):
        logger.info("Перезапуск приложения")
        self.main_window.destroy()
        os.system(f'"{sys.executable}" "{sys.argv[0]}"')
        sys.exit(0)

    def quit(self):
        logger.info("Завершение работы приложения")
        if hasattr(self, 'tray') and self.tray:
            self.tray.stop()
        self.worker.shutdown()
        self.main_window.quit()
        self.main_window.destroy()
        sys.exit(0)

    def run(self):
        try:
            self.main_window.mainloop()
        except Exception as e:
            logger.error(f"Ошибка в основном цикле: {e}", exc_info=True)

    def update_tray_speed(self, speed):
        """Обновление скорости в трее"""
        if hasattr(self, 'tray') and self.tray:
            self.tray.update_speed(speed)
    # ========== НОВЫЕ МЕТОДЫ ДЛЯ ОЧИСТКИ ==========

    def on_closing(self):
        """При закрытии окна - спрашиваем про очистку TEMP"""
        self.ask_cleanup_before_exit()

    def ask_cleanup_before_exit(self):
        """Красивый диалог перед выходом"""
        dialog = ctk.CTkToplevel(self.main_window)
        dialog.title("🧹 ОЧИСТКА СИСТЕМЫ")
        dialog.geometry("450x250")
        dialog.resizable(False, False)
        dialog.transient(self.main_window)
        dialog.grab_set()

        # Устанавливаем стиль
        dialog.configure(fg_color="#1a1a2a")

        # Центрируем
        dialog.update_idletasks()
        x = self.main_window.winfo_x() + (self.main_window.winfo_width() - 450) // 2
        y = self.main_window.winfo_y() + (self.main_window.winfo_height() - 250) // 2
        dialog.geometry(f"+{x}+{y}")

        # Иконка
        ctk.CTkLabel(dialog, text="🧹", font=ctk.CTkFont(size=48)).pack(pady=15)

        # Заголовок
        ctk.CTkLabel(dialog, text="ОЧИСТКА СИСТЕМЫ",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#ffaa00").pack()

        # Текст
        ctk.CTkLabel(dialog, text="Очистить временные файлы перед выходом?\n\n"
                                  "Это освободит место на диске и ускорит систему.",
                     font=ctk.CTkFont(size=12),
                     text_color="#888").pack(pady=15)

        # Кнопки
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        def cleanup_and_exit():
            dialog.destroy()
            self.clean_temp_files()
            self.quit()

        def just_exit():
            dialog.destroy()
            self.quit()

        # Стилизованные кнопки
        clean_btn = ctk.CTkButton(btn_frame, text="🧹 ДА, ОЧИСТИТЬ",
                                  fg_color="#2ecc71", hover_color="#27ae60",
                                  width=130, command=cleanup_and_exit)
        clean_btn.pack(side="left", padx=8)

        exit_btn = ctk.CTkButton(btn_frame, text="❌ НЕТ, ВЫЙТИ",
                                 fg_color="#e74c3c", hover_color="#c0392b",
                                 width=130, command=just_exit)
        exit_btn.pack(side="left", padx=8)

        cancel_btn = ctk.CTkButton(btn_frame, text="↩️ ОТМЕНА",
                                   fg_color="#2c3e66", hover_color="#1a2a3a",
                                   width=130, command=dialog.destroy)
        cancel_btn.pack(side="left", padx=8)

    def clean_temp_files(self):
        """Очистка временных файлов"""
        temp_paths = [
            os.environ.get('TEMP', ''),
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp')
        ]

        cleaned = 0
        freed = 0

        for temp_path in temp_paths:
            if temp_path and os.path.exists(temp_path):
                try:
                    for filename in os.listdir(temp_path):
                        file_path = os.path.join(temp_path, filename)
                        try:
                            if os.path.isfile(file_path):
                                freed += os.path.getsize(file_path)
                                os.remove(file_path)
                                cleaned += 1
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path, ignore_errors=True)
                                cleaned += 1
                        except:
                            pass
                except:
                    pass

        logger.info(f"Очистка TEMP: удалено {cleaned} файлов, освобождено {freed / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    try:
        app = NetGuardianApp()
        app.run()
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске: {e}", exc_info=True)
        input("Нажми Enter для выхода...")