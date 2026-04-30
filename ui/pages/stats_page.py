import customtkinter as ctk
import json
import os
from datetime import datetime
from collections import deque


class StatsHistory:
    def __init__(self):
        self.history_file = os.path.expanduser("~/.netguardian_history.json")
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except:
            pass

    def add_test(self, download, upload, ping):
        self.history.insert(0, {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "download": round(download, 1),
            "upload": round(upload, 1),
            "ping": round(ping, 0)
        })
        self.history = self.history[:100]
        self.save_history()

    def get_history(self):
        return self.history

    def get_stats(self):
        if not self.history:
            return None
        downloads = [h['download'] for h in self.history]
        uploads = [h['upload'] for h in self.history]
        pings = [h['ping'] for h in self.history]
        return {
            'max_download': max(downloads),
            'min_download': min(downloads),
            'avg_download': sum(downloads) / len(downloads),
            'max_upload': max(uploads),
            'min_upload': min(uploads),
            'avg_upload': sum(uploads) / len(uploads),
            'avg_ping': sum(pings) / len(pings),
            'total_tests': len(self.history)
        }

    def clear_history(self):
        self.history = []
        self.save_history()


class StatsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.history = StatsHistory()
        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        # Заголовок в стиле главного логотипа
        header = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(header, text="📊", font=ctk.CTkFont(size=38)).pack(pady=(15, 5))
        ctk.CTkLabel(header, text="NET GUARDIAN",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#00d4ff").pack()
        ctk.CTkLabel(header, text="STATISTICS",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#666").pack(pady=(0, 15))

        # Верхняя панель с кнопками
        top_panel = ctk.CTkFrame(self, corner_radius=10, fg_color="#1a1a2a")
        top_panel.pack(fill="x", padx=20, pady=5)

        self.refresh_btn = ctk.CTkButton(top_panel, text="🔄 ОБНОВИТЬ", width=120,
                                         fg_color="#d35400", command=self.refresh)
        self.refresh_btn.pack(side="left", padx=10, pady=10)

        self.clear_btn = ctk.CTkButton(top_panel, text="🗑️ ОЧИСТИТЬ ИСТОРИЮ", width=150,
                                       fg_color="#e74c3c", hover_color="#c0392b",
                                       command=self.clear_history)
        self.clear_btn.pack(side="left", padx=10, pady=10)

        # Статистика
        self.stats_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        self.stats_frame.pack(fill="x", padx=20, pady=10)

        # Список истории
        history_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(history_frame, text="📜 ПОСЛЕДНИЕ ТЕСТЫ",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffaa00").pack(pady=8)

        self.history_text = ctk.CTkTextbox(history_frame, font=ctk.CTkFont(family="Consolas", size=11),
                                           state="disabled")
        self.history_text.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh(self):
        self._update_stats()
        self._update_history()

    def _update_stats(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()

        stats = self.history.get_stats()

        if stats:
            stats_container = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
            stats_container.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(stats_container, text="📈 СТАТИСТИКА ЗА ВСЁ ВРЕМЯ",
                         font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="#00d4ff").pack(pady=5)

            grid_frame = ctk.CTkFrame(stats_container, fg_color="transparent")
            grid_frame.pack(pady=10)

            stats_data = [
                ("📥 МАКС. ЗАГРУЗКА:", f"{stats['max_download']:.1f} Mbps", "#00ff88"),
                ("📥 МИН. ЗАГРУЗКА:", f"{stats['min_download']:.1f} Mbps", "#ffaa00"),
                ("📥 СРЕД. ЗАГРУЗКА:", f"{stats['avg_download']:.1f} Mbps", "#00cc66"),
                ("📤 МАКС. ОТДАЧА:", f"{stats['max_upload']:.1f} Mbps", "#ffaa00"),
                ("📤 МИН. ОТДАЧА:", f"{stats['min_upload']:.1f} Mbps", "#ff8800"),
                ("📤 СРЕД. ОТДАЧА:", f"{stats['avg_upload']:.1f} Mbps", "#ffaa00"),
                ("🏓 СРЕД. ПИНГ:", f"{stats['avg_ping']:.0f} ms", "#3498db"),
                ("📋 ВСЕГО ТЕСТОВ:", str(stats['total_tests']), "#9b59b6")
            ]

            for i, (label, value, color) in enumerate(stats_data):
                row = i // 2
                col = i % 2
                frame = ctk.CTkFrame(grid_frame, corner_radius=8, fg_color="#0f0f1a")
                frame.grid(row=row, column=col, padx=5, pady=3, sticky="ew")

                ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=11)).pack(side="left", padx=10, pady=6)
                ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=11, weight="bold"),
                             text_color=color).pack(side="right", padx=10, pady=6)

                grid_frame.grid_columnconfigure(col, weight=1)
        else:
            ctk.CTkLabel(self.stats_frame, text="📭 НЕТ ДАННЫХ. ЗАПУСТИТЕ SPEEDTEST!",
                         font=ctk.CTkFont(size=13), text_color="#ffaa00").pack(pady=20)

    def _update_history(self):
        history = self.history.get_history()

        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", "end")

        if history:
            header = f"{'№':<4} | {'ДАТА И ВРЕМЯ':<20} | {'ЗАГРУЗКА':<10} | {'ОТДАЧА':<10} | {'ПИНГ':<8}\n"
            header += "-" * 70 + "\n"
            self.history_text.insert("1.0", header)

            for i, test in enumerate(history, 1):
                line = f"{i:<4} | {test['timestamp']:<20} | {test['download']:<10} | {test['upload']:<10} | {test['ping']:<8} ms\n"
                self.history_text.insert("end", line)

            self.history_text.insert("end", "\n" + "-" * 70 + "\n")
            self.history_text.insert("end", f"📁 ИСТОРИЯ СОХРАНЕНА: {os.path.expanduser('~/.netguardian_history.json')}")
        else:
            self.history_text.insert("1.0", "📭 НЕТ СОХРАНЁННЫХ ТЕСТОВ.\n\nЗАПУСТИТЕ SPEEDTEST НА ГЛАВНОЙ СТРАНИЦЕ!")

        self.history_text.configure(state="disabled")

    def add_test_result(self, download, upload, ping):
        self.history.add_test(download, upload, ping)
        self.refresh()

    def clear_history(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("ПОДТВЕРЖДЕНИЕ")
        dialog.geometry("350x150")
        dialog.transient(self)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="🗑️ ОЧИСТИТЬ ВСЮ ИСТОРИЮ?",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=20)
        ctk.CTkLabel(dialog, text="ВСЕ ТЕСТЫ БУДУТ УДАЛЕНЫ НАВСЕГДА!",
                     font=ctk.CTkFont(size=11), text_color="#ff6666").pack()

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)

        def do_clear():
            self.history.clear_history()
            self.refresh()
            dialog.destroy()
            self.show_message("✅ ИСТОРИЯ ОЧИЩЕНА")

        ctk.CTkButton(btn_frame, text="✅ ДА, ОЧИСТИТЬ", fg_color="#e74c3c",
                      command=do_clear).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="❌ ОТМЕНА", command=dialog.destroy).pack(side="left", padx=10)

    def show_message(self, text):
        label = ctk.CTkLabel(self, text=text, font=ctk.CTkFont(size=11),
                             fg_color="#2c3e66", corner_radius=8, padx=15, pady=8)
        label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(2000, label.destroy)