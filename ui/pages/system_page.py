import customtkinter as ctk
import psutil
import subprocess
import os
import threading
import shutil
from datetime import datetime
from core.language import Language

lang = Language()


class SystemPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.create_widgets()
        self.update_system_info()
        self.update_battery_info()
        self.update_temperature()

    def create_widgets(self):
        from utils.simple_tooltip import add_tooltip

        # Заголовок
        header = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(header, text="🔧", font=ctk.CTkFont(size=38)).pack(pady=(15, 5))
        ctk.CTkLabel(header, text="NET GUARDIAN",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#00d4ff").pack()
        ctk.CTkLabel(header, text=lang.get("system_title").upper(),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#666").pack(pady=(0, 15))

        # Основной контейнер с 2 колонками
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Левая колонка
        left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Правая колонка
        right_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=10)

        # === ЛЕВАЯ КОЛОНКА ===
        # Очистка TEMP
        clean_frame = ctk.CTkFrame(left_frame, corner_radius=12, fg_color="#1a1a2a")
        clean_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(clean_frame, text=lang.get("system_clean_title"),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffaa00").pack(pady=5)

        self.clean_btn = ctk.CTkButton(clean_frame, text=lang.get("system_clean_button"),
                                       fg_color="#e67e22", command=self.clean_temp)
        self.clean_btn.pack(pady=5, padx=20)
        add_tooltip(self.clean_btn, "🗑️ Удаляет временные файлы\nОсвобождает место на диске")

        self.clean_status = ctk.CTkLabel(clean_frame, text="", font=ctk.CTkFont(size=11))
        self.clean_status.pack(pady=5)

        # Диск анализатор
        disk_frame = ctk.CTkFrame(left_frame, corner_radius=12, fg_color="#1a1a2a")
        disk_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(disk_frame, text=lang.get("system_disk_title"),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffaa00").pack(pady=5)

        self.disk_btn = ctk.CTkButton(disk_frame, text=lang.get("system_disk_button"),
                                      command=self.disk_analyzer)
        self.disk_btn.pack(pady=5, padx=20)
        add_tooltip(self.disk_btn, "📀 Находит самые большие файлы на диске C:\nПомогает освободить место")

        # Турбо-оптимизация
        turbo_frame = ctk.CTkFrame(left_frame, corner_radius=12, fg_color="#1a1a2a")
        turbo_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(turbo_frame, text=lang.get("system_turbo_title"),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffaa00").pack(pady=5)

        self.turbo_btn = ctk.CTkButton(turbo_frame, text=lang.get("system_turbo_button"),
                                       fg_color="#d35400", command=self.turbo_optimize)
        self.turbo_btn.pack(pady=5, padx=20)
        add_tooltip(self.turbo_btn,
                    "⚡ Оптимизирует систему для максимальной производительности\nОтключает телеметрию, ускоряет меню")

        # Автозагрузка
        startup_frame = ctk.CTkFrame(left_frame, corner_radius=12, fg_color="#1a1a2a")
        startup_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(startup_frame, text=lang.get("system_startup_title"),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#ffaa00").pack(pady=5)

        self.startup_btn = ctk.CTkButton(startup_frame, text=lang.get("system_startup_button"),
                                         command=self.show_startup)
        self.startup_btn.pack(pady=5, padx=20)
        add_tooltip(self.startup_btn, "🚀 Показывает все программы\nкоторые запускаются вместе с Windows")

        # Сетевой сканер
        network_frame = ctk.CTkFrame(left_frame, corner_radius=12, fg_color="#1a1a2a")
        network_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(network_frame, text=lang.get("system_network_title"),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#00d4ff").pack(pady=5)

        self.network_btn = ctk.CTkButton(network_frame, text=lang.get("system_network_button"),
                                         fg_color="#e67e22", command=self.open_network_scanner)
        self.network_btn.pack(pady=5, padx=20)
        add_tooltip(self.network_btn, "🌐 Сканирует локальную сеть\nПоказывает все подключённые устройства")

        # === ПРАВАЯ КОЛОНКА ===
        # Батарея
        battery_frame = ctk.CTkFrame(right_frame, corner_radius=12, fg_color="#1a1a2a")
        battery_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(battery_frame, text=lang.get("system_battery_title"),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#00d4ff").pack(pady=5)

        self.battery_label = ctk.CTkLabel(battery_frame, text=lang.get("system_temp_loading"),
                                          font=ctk.CTkFont(size=12))
        self.battery_label.pack(pady=5)
        add_tooltip(self.battery_label, "🔋 Состояние аккумулятора\nЗаряд и оставшееся время работы")

        # Температура
        temp_frame = ctk.CTkFrame(right_frame, corner_radius=12, fg_color="#1a1a2a")
        temp_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(temp_frame, text=lang.get("system_temperature_title"),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#00d4ff").pack(pady=5)

        self.temp_label = ctk.CTkLabel(temp_frame, text=lang.get("system_temp_loading"),
                                       font=ctk.CTkFont(size=12))
        self.temp_label.pack(pady=5)
        add_tooltip(self.temp_label, "🌡️ Температура компонентов\nCPU, GPU и другие датчики")

        # Системная информация
        info_frame = ctk.CTkFrame(right_frame, corner_radius=12, fg_color="#1a1a2a")
        info_frame.pack(fill="both", expand=True, pady=10)
        ctk.CTkLabel(info_frame, text=lang.get("system_info_title"),
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#00d4ff").pack(pady=5)

        self.sys_info_text = ctk.CTkTextbox(info_frame, height=150, font=ctk.CTkFont(size=11), state="disabled")
        self.sys_info_text.pack(fill="both", expand=True, padx=10, pady=5)
        add_tooltip(self.sys_info_text, "💻 Детальная информация о процессоре,\nоперативной памяти и дисках")

    def refresh_texts(self):
        """Обновление текстов при смене языка"""
        # Пересоздаём виджеты для обновления текстов
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        self.update_system_info()
        self.update_battery_info()
        self.update_temperature()

    def open_network_scanner(self):
        from ui.pages.network_scan_page import NetworkScanPage
        dialog = ctk.CTkToplevel(self)
        dialog.title("NET GUARDIAN SCAN")
        dialog.geometry("750x600")
        dialog.transient(self)
        scanner = NetworkScanPage(dialog, self.app)
        scanner.pack(fill="both", expand=True)

    def clean_temp(self):
        def do_clean():
            targets = [os.environ.get('TEMP'), os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp')]
            files_deleted, size_freed = 0, 0
            for target in targets:
                if target and os.path.exists(target):
                    for root, dirs, files in os.walk(target):
                        for name in files:
                            try:
                                file_path = os.path.join(root, name)
                                size_freed += os.path.getsize(file_path)
                                os.remove(file_path)
                                files_deleted += 1
                            except:
                                pass
            msg = lang.get("system_clean_done").format(files=files_deleted, size=f"{size_freed / 1024 / 1024:.1f}")
            self.after(0, lambda: self.clean_status.configure(text=f"✅ {msg}", text_color="#00ff88"))

        self.clean_status.configure(text=f"⏳ {lang.get('system_clean_status')}", text_color="#ffaa00")
        threading.Thread(target=do_clean, daemon=True).start()

    def disk_analyzer(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(lang.get("system_disk_title"))
        dialog.geometry("750x550")
        dialog.transient(self)
        text_box = ctk.CTkTextbox(dialog, font=ctk.CTkFont(family="Consolas", size=10), state="disabled")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)
        text_box.configure(state="normal")
        text_box.insert("end", f"🔄 {lang.get('system_analyzing')}\n")
        text_box.configure(state="disabled")

        def analyze():
            file_list = []
            for root, dirs, files in os.walk("C:\\"):
                for name in files:
                    try:
                        file_path = os.path.join(root, name)
                        file_list.append((file_path, os.path.getsize(file_path)))
                    except:
                        continue
            file_list.sort(key=lambda x: x[1], reverse=True)
            result = "=" * 70 + f"\n{lang.get('system_top_files')}\n" + "=" * 70 + "\n\n"
            for i, (path, size) in enumerate(file_list[:20], 1):
                size_mb = size / (1024 * 1024)
                result += f"[{i:2d}] {size_mb:.1f} MB | {path}\n"
            text_box.configure(state="normal")
            text_box.delete("1.0", "end")
            text_box.insert("1.0", result)
            text_box.configure(state="disabled")

        threading.Thread(target=analyze, daemon=True).start()

    def turbo_optimize(self):
        """Показать диалог оптимизации"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("⚡ ТУРБО-ОПТИМИЗАЦИЯ")
        dialog.geometry("550x600")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Центрируем
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - 550) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 600) // 2
        dialog.geometry(f"+{x}+{y}")

        # Заголовок
        ctk.CTkLabel(dialog, text="⚡ ТУРБО-ОПТИМИЗАЦИЯ",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color="#ffaa00").pack(pady=15)

        ctk.CTkLabel(dialog, text="Выберите действия для ускорения системы:",
                     font=ctk.CTkFont(size=12)).pack(pady=5)

        # Фрейм с опциями
        options_frame = ctk.CTkFrame(dialog, fg_color="#1a1a2a", corner_radius=12)
        options_frame.pack(fill="x", padx=20, pady=10)

        # Переменные
        opt_telemetry = ctk.BooleanVar(value=True)
        opt_menu = ctk.BooleanVar(value=True)
        opt_prefetch = ctk.BooleanVar(value=False)
        opt_indexing = ctk.BooleanVar(value=False)

        # Опции
        opt1 = ctk.CTkCheckBox(options_frame, text="🛡️ Отключение телеметрии Windows",
                               variable=opt_telemetry, font=ctk.CTkFont(size=12))
        opt1.pack(anchor="w", padx=20, pady=5)

        opt2 = ctk.CTkCheckBox(options_frame, text="⚡ Ускорение меню (убрать задержку)",
                               variable=opt_menu, font=ctk.CTkFont(size=12))
        opt2.pack(anchor="w", padx=20, pady=5)

        opt3 = ctk.CTkCheckBox(options_frame, text="🧹 Очистка Prefetch (кэш программ)",
                               variable=opt_prefetch, font=ctk.CTkFont(size=12))
        opt3.pack(anchor="w", padx=20, pady=5)

        opt4 = ctk.CTkCheckBox(options_frame, text="📀 Отключение индексации дисков",
                               variable=opt_indexing, font=ctk.CTkFont(size=12))
        opt4.pack(anchor="w", padx=20, pady=5)

        # Фрейм для результатов (скроллируемый)
        result_frame = ctk.CTkFrame(dialog, fg_color="#1a1a2a", corner_radius=12)
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(result_frame, text="📋 РЕЗУЛЬТАТЫ:",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#00d4ff").pack(anchor="w", padx=15, pady=5)

        result_textbox = ctk.CTkTextbox(result_frame, font=ctk.CTkFont(family="Consolas", size=10),
                                        state="normal", height=120)
        result_textbox.pack(fill="both", expand=True, padx=15, pady=5)
        result_textbox.configure(state="disabled")

        # Кнопки
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)

        # Словарь для хранения исходного состояния кнопок
        original_states = {}

        def set_controls_state(state):
            """Включить/выключить все контролы"""
            opt1.configure(state=state)
            opt2.configure(state=state)
            opt3.configure(state=state)
            opt4.configure(state=state)
            if state == "normal":
                apply_btn.configure(state="normal")
                cancel_btn.configure(state="normal")
            else:
                apply_btn.configure(state="disabled")
                cancel_btn.configure(state="disabled")

        def add_result(text):
            """Добавить строку в результат"""
            result_textbox.configure(state="normal")
            result_textbox.insert("end", f"{text}\n")
            result_textbox.see("end")
            result_textbox.configure(state="disabled")

        def apply():
            set_controls_state("disabled")
            add_result("🔄 Применение оптимизаций...")

            def optimize():
                results = []

                if opt_telemetry.get():
                    try:
                        subprocess.run(["sc", "stop", "DiagTrack"], capture_output=True)
                        subprocess.run(["sc", "config", "DiagTrack", "start=", "disabled"], capture_output=True)
                        results.append("✅ Телеметрия отключена")
                    except:
                        results.append("❌ Телеметрия - ошибка")

                if opt_menu.get():
                    try:
                        subprocess.run(["reg", "add", "HKCU\\Control Panel\\Desktop", "/v", "MenuShowDelay",
                                        "/t", "REG_SZ", "/d", "0", "/f"], capture_output=True)
                        results.append("✅ Ускорение меню применено")
                    except:
                        results.append("❌ Ускорение меню - ошибка")

                if opt_prefetch.get():
                    try:
                        prefetch_path = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Prefetch')
                        if os.path.exists(prefetch_path):
                            count = 0
                            for f in os.listdir(prefetch_path):
                                try:
                                    os.remove(os.path.join(prefetch_path, f))
                                    count += 1
                                except:
                                    pass
                            if count > 0:
                                results.append(f"✅ Prefetch очищен ({count} файлов)")
                            else:
                                results.append("ℹ️ Prefetch уже пуст")
                        else:
                            results.append("ℹ️ Prefetch не найден")
                    except:
                        results.append("❌ Prefetch - ошибка")

                if opt_indexing.get():
                    try:
                        subprocess.run('net stop "Windows Search"', shell=True, capture_output=True)
                        subprocess.run('sc config "WSearch" start= disabled', shell=True, capture_output=True)
                        results.append("✅ Индексация отключена")
                    except:
                        results.append("❌ Индексация - ошибка")

                # Показываем результаты
                for r in results:
                    self.after(0, lambda res=r: add_result(res))

                self.after(0, lambda: add_result("\n✅ ОПТИМИЗАЦИЯ ЗАВЕРШЕНА"))
                self.after(0, lambda: set_controls_state("normal"))
                self.after(0, lambda: apply_btn.configure(text="✅ ГОТОВО", fg_color="#2ecc71"))

            threading.Thread(target=optimize, daemon=True).start()

        def cancel():
            dialog.destroy()

        apply_btn = ctk.CTkButton(btn_frame, text="🚀 ПРИМЕНИТЬ", fg_color="#d35400", command=apply, width=120)
        apply_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(btn_frame, text="❌ ОТМЕНА", fg_color="#2c3e66", command=cancel, width=120)
        cancel_btn.pack(side="left", padx=10)

        # Кнопка "Закрыть" появляется после оптимизации
        close_btn = ctk.CTkButton(btn_frame, text="📋 ЗАКРЫТЬ", fg_color="#2ecc71", command=dialog.destroy, width=120)

        # Не показываем сразу

        # Функция для показа кнопки закрытия после завершения
        def show_close_button():
            close_btn.pack(side="left", padx=10)
            apply_btn.configure(text="🚀 ПРИМЕНИТЬ", state="disabled")

        def check_and_show():
            """Проверяем, можно ли показать кнопку закрытия"""
            # Ждём пока apply_btn станет активным
            if apply_btn.cget("state") == "normal":
                show_close_button()
            else:
                dialog.after(500, check_and_show)

        # Запускаем проверку после завершения оптимизации
        def on_apply_complete():
            if apply_btn.cget("state") == "normal":
                show_close_button()
            else:
                dialog.after(500, on_apply_complete)

        # Сохраняем оригинальный callback
        original_apply = apply

        def new_apply():
            original_apply()
            dialog.after(100, check_and_show)

        apply_btn.configure(command=new_apply)


    def show_startup(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title(lang.get("system_startup_title"))
        dialog.geometry("800x400")
        text_box = ctk.CTkTextbox(dialog, font=ctk.CTkFont(family="Consolas", size=10), state="disabled")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)
        try:
            output = subprocess.check_output('wmic startup get caption,command', shell=True).decode('utf-8',
                                                                                                    errors='ignore')
            text_box.configure(state="normal")
            text_box.insert("end", output)
            text_box.configure(state="disabled")
        except Exception as e:
            text_box.configure(state="normal")
            text_box.insert("end", f"Error: {e}")
            text_box.configure(state="disabled")

    def update_system_info(self):
        cpu_percent = psutil.cpu_percent()
        ram = psutil.virtual_memory()

        # Переводим названия в зависимости от языка
        cpu_text = "CPU" if lang.get_lang() == "en" else "ПРОЦЕССОР"
        ram_text = "RAM" if lang.get_lang() == "en" else "ОПЕРАТИВНАЯ ПАМЯТЬ"
        disk_text = "DISKS" if lang.get_lang() == "en" else "ДИСКИ"
        free_text = "free" if lang.get_lang() == "en" else "свободно"
        used_text = "used" if lang.get_lang() == "en" else "заполнено"

        info = f"📊 {cpu_text}: {cpu_percent}%\n"
        info += f"💾 {ram_text}: {ram.percent}% ({ram.used / (1024 ** 3):.1f} GB / {ram.total / (1024 ** 3):.1f} GB)\n"
        info += f"🗄️ {disk_text}:\n"

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                info += f"   • {partition.device}: {usage.percent}% {used_text}\n"
            except:
                pass

        self.sys_info_text.configure(state="normal")
        self.sys_info_text.delete("1.0", "end")
        self.sys_info_text.insert("1.0", info)
        self.sys_info_text.configure(state="disabled")
        self.after(5000, self.update_system_info)

    def update_battery_info(self):
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            status = lang.get("system_battery_charging") if battery.power_plugged else lang.get(
                "system_battery_discharging")
            color = "#00ff88" if percent > 50 else ("#ffaa00" if percent > 20 else "#ff6666")
            text = f"{status}\n{percent}%"
            if not battery.power_plugged and battery.secsleft != psutil.POWER_TIME_UNKNOWN and battery.secsleft < 864000:
                hours = battery.secsleft // 3600
                mins = (battery.secsleft % 3600) // 60
                time_text = "left" if lang.get_lang() == "en" else "осталось"
                text += f"\n{time_text}: {hours}h {mins}m"
            self.battery_label.configure(text=text, text_color=color)
        else:
            self.battery_label.configure(text=f"❌ {lang.get('system_battery_not_found')}", text_color="#ff6666")
        self.after(30000, self.update_battery_info)

    def update_temperature(self):
        temps = []
        try:
            sensors = psutil.sensors_temperatures()
            if sensors:
                for name, entries in sensors.items():
                    for entry in entries:
                        if entry.current:
                            temps.append(f"{name}: {entry.current:.1f}°C")
        except:
            pass
        if temps:
            self.temp_label.configure(text="\n".join(temps), text_color="#00ff88")
        else:
            self.temp_label.configure(text=f"🌡️ {lang.get('system_temp_not_found')}", text_color="#ffaa00")
        self.after(30000, self.update_temperature)

    def show_message(self, message):
        label = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=11),
                             fg_color="#2c3e66", corner_radius=8, padx=15, pady=8)
        label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(3000, label.destroy)