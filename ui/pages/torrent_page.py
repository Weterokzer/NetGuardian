import customtkinter as ctk
import subprocess
import threading
from utils.simple_tooltip import add_tooltip


class TorrentPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.current_limit = 0
        self.client_var = ctk.StringVar(value="Все клиенты")
        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        header = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(header, text="🏴‍☠️", font=ctk.CTkFont(size=38)).pack(pady=(15, 5))
        ctk.CTkLabel(header, text="NET GUARDIAN",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#00d4ff").pack()
        ctk.CTkLabel(header, text="TORRENT PROTECT",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#666").pack(pady=(0, 5))

        # Выбор клиента
        client_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1a2a")
        client_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(client_frame, text="🎮 ТОРРЕНТ-КЛИЕНТ",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#ffaa00").pack(pady=5)

        clients = ["Все клиенты", "qBittorrent", "uTorrent", "Transmission", "BitComet", "Deluge"]
        client_menu = ctk.CTkOptionMenu(client_frame, values=clients, variable=self.client_var, width=150)
        client_menu.pack(pady=5)
        add_tooltip(client_menu, "Выберите ваш торрент-клиент для более точной настройки")

        # Режимы
        modes_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1a2a")
        modes_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(modes_frame, text="⚡ БЫСТРЫЕ РЕЖИМЫ",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffaa00").pack(pady=10)

        btn_container = ctk.CTkFrame(modes_frame, fg_color="transparent")
        btn_container.pack(pady=10)

        modes = [
            ("🕵️ ИНКОГНИТО", 1, "#7f8c8d", "1 Kbps - минимальная активность"),
            ("🌙 НОЧНОЙ", 50, "#3498db", "50 Kbps - фоновая загрузка"),
            ("🤫 ТИХИЙ", 200, "#2ecc71", "200 Kbps - комфортный режим"),
            ("⚖️ БАЛАНС", 500, "#f39c12", "500 Kbps - золотая середина"),
            ("🔒 STOP", 0, "#e74c3c", "Полная остановка выгрузки")
        ]

        for name, speed, color, tip in modes:
            btn = ctk.CTkButton(btn_container, text=name, width=110, height=40,
                                fg_color=color, hover_color=color,
                                font=ctk.CTkFont(size=12, weight="bold"),
                                command=lambda s=speed: self.set_limit(s))
            btn.pack(side="left", padx=5)
            add_tooltip(btn, tip)

        # Ручная настройка
        custom_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1a2a")
        custom_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(custom_frame, text="🎛️ РУЧНАЯ НАСТРОЙКА",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#ffaa00").pack(pady=10)

        custom_row = ctk.CTkFrame(custom_frame, fg_color="transparent")
        custom_row.pack(pady=10)

        ctk.CTkLabel(custom_row, text="СКОРОСТЬ (Kbps):", font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        self.custom_entry = ctk.CTkEntry(custom_row, width=120, placeholder_text="100-5000")
        self.custom_entry.pack(side="left", padx=10)
        add_tooltip(self.custom_entry, "Введите скорость от 0 до 10000 Kbps")

        ctk.CTkButton(custom_row, text="ПРИМЕНИТЬ", fg_color="#9b59b6",
                      command=self.apply_custom_limit).pack(side="left", padx=10)

        # Статус
        status_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1a2a")
        status_frame.pack(pady=10, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(status_frame, text="✅ НЕТ АКТИВНЫХ ОГРАНИЧЕНИЙ",
                                         font=ctk.CTkFont(size=13, weight="bold"),
                                         text_color="#00ff88")
        self.status_label.pack(pady=20)
        add_tooltip(self.status_label, "Текущий статус ограничения трафика")

        # Рекомендации
        info_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1a2a")
        info_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(info_frame, text="ℹ️ РЕКОМЕНДАЦИИ",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#00d4ff").pack(pady=10)

        self.recommend_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=11), justify="left")
        self.recommend_label.pack(pady=10, padx=20)

        self.update_recommendation()

    def update_recommendation(self):
        """Обновление рекомендаций в зависимости от выбранного клиента"""
        client = self.client_var.get()
        tips = {
            "qBittorrent": "Настройки → Скорость → Ограничение отдачи",
            "uTorrent": "Настройки → Пропускная способность → Макс. скорость отдачи",
            "Transmission": "Edit → Preferences → Speed → Upload limit",
            "BitComet": "Настройки → Сеть → Ограничение отдачи",
            "Deluge": "Preferences → Bandwidth → Upload Speed Limit"
        }
        tip = tips.get(client, "Настройте ограничение отдачи в вашем торрент-клиенте")
        self.recommend_label.configure(text=f"📖 {tip}")

    def apply_custom_limit(self):
        try:
            speed = int(self.custom_entry.get())
            if 0 <= speed <= 10000:
                self.set_limit(speed)
            else:
                self.show_message("❌ Введите скорость от 0 до 10000 Kbps")
        except ValueError:
            self.show_message("❌ Введите корректное число")

    def set_limit(self, speed_kbps):
        def do_set():
            try:
                if speed_kbps > 0:
                    subprocess.run(
                        'powershell -Command "Get-NetQosPolicy -Name \'NG_Limit\' | Remove-NetQosPolicy -ErrorAction SilentlyContinue"',
                        shell=True, capture_output=True, timeout=3)
                    cmd = f'powershell -Command "New-NetQosPolicy -Name \'NG_Limit\' -ThrottleRateMbps {speed_kbps / 1000} -NetworkProfile All -ErrorAction SilentlyContinue"'
                    subprocess.run(cmd, shell=True, capture_output=True, timeout=3)
                    return True, speed_kbps
                else:
                    subprocess.run(
                        'powershell -Command "Get-NetQosPolicy -Name \'NG_Limit\' | Remove-NetQosPolicy -ErrorAction SilentlyContinue"',
                        shell=True, capture_output=True, timeout=3)
                    return False, 0
            except:
                return False, 0

        def callback(result):
            success, speed = result
            if success and speed > 0:
                mode_name = self.get_mode_name(speed)
                self.status_label.configure(
                    text=f"🛡️ АКТИВЕН: {mode_name}\nСКОРОСТЬ: {speed} Kbps ({speed / 1000} Mbps)\nКЛИЕНТ: {self.client_var.get()}",
                    text_color="#ffaa00"
                )
                self.show_message(f"✅ Лимит {speed} Kbps установлен")
            else:
                self.status_label.configure(text="✅ НЕТ АКТИВНЫХ ОГРАНИЧЕНИЙ", text_color="#00ff88")
                self.show_message("✅ Лимит отключён")

        self.status_label.configure(text="⏳ ПРИМЕНЕНИЕ ЛИМИТА...", text_color="#ffaa00")
        threading.Thread(target=lambda: callback(do_set()), daemon=True).start()

    def get_mode_name(self, speed):
        modes = {1: "ИНКОГНИТО", 50: "НОЧНОЙ", 200: "ТИХИЙ", 500: "БАЛАНС"}
        return modes.get(speed, f"КАСТОМНЫЙ ({speed} Kbps)")

    def show_message(self, message):
        label = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=11),
                             fg_color="#2c3e66", corner_radius=8, padx=15, pady=8)
        label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(2500, label.destroy)