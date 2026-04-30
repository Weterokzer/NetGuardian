import customtkinter as ctk
import psutil
import threading
import time


class ProcessItem(ctk.CTkFrame):
    """Один элемент процесса (карточка)"""

    def __init__(self, parent, process_info, kill_callback):
        super().__init__(parent, fg_color="#1a1a2a", corner_radius=8)
        self.process = process_info
        self.kill_callback = kill_callback

        self.pack(fill="x", pady=2, padx=5)
        self.create_widgets()

    def create_widgets(self):
        # Имя процесса (жирный)
        name = self.process['name'][:45] if len(self.process['name']) > 45 else self.process['name']
        ctk.CTkLabel(self, text=name, font=ctk.CTkFont(size=12, weight="bold"),
                     anchor="w").pack(side="left", padx=10, pady=8, fill="x", expand=True)

        # PID
        ctk.CTkLabel(self, text=f"PID: {self.process['pid']}",
                     font=ctk.CTkFont(size=10), text_color="#888",
                     width=70).pack(side="left", padx=5)

        # Память (с цветом)
        mem_mb = self.process['memory_mb']
        if mem_mb > 500:
            mem_color = "#ff6666"
        elif mem_mb > 200:
            mem_color = "#ffaa00"
        else:
            mem_color = "#00ff88"

        mem_text = f"💾 {self.process['memory']:.1f}% ({mem_mb:.0f} MB)"
        ctk.CTkLabel(self, text=mem_text, font=ctk.CTkFont(size=10),
                     text_color=mem_color, width=120).pack(side="left")

        # CPU
        if self.process['cpu'] > 50:
            cpu_color = "#ff6666"
        elif self.process['cpu'] > 20:
            cpu_color = "#ffaa00"
        else:
            cpu_color = "#00ff88"

        cpu_text = f"⚡ CPU: {self.process['cpu']:.0f}%"
        ctk.CTkLabel(self, text=cpu_text, font=ctk.CTkFont(size=10),
                     text_color=cpu_color, width=80).pack(side="left")

        # Кнопка убить
        ctk.CTkButton(self, text="✕", width=30, height=26,
                      fg_color="#c0392b", hover_color="#e74c3c",
                      font=ctk.CTkFont(size=12, weight="bold"),
                      command=lambda: self.kill_callback(self.process['pid'], self.process['name'])).pack(side="right",
                                                                                                          padx=8)


class ControlPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.all_processes = []
        self.is_loading = False

        # Настройки пагинации
        self.items_per_page = 30
        self.current_page = 0
        self.total_pages = 0
        self.filtered_processes = []

        self.create_widgets()
        self.load_processes()

    def create_widgets(self):
        # Заголовок
        header = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(header, text="🎮", font=ctk.CTkFont(size=38)).pack(pady=(15, 5))
        ctk.CTkLabel(header, text="NET GUARDIAN",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#00d4ff").pack()
        ctk.CTkLabel(header, text="PROCESS CONTROL",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#666").pack(pady=(0, 15))
        # Поиск
        self.search_entry = ctk.CTkEntry(header, width=250, placeholder_text="🔍 Поиск процесса...")
        self.search_entry.pack(side="right", padx=15)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_and_paginate())

        # Кнопка обновления
        self.refresh_btn = ctk.CTkButton(header, text="🔄", width=40,
                                         command=self.load_processes)
        self.refresh_btn.pack(side="right", padx=5)

        # Статистика
        stats_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1a1a2a")
        stats_frame.pack(fill="x", padx=20, pady=5)

        self.total_label = ctk.CTkLabel(stats_frame, text="📊 Всего процессов: 0",
                                        font=ctk.CTkFont(size=11))
        self.total_label.pack(side="left", padx=15, pady=6)

        self.sys_label = ctk.CTkLabel(stats_frame, text="💻 Система: загрузка...",
                                      font=ctk.CTkFont(size=11))
        self.sys_label.pack(side="right", padx=15, pady=6)

        # Панель пагинации
        self.pagination_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1a1a2a")
        self.pagination_frame.pack(fill="x", padx=20, pady=5)

        self.prev_btn = ctk.CTkButton(self.pagination_frame, text="◀ НАЗАД", width=100,
                                      state="disabled", command=self.prev_page)
        self.prev_btn.pack(side="left", padx=10, pady=5)

        self.page_label = ctk.CTkLabel(self.pagination_frame, text="Страница 0 из 0",
                                       font=ctk.CTkFont(size=11, weight="bold"))
        self.page_label.pack(side="left", expand=True, padx=10)

        self.next_btn = ctk.CTkButton(self.pagination_frame, text="ВПЕРЕД ▶", width=100,
                                      state="disabled", command=self.next_page)
        self.next_btn.pack(side="right", padx=10, pady=5)

        # Контейнер для списка процессов
        self.process_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.process_container.pack(fill="both", expand=True, padx=20, pady=5)

        # Индикатор загрузки
        self.loading_label = ctk.CTkLabel(self.process_container,
                                          text="⏳ Загрузка процессов...\n\n(это может занять несколько секунд)",
                                          font=ctk.CTkFont(size=14), text_color="#888")
        self.loading_label.pack(pady=50)

        # Таймер для автообновления статистики
        self.update_system_stats()

    def update_system_stats(self):
        """Обновление системной статистики"""
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            self.sys_label.configure(text=f"💻 CPU: {cpu}% | 🧠 RAM: {ram.percent}%")
        except:
            pass
        self.after(2000, self.update_system_stats)

    def load_processes(self):
        """Загрузка процессов в фоне"""
        if self.is_loading:
            return

        self.is_loading = True
        self.refresh_btn.configure(state="disabled", text="⏳")

        # Скрываем пагинацию
        self.pagination_frame.pack_forget()

        # Показываем загрузку
        self.loading_label.pack(pady=50)
        self._clear_process_list()

        def load():
            processes = []
            try:
                total_ram = psutil.virtual_memory().total

                for proc in psutil.process_iter(['name', 'pid', 'memory_percent', 'cpu_percent']):
                    try:
                        info = proc.info
                        if info['name'] and info['name'].strip():
                            mem_percent = info['memory_percent'] or 0
                            mem_mb = (mem_percent / 100) * total_ram / (1024 * 1024)

                            processes.append({
                                'name': info['name'],
                                'pid': info['pid'],
                                'memory': mem_percent,
                                'memory_mb': mem_mb,
                                'cpu': proc.cpu_percent(interval=0.03)
                            })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

                # Сортировка по памяти
                processes.sort(key=lambda x: x['memory'], reverse=True)
                return processes
            except Exception as e:
                return []

        def callback(processes):
            self.all_processes = processes
            self.total_label.configure(text=f"📊 Всего процессов: {len(processes)} (топ по памяти)")
            self.refresh_btn.configure(state="normal", text="🔄")
            self.is_loading = False
            self.loading_label.pack_forget()

            # Показываем пагинацию
            self.pagination_frame.pack(fill="x", padx=20, pady=5)

            # Применяем фильтр и пагинацию
            self.filter_and_paginate()

        threading.Thread(target=lambda: callback(load()), daemon=True).start()

    def filter_and_paginate(self):
        """Фильтрация и расчёт страниц"""
        search = self.search_entry.get().lower().strip()

        # Фильтруем
        if search:
            self.filtered_processes = [p for p in self.all_processes if search in p['name'].lower()]
        else:
            self.filtered_processes = self.all_processes.copy()

        # Рассчитываем страницы
        self.total_pages = max(1, (len(self.filtered_processes) + self.items_per_page - 1) // self.items_per_page)
        self.current_page = min(self.current_page, self.total_pages - 1)
        self.current_page = max(0, self.current_page)

        # Обновляем пагинацию
        self.update_pagination_controls()

        # Показываем текущую страницу
        self.display_current_page()

    def display_current_page(self):
        """Отображение текущей страницы"""
        self._clear_process_list()

        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.filtered_processes))

        page_processes = self.filtered_processes[start_idx:end_idx]

        if not page_processes and not self.is_loading:
            empty_label = ctk.CTkLabel(self.process_container,
                                       text="🔍 Ничего не найдено\n\nИзмените поисковый запрос или нажмите 'Обновить'",
                                       font=ctk.CTkFont(size=13), text_color="#888")
            empty_label.pack(pady=50)
            return

        for proc in page_processes:
            ProcessItem(self.process_container, proc, self.kill_process)

        # Обновляем информацию на панели
        start_num = start_idx + 1 if page_processes else 0
        end_num = end_idx
        self.page_label.configure(
            text=f"Страница {self.current_page + 1} из {self.total_pages}  |  Показано: {start_num}-{end_num} из {len(self.filtered_processes)}")

    def update_pagination_controls(self):
        """Обновление состояния кнопок пагинации"""
        if self.total_pages <= 1:
            self.prev_btn.configure(state="disabled")
            self.next_btn.configure(state="disabled")
        else:
            self.prev_btn.configure(state="normal" if self.current_page > 0 else "disabled")
            self.next_btn.configure(state="normal" if self.current_page < self.total_pages - 1 else "disabled")

    def prev_page(self):
        """Предыдущая страница"""
        if self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()
            self.update_pagination_controls()

    def next_page(self):
        """Следующая страница"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_current_page()
            self.update_pagination_controls()

    def _clear_process_list(self):
        """Очистка списка процессов"""
        for w in self.process_container.winfo_children():
            if w != self.loading_label:
                w.destroy()

    def kill_process(self, pid, name):
        """Завершение процесса с подтверждением"""
        # Создаём диалог подтверждения
        dialog = ctk.CTkToplevel(self)
        dialog.title("Подтверждение")
        dialog.geometry("380x180")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Центрируем
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 380) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 180) // 2
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(dialog, text="⚠️", font=ctk.CTkFont(size=40)).pack(pady=10)

        ctk.CTkLabel(dialog, text=f"Завершить процесс:", font=ctk.CTkFont(size=13)).pack()
        ctk.CTkLabel(dialog, text=f"\"{name[:50]}\" (PID: {pid})",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color="#ffaa00").pack()
        ctk.CTkLabel(dialog, text="Это действие необратимо!",
                     font=ctk.CTkFont(size=11), text_color="#ff6666").pack(pady=5)

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        def do_kill():
            dialog.destroy()

            def kill():
                try:
                    proc = psutil.Process(pid)
                    proc.terminate()
                    time.sleep(0.5)
                    if proc.is_running():
                        proc.kill()
                    self.after(0, lambda: self.show_message(f"✅ \"{name[:40]}\" завершён", "success"))
                    self.after(1000, self.load_processes)
                except psutil.NoSuchProcess:
                    self.after(0, lambda: self.show_message(f"ℹ️ Процесс уже завершён", "info"))
                    self.after(1000, self.load_processes)
                except Exception as e:
                    self.after(0, lambda: self.show_message(f"❌ Ошибка: {str(e)[:50]}", "error"))

            threading.Thread(target=kill, daemon=True).start()

        ctk.CTkButton(btn_frame, text="✅ ЗАВЕРШИТЬ", fg_color="#c0392b",
                      command=do_kill).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="❌ ОТМЕНА", fg_color="#2c3e66",
                      command=dialog.destroy).pack(side="left", padx=10)

    def show_message(self, message, msg_type="info"):
        """Красивое всплывающее сообщение"""
        colors = {
            "success": "#2ecc71",
            "error": "#e74c3c",
            "info": "#3498db"
        }

        # Удаляем старые сообщения
        for w in self.winfo_children():
            if isinstance(w, ctk.CTkLabel) and getattr(w, 'is_temp', False):
                w.destroy()

        label = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=12),
                             fg_color=colors.get(msg_type, "#2c3e66"),
                             corner_radius=10, padx=20, pady=10)
        label.is_temp = True
        label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(2500, label.destroy)