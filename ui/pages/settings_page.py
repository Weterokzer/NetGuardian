import customtkinter as ctk
import subprocess
import os
import sys
import webbrowser
from core.settings import AppSettings
from core.language import Language
from utils.system import SystemHelper


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.settings = AppSettings()
        self.lang = Language()
        self.pending_restart = False
        self.pending_lang = None
        self.pending_theme = None
        self.create_widgets()
        self.load_settings()

    def create_widgets(self):
        # Заголовок
        header = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(header, text="⚙️", font=ctk.CTkFont(size=38)).pack(pady=(15, 5))
        ctk.CTkLabel(header, text="NET GUARDIAN",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#00d4ff").pack()
        ctk.CTkLabel(header, text="SETTINGS",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#666").pack(pady=(0, 15))

        self.summary_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1a2a")
        self.summary_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.startup_status = self._create_summary_card(
            self.summary_frame, "АВТОЗАПУСК", "Проверка...", "#00d4ff"
        )
        self.tray_status = self._create_summary_card(
            self.summary_frame, "ТРЕЙ", "Проверка...", "#00ff88"
        )
        self.theme_status = self._create_summary_card(
            self.summary_frame, "ТЕМА", "Проверка...", "#ffaa00"
        )

        # Основные настройки
        general_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        general_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(general_frame, text="ОСНОВНЫЕ НАСТРОЙКИ",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#00d4ff").pack(pady=10, anchor="w", padx=20)

        self.auto_start_var = ctk.BooleanVar()
        self.auto_start_switch = ctk.CTkSwitch(general_frame, text="Автозапуск с Windows",
                                               variable=self.auto_start_var, command=self.toggle_auto_start)
        self.auto_start_switch.pack(pady=8, anchor="w", padx=40)

        self.minimize_tray_var = ctk.BooleanVar()
        self.minimize_tray_switch = ctk.CTkSwitch(general_frame, text="Сворачивать в системный трей",
                                                  variable=self.minimize_tray_var, command=self.toggle_minimize_tray)
        self.minimize_tray_switch.pack(pady=8, anchor="w", padx=40)

        # Язык
        lang_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        lang_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(lang_frame, text="ЯЗЫК / LANGUAGE",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#00d4ff").pack(pady=10, anchor="w", padx=20)

        self.lang_var = ctk.StringVar(value="🇷🇺 Русский")
        lang_options = ctk.CTkOptionMenu(lang_frame, values=["🇷🇺 Русский", "🇬🇧 English"],
                                         variable=self.lang_var,
                                         command=self.on_language_change,
                                         width=150)
        lang_options.pack(pady=8, anchor="w", padx=40)

        # Тема
        theme_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        theme_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(theme_frame, text="ОФОРМЛЕНИЕ",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#00d4ff").pack(pady=10, anchor="w", padx=20)

        ctk.CTkLabel(theme_frame, text="Выберите тему:", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=40)

        self.theme_var = ctk.StringVar(value="dark")
        theme_options = ctk.CTkOptionMenu(theme_frame, values=["🌙 Тёмная", "☀️ Светлая"],
                                          variable=self.theme_var,
                                          command=self.on_theme_change,
                                          width=150)
        theme_options.pack(pady=8, anchor="w", padx=40)

        # Поддержка проекта
        support_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        support_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(support_frame, text="☕ ПОДДЕРЖАТЬ ПРОЕКТ",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#ffaa00").pack(pady=10, anchor="w", padx=20)

        ctk.CTkLabel(support_frame,
                     text="Если вам нравится NetGuardian, вы можете поддержать разработку!",
                     font=ctk.CTkFont(size=11), text_color="#888").pack(anchor="w", padx=40)

        # Кнопки поддержки
        support_row = ctk.CTkFrame(support_frame, fg_color="transparent")
        support_row.pack(pady=10)

        def open_tipee():
            webbrowser.open("https://www.tipeeestream.com/net-guardian-ultimate/donation")

        def open_github():
            webbrowser.open("https://github.com/Weterokzer/NetGuardian")

        # Кнопка TipeeeStream
        tipee_btn = ctk.CTkButton(support_row, text="💝 TipeeeStream",
                                  fg_color="#e74c3c", hover_color="#c0392b",
                                  width=140, command=open_tipee)
        tipee_btn.pack(side="left", padx=5)

        # Кнопка GitHub
        github_btn = ctk.CTkButton(support_row, text="⭐ GitHub",
                                   fg_color="#333", hover_color="#555",
                                   width=100, command=open_github)
        github_btn.pack(side="left", padx=5)

        # Подсказки
        from utils.simple_tooltip import add_tooltip
        add_tooltip(tipee_btn, "Поддержать через TipeeeStream")
        add_tooltip(github_btn, "Поставить звезду на GitHub")

        # О программе
        self.about_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        self.about_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(self.about_frame, text="📖 О ПРОГРАММЕ",
                     font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#00d4ff").pack(pady=10, anchor="w", padx=20)

        about_text = """NET GUARDIAN ULTIMATE v4.0
ПРОФЕССИОНАЛЬНЫЙ ИНСТРУМЕНТ ДЛЯ МОНИТОРИНГА СЕТИ

✨ ОСОБЕННОСТИ:
• МОНИТОРИНГ СКОРОСТИ В РЕАЛЬНОМ ВРЕМЕНИ
• SPEEDTEST С ИСТОРИЕЙ РЕЗУЛЬТАТОВ
• УПРАВЛЕНИЕ ПРОЦЕССАМИ
• КОНТРОЛЬ ПОРТОВ БРАНДМАУЭРА
• ЗАЩИТА ТОРРЕНТ-ТРАФИКА

⚡ СОЗДАНО С ПОДДЕРЖКОЙ БЕЗ СНА И БУЛКА С ЧАЕМ"""

        ctk.CTkLabel(self.about_frame, text=about_text,
                     font=ctk.CTkFont(size=11),
                     justify="left",
                     text_color="#888").pack(pady=10, anchor="w", padx=40)

        reset_btn = ctk.CTkButton(self.about_frame, text="🔄 СБРОСИТЬ ВСЕ НАСТРОЙКИ",
                                  fg_color="#e74c3c", hover_color="#c0392b",
                                  command=self.reset_settings)
        reset_btn.pack(pady=15)

        # Панель для сообщения о pending restart
        self.restart_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#d35400")
        self.restart_label = ctk.CTkLabel(self.restart_frame, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.restart_label.pack(pady=8)
        self.restart_btn = ctk.CTkButton(self.restart_frame, text="🔄 ПЕРЕЗАПУСТИТЬ СЕЙЧАС",
                                         fg_color="#2ecc71", command=self.execute_restart)
        self.restart_btn.pack(pady=5)

    def _create_summary_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color="#0f0f1a")
        card.pack(side="left", fill="x", expand=True, padx=8, pady=10)

        ctk.CTkLabel(card, text=title,
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color="#8a95a8").pack(anchor="w", padx=14, pady=(10, 0))
        value_label = ctk.CTkLabel(card, text=value,
                                   font=ctk.CTkFont(size=14, weight="bold"),
                                   text_color=color)
        value_label.pack(anchor="w", padx=14, pady=(2, 10))
        return value_label

    def update_summary(self):
        startup = "Включён" if self.auto_start_var.get() else "Выключен"
        tray = "Включён" if self.minimize_tray_var.get() else "Выключен"
        theme = "Тёмная" if self.settings.get("theme", "dark") == "dark" else "Светлая"

        self.startup_status.configure(text=startup, text_color="#00ff88" if self.auto_start_var.get() else "#8a95a8")
        self.tray_status.configure(text=tray, text_color="#00ff88" if self.minimize_tray_var.get() else "#8a95a8")
        self.theme_status.configure(text=theme)

    def load_settings(self):
        real_auto_start = SystemHelper.is_in_startup()
        self.auto_start_var.set(real_auto_start)
        self.settings.set("auto_start", real_auto_start)
        self.minimize_tray_var.set(self.settings.get("minimize_to_tray", True))
        theme = self.settings.get("theme", "dark")
        self.theme_var.set("🌙 Тёмная" if theme == "dark" else "☀️ Светлая")
        lang = self.settings.get_language()
        self.lang_var.set("🇷🇺 Русский" if lang == "ru" else "🇬🇧 English")
        self.update_summary()

    def on_language_change(self, choice):
        new_lang = "ru" if "Русский" in choice else "en"
        self.settings.set_language(new_lang)
        self.pending_lang = choice
        self.pending_restart = True
        self.show_restart_panel()

    def on_theme_change(self, choice):
        new_theme = "dark" if "Тёмная" in choice else "light"
        self.settings.set("theme", new_theme)
        self.pending_theme = choice
        self.pending_restart = True
        self.update_summary()
        self.show_restart_panel()

    def show_restart_panel(self):
        changes = []
        if self.pending_lang:
            changes.append(f"язык → {self.pending_lang}")
        if self.pending_theme:
            changes.append(f"тему → {self.pending_theme}")

        if changes:
            text = f"✅ Изменения сохранены: {', '.join(changes)}\n⚠️ Для применения изменений требуется перезапуск!"
            self.restart_label.configure(text=text, text_color="#ffffff")
            self.restart_frame.pack(fill="x", padx=20, pady=10)
            self.restart_frame.pack_forget()
            self.restart_frame.pack(fill="x", padx=20, pady=10, before=self.about_frame)

    def execute_restart(self):
        self.app.restart_app()

    def toggle_auto_start(self):
        enabled = self.auto_start_var.get()
        try:
            if enabled:
                SystemHelper.add_to_startup()
                self.show_message("✅ Автозагрузка включена")
            else:
                SystemHelper.remove_from_startup()
                self.show_message("✅ Автозагрузка отключена")
            self.settings.set("auto_start", enabled)
            self.update_summary()
        except Exception as exc:
            self.auto_start_var.set(not enabled)
            self.update_summary()
            self.show_message(f"❌ Автозагрузка: {str(exc)[:80]}")

    def toggle_minimize_tray(self):
        self.settings.set("minimize_to_tray", self.minimize_tray_var.get())
        self.update_summary()

    def reset_settings(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("ПОДТВЕРЖДЕНИЕ")
        dialog.geometry("350x150")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="СБРОСИТЬ ВСЕ НАСТРОЙКИ?",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)
        ctk.CTkLabel(dialog, text="ЭТО ДЕЙСТВИЕ НЕЛЬЗЯ ОТМЕНИТЬ!",
                     font=ctk.CTkFont(size=11), text_color="#ff6666").pack()

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)

        def do_reset():
            for key in self.settings._defaults:
                self.settings.set(key, self.settings._defaults[key])
            self.settings.set_language("ru")
            dialog.destroy()
            self.pending_lang = "🇷🇺 Русский"
            self.pending_theme = "🌙 Тёмная"
            self.pending_restart = True
            self.show_restart_panel()
            self.load_settings()

        ctk.CTkButton(btn_frame, text="✅ ДА, СБРОСИТЬ", fg_color="#e74c3c",
                      command=do_reset).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="❌ ОТМЕНА", fg_color="#2c3e66",
                      command=dialog.destroy).pack(side="left", padx=10)

    def show_message(self, message):
        label = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=11),
                             fg_color="#2c3e66", corner_radius=8, padx=15, pady=8)
        label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(3000, label.destroy)
