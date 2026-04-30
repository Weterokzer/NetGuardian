import customtkinter as ctk
import threading
import socket
import subprocess


class NetworkScanPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.is_scanning = False
        self.create_widgets()

    def create_widgets(self):
        # Заголовок в стиле главного логотипа
        header = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        header.pack(fill="x", padx=20, pady=10)

        # Иконка как в сайдбаре
        ctk.CTkLabel(header, text="🌐", font=ctk.CTkFont(size=38)).pack(pady=(15, 5))

        # Название как в сайдбаре
        ctk.CTkLabel(header, text="NET GUARDIAN",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#00d4ff").pack()

        ctk.CTkLabel(header, text="SCAN",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#666").pack(pady=(0, 15))

        # Прогресс-бар
        progress_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20, pady=10)

        self.progress_label = ctk.CTkLabel(progress_frame, text="⚡ ГОТОВ К СКАНИРОВАНИЮ",
                                           font=ctk.CTkFont(size=13, weight="bold"),
                                           text_color="#00d4ff")
        self.progress_label.pack(pady=8)

        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=450, height=12,
                                               progress_color="#00d4ff",
                                               fg_color="#2a2a3a")
        self.progress_bar.pack(pady=10, padx=20)
        self.progress_bar.set(0)

        # Кнопка сканирования
        self.scan_btn = ctk.CTkButton(self, text="🔍 СКАНИРОВАТЬ СЕТЬ",
                                      fg_color="#d35400", hover_color="#e67e22",
                                      height=50, font=ctk.CTkFont(size=15, weight="bold"),
                                      corner_radius=12,
                                      command=self.scan_network)
        self.scan_btn.pack(pady=15, padx=20)

        # Результаты
        result_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(result_frame, text="📡 УСТРОЙСТВА В СЕТИ",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffaa00").pack(pady=8)

        self.result_text = ctk.CTkTextbox(result_frame, font=ctk.CTkFont(family="Consolas", size=11),
                                          state="disabled")
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Статус
        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=11), text_color="#888")
        self.status_label.pack(pady=5)

    def get_local_ip(self):
        """Получение локального IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "192.168.1.1"

    def scan_network(self):
        if self.is_scanning:
            return

        self.is_scanning = True
        self.scan_btn.configure(state="disabled", text="⏳ СКАНИРОВАНИЕ...")
        self.progress_bar.set(0)

        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "🔍 СКАНИРОВАНИЕ СЕТИ...\n\n")
        self.result_text.configure(state="disabled")

        threading.Thread(target=self.scan, daemon=True).start()

    def scan(self):
        local_ip = self.get_local_ip()
        ip_parts = local_ip.split('.')
        network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}"

        devices = []
        total_ips = 254

        for i in range(1, 255):
            ip = f"{network}.{i}"

            # Обновляем прогресс
            progress = i / total_ips
            self.after(0, lambda p=progress, c=i: self.update_progress(p, c, total_ips))

            try:
                result = subprocess.run(f"ping -n 1 -w 300 {ip}", shell=True, capture_output=True, text=True)
                if "TTL=" in result.stdout or "ttl=" in result.stdout.lower():
                    try:
                        hostname = socket.gethostbyaddr(ip)[0]
                    except:
                        hostname = "Неизвестно"

                    devices.append((ip, hostname))
            except:
                continue

        self.after(0, lambda: self.show_results(devices))

    def update_progress(self, progress, current, total):
        """Обновление прогресс-бара"""
        self.progress_bar.set(progress)
        percent = int(progress * 100)
        self.progress_label.configure(text=f"📡 СКАНИРОВАНИЕ: {current}/255 IP-АДРЕСОВ ({percent}%)")

        if current == total:
            self.progress_label.configure(text="✅ СКАНИРОВАНИЕ ЗАВЕРШЕНО!", text_color="#00ff88")

    def show_results(self, devices):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")

        if devices:
            result = "╔" + "═" * 58 + "╗\n"
            result += f"║  🌐 НАЙДЕНО УСТРОЙСТВ: {len(devices):<37} ║\n"
            result += "╠" + "═" * 58 + "╣\n"

            for ip, hostname in devices:
                result += f"║  📱 IP: {ip:<48} ║\n"
                result += f"║     Имя: {hostname[:45]:<45} ║\n"
                result += "╟" + "─" * 58 + "╢\n"

            result = result[:-4]  # Убираем последнюю линию
            result += "╚" + "═" * 58 + "╝"
        else:
            result = "╔" + "═" * 58 + "╗\n"
            result += "║  ❌ УСТРОЙСТВА НЕ НАЙДЕНЫ                    ║\n"
            result += "║                                             ║\n"
            result += "║  ПРОВЕРЬТЕ ПОДКЛЮЧЕНИЕ К СЕТИ               ║\n"
            result += "╚" + "═" * 58 + "╝"

        self.result_text.insert("1.0", result)
        self.result_text.configure(state="disabled")

        self.scan_btn.configure(state="normal", text="🔍 СКАНИРОВАТЬ СЕТЬ")
        self.status_label.configure(text=f"✅ Завершено. Найдено устройств: {len(devices)}")
        self.is_scanning = False

        # Сбрасываем прогресс через 3 секунды
        self.after(3000, self.reset_progress)

    def reset_progress(self):
        """Сброс прогресс-бара"""
        self.progress_bar.set(0)
        self.progress_label.configure(text="⚡ ГОТОВ К СКАНИРОВАНИЮ", text_color="#00d4ff")