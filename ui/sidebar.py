import customtkinter as ctk
from core.language import Language
from utils.simple_tooltip import add_tooltip
lang = Language()


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, callback):
        self.callback = callback
        self.buttons = {}

        # Определяем цвета в зависимости от темы ПРИ СОЗДАНИИ
        self.update_colors()

        super().__init__(parent, width=250, corner_radius=0, fg_color=self.bg_color)
        self.grid_propagate(False)

        self.create_widgets()

        # Подписываемся на смену темы
        self.bind("<Map>", lambda e: self.refresh_theme())

    def update_colors(self):
        """Обновление цветов в зависимости от темы"""
        is_dark = ctk.get_appearance_mode() == "Dark"

        if is_dark:
            # Тёмная тема
            self.bg_color = "#0f0f1a"
            self.btn_fg = "transparent"
            self.btn_text = "#ffffff"
            self.btn_hover = "#1a2a3a"
            self.logo_color = "#00d4ff"
            self.text_secondary = "#666"
            self.sep_color = "#2c3e66"
            self.status_color = "#00ff88"
            self.credit_color = "#666"
        else:
            # Светлая тема
            self.bg_color = "#f0f0f5"
            self.btn_fg = "transparent"
            self.btn_text = "#1a1a2e"
            self.btn_hover = "#e0e0e8"
            self.logo_color = "#0066cc"
            self.text_secondary = "#999"
            self.sep_color = "#c0c0d0"
            self.status_color = "#00aa44"
            self.credit_color = "#aaa"

    def refresh_theme(self):
        """Обновление темы при смене"""
        self.update_colors()
        self.configure(fg_color=self.bg_color)

        # Обновляем логотип и все кнопки
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def create_widgets(self):
        # Логотип
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=25)

        ctk.CTkLabel(logo_frame, text="🛡️", font=ctk.CTkFont(size=48),
                     text_color=self.logo_color).pack()

        ctk.CTkLabel(logo_frame, text="NET GUARDIAN",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=self.logo_color).pack()

        ctk.CTkLabel(logo_frame, text="ULTIMATE",
                     font=ctk.CTkFont(size=12),
                     text_color=self.text_secondary).pack()

        # Разделитель
        ctk.CTkFrame(self, height=2, fg_color=self.sep_color).pack(fill="x", padx=20, pady=15)

        # Кнопки навигации
        nav_items = [
            (lang.get("menu_speed"), "speed"),
            (lang.get("menu_control"), "control"),
            (lang.get("menu_ports"), "ports"),
            (lang.get("menu_torrent"), "torrent"),
            (lang.get("menu_stats"), "stats"),
            (lang.get("menu_settings"), "settings"),
            (lang.get("menu_system"), "system")
        ]

        for text, page_id in nav_items:
            btn = ctk.CTkButton(
                self,
                text=text,
                font=ctk.CTkFont(size=14),
                fg_color=self.btn_fg,
                text_color=self.btn_text,
                hover_color=self.btn_hover,
                anchor="w",
                height=45,
                corner_radius=8,
                command=lambda p=page_id: self.callback(p)
            )
            btn.pack(pady=3, padx=15, fill="x")
            self.buttons[page_id] = btn

        # ========== ПОДСКАЗКИ К КНОПКАМ ==========
        tips = {
            "speed": "📡 Мониторинг скорости в реальном времени\nГрафики загрузки и отдачи",
            "control": "🎮 Управление процессами\nПоиск, фильтрация, завершение процессов",
            "ports": "🌊 Управление портами брандмауэра\nОткрытие/закрытие портов",
            "torrent": "🏴‍☠️ Защита торрент-трафика\nОграничение скорости выгрузки",
            "stats": "📊 Статистика тестов скорости\nИстория и анализ",
            "settings": "⚙️ Настройки приложения\nТема, язык, автозапуск",
            "system": "🔧 Системные утилиты\nОчистка, оптимизация, сканер"
        }

        for page_id, tip in tips.items():
            if page_id in self.buttons:
                add_tooltip(self.buttons[page_id], tip)
        # ========== КОНЕЦ ПОДСКАЗОК ==========

        # Статус внизу
        status_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=10)
        status_frame.pack(side="bottom", fill="x", padx=15, pady=20)

        ctk.CTkLabel(status_frame, text="🟢", font=ctk.CTkFont(size=12)).pack(side="left", padx=8, pady=5)
        ctk.CTkLabel(status_frame, text="ВСЕГДА НА СТРАЖЕ",
                     font=ctk.CTkFont(size=10, weight="bold"),
                     text_color=self.status_color).pack(side="left")

        # Креативное описание
        ctk.CTkLabel(self, text="⚡ Создано с поддержкой\n   без сна и булка с чаем",
                     font=ctk.CTkFont(size=9),
                     text_color=self.credit_color,
                     justify="left").pack(side="bottom", pady=10)

    def set_active(self, page_id):
        for pid, btn in self.buttons.items():
            if pid == page_id:
                btn.configure(fg_color=self.btn_hover)
            else:
                btn.configure(fg_color="transparent")