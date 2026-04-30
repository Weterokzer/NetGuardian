import customtkinter as ctk
import subprocess
import threading
from utils.simple_tooltip import add_tooltip

class PortManager:
    def __init__(self):
        pass

    def open_port(self, port, protocol="TCP"):
        try:
            cmd = f'netsh advfirewall firewall add rule name="NG_Port_{port}" dir=in action=allow protocol={protocol} localport={port}'
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            return True, f"Порт {port}/{protocol} открыт"
        except Exception as e:
            return False, str(e)

    def close_port(self, port):
        try:
            cmd = f'netsh advfirewall firewall delete rule name="NG_Port_{port}"'
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
            return True, f"Порт {port} закрыт"
        except Exception as e:
            return False, str(e)

    def list_rules(self):
        try:
            cmd = 'netsh advfirewall firewall show rule name=all dir=in | findstr "NG_Port"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
            return result.stdout if result.stdout else "Нет активных правил"
        except:
            return "Ошибка получения правил"


class PortsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.port_manager = PortManager()
        self.create_widgets()
        self.refresh_rules()

    def create_widgets(self):
        # Заголовок в стиле главного логотипа
        header = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        header.pack(fill="x", padx=20, pady=10)

        # Иконка
        ctk.CTkLabel(header, text="🌊", font=ctk.CTkFont(size=38)).pack(pady=(15, 5))

        # Название
        ctk.CTkLabel(header, text="NET GUARDIAN",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#00d4ff").pack()

        ctk.CTkLabel(header, text="PORTS",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#666").pack(pady=(0, 15))

        # Панель управления
        control_panel = ctk.CTkFrame(self, corner_radius=12, fg_color="#1a1a2a")
        control_panel.pack(pady=15, padx=20, fill="x")

        # Ввод
        input_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
        input_frame.pack(pady=20)

        ctk.CTkLabel(input_frame, text="НОМЕР ПОРТА:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left",
                                                                                                      padx=10)
        self.port_entry = ctk.CTkEntry(input_frame, width=120, placeholder_text="6881")
        self.port_entry.pack(side="left", padx=10)

        # Быстрые порты
        quick_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
        quick_frame.pack(pady=5)

        ctk.CTkLabel(quick_frame, text="БЫСТРЫЕ ПОРТЫ:", font=ctk.CTkFont(size=11, weight="bold")).pack(side="left",
                                                                                                        padx=10)

        quick_ports = [("80 (HTTP)", 80), ("443 (HTTPS)", 443), ("22 (SSH)", 22), ("3389 (RDP)", 3389),
                       ("6881 (BT)", 6881)]

        for name, port in quick_ports:
            btn = ctk.CTkButton(quick_frame, text=name, width=70, height=25,
                                fg_color="#2c3e66", font=ctk.CTkFont(size=10),
                                command=lambda p=port: self.set_port(p))
            btn.pack(side="left", padx=3)
            add_tooltip(btn, f"Установить порт {name}")

        ctk.CTkLabel(input_frame, text="ПРОТОКОЛ:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=10)
        self.protocol_var = ctk.StringVar(value="TCP")
        protocol_menu = ctk.CTkOptionMenu(control_panel, values=["TCP", "UDP"],
                                          variable=self.protocol_var, width=100)
        protocol_menu.pack(pady=5)

        # Кнопки
        btn_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
        btn_frame.pack(pady=15)

        self.open_btn = ctk.CTkButton(btn_frame, text="🔓 ОТКРЫТЬ", fg_color="#2ecc71", hover_color="#27ae60",
                                      width=120, command=self.open_port)
        self.open_btn.pack(side="left", padx=10)

        self.close_btn = ctk.CTkButton(btn_frame, text="🔒 ЗАКРЫТЬ", fg_color="#e74c3c", hover_color="#c0392b",
                                       width=120, command=self.close_port)
        self.close_btn.pack(side="left", padx=10)

        self.status_label = ctk.CTkLabel(control_panel, text="⚡ ГОТОВ К РАБОТЕ",
                                         font=ctk.CTkFont(size=11), text_color="#00d4ff")
        self.status_label.pack(pady=10)

        # Список правил
        rules_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        rules_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(rules_frame, text="📋 АКТИВНЫЕ ПРАВИЛА",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffaa00").pack(pady=8)

        self.rules_text = ctk.CTkTextbox(rules_frame, font=ctk.CTkFont(family="Consolas", size=11),
                                         state="normal")
        self.rules_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_btn = ctk.CTkButton(rules_frame, text="🔄 ОБНОВИТЬ", width=120,
                                         fg_color="#d35400", command=self.refresh_rules)
        self.refresh_btn.pack(pady=10)

    def open_port(self):
        def do_open():
            try:
                port = int(self.port_entry.get())
                if 1 <= port <= 65535:
                    success, msg = self.port_manager.open_port(port, self.protocol_var.get())
                    return success, msg
                return False, "Порт вне диапазона (1-65535)"
            except ValueError:
                return False, "Введите число"

        def callback(result):
            success, msg = result
            if success:
                self.status_label.configure(text=f"✅ {msg}", text_color="#00ff88")
            else:
                self.status_label.configure(text=f"❌ {msg}", text_color="#ff6666")
            self.refresh_rules()

        self.status_label.configure(text="⏳ ОТКРЫТИЕ ПОРТА...", text_color="#ffaa00")
        threading.Thread(target=lambda: callback(do_open()), daemon=True).start()

    def close_port(self):
        def do_close():
            try:
                port = int(self.port_entry.get())
                success, msg = self.port_manager.close_port(port)
                return success, msg
            except ValueError:
                return False, "Введите число"

        def callback(result):
            success, msg = result
            if success:
                self.status_label.configure(text=f"✅ {msg}", text_color="#00ff88")
            else:
                self.status_label.configure(text=f"❌ {msg}", text_color="#ff6666")
            self.refresh_rules()

        self.status_label.configure(text="⏳ ЗАКРЫТИЕ ПОРТА...", text_color="#ffaa00")
        threading.Thread(target=lambda: callback(do_close()), daemon=True).start()

    def refresh_rules(self):
        self.rules_text.configure(state="normal")
        self.rules_text.delete("1.0", "end")
        rules = self.port_manager.list_rules()

        if rules and "Нет активных правил" not in rules:
            result = "╔" + "═" * 58 + "╗\n"
            result += "║  🛡️ АКТИВНЫЕ ПРАВИЛА БРАНДМАУЭРА              ║\n"
            result += "╠" + "═" * 58 + "╣\n"

            for line in rules.split('\n')[:20]:
                if line.strip():
                    result += f"║  {line[:54]:<54} ║\n"
            result += "╚" + "═" * 58 + "╝"
        else:
            result = "╔" + "═" * 58 + "╗\n"
            result += "║  ❌ НЕТ АКТИВНЫХ ПРАВИЛ NG                  ║\n"
            result += "╚" + "═" * 58 + "╝"

        self.rules_text.insert("1.0", result)
        self.rules_text.configure(state="disabled")

    def set_port(self, port):
        self.port_entry.delete(0, "end")
        self.port_entry.insert(0, str(port))