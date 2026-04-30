import customtkinter as ctk
import psutil
import threading
import time
from collections import deque

try:
    import matplotlib

    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import speedtest

    SPEEDTEST_AVAILABLE = True
except ImportError:
    SPEEDTEST_AVAILABLE = False


class SpeedPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.current_speed = 0
        self.last_net_io = None
        self.last_time = 0

        self.download_history = deque(maxlen=60)
        self.upload_history = deque(maxlen=60)
        self.time_history = deque(maxlen=60)
        self.counter = 0

        self.create_widgets()
        self.start_monitoring()

    def create_widgets(self):
        # Заголовок
        header = ctk.CTkFrame(self, corner_radius=15, fg_color="#1a1a2a")
        header.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(header, text="📡", font=ctk.CTkFont(size=38)).pack(pady=(15, 5))
        ctk.CTkLabel(header, text="NET GUARDIAN",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color="#00d4ff").pack()
        ctk.CTkLabel(header, text="SPEEDOMETER",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#666").pack(pady=(0, 15))

        # Основной контейнер
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        left_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=10)

        right_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        right_panel.pack(side="right", fill="both", expand=True, padx=10)

        # Левая панель
        center = ctk.CTkFrame(left_panel, fg_color="transparent")
        center.pack(expand=True)

        self.speed_label = ctk.CTkLabel(center, text="0.0",
                                        font=ctk.CTkFont(size=72, weight="bold"),
                                        text_color="#00ff88")
        self.speed_label.pack(pady=20)

        ctk.CTkLabel(center, text="Mbps", font=ctk.CTkFont(size=20), text_color="#888").pack()

        self.progress_bar = ctk.CTkProgressBar(center, width=350, height=12, fg_color="#2a2a3a")
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)

        traffic_frame = ctk.CTkFrame(center, fg_color="#1a1a2a", corner_radius=10)
        traffic_frame.pack(pady=15)

        self.down_label = ctk.CTkLabel(traffic_frame, text="📥 ЗАГРУЗКА: 0 Mbps",
                                       font=ctk.CTkFont(size=13, weight="bold"),
                                       text_color="#00ff88")
        self.down_label.pack(side="left", padx=30, pady=12)

        self.up_label = ctk.CTkLabel(traffic_frame, text="📤 ОТДАЧА: 0 Mbps",
                                     font=ctk.CTkFont(size=13, weight="bold"),
                                     text_color="#ffaa00")
        self.up_label.pack(side="left", padx=30, pady=12)

        self.test_btn = ctk.CTkButton(center, text="⚡ ЗАПУСТИТЬ SPEEDTEST ⚡",
                                      fg_color="#d35400", hover_color="#e67e22",
                                      height=45, width=300,
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      corner_radius=12,
                                      command=self.run_speedtest)
        self.test_btn.pack(pady=20)

        self.result_text = ctk.CTkTextbox(center, width=400, height=120,
                                          font=ctk.CTkFont(family="Consolas", size=10),
                                          state="disabled")
        self.result_text.pack(pady=10)

        # Правая панель (графики)
        if MATPLOTLIB_AVAILABLE:
            self.figure = Figure(figsize=(6, 6), facecolor='#1a1a2a', dpi=80)

            self.ax1 = self.figure.add_subplot(211)
            self.ax1.set_facecolor('#0f0f1a')
            self.ax1.set_title('ЗАГРУЗКА (DOWNLOAD)', color='#00ff88', fontsize=11, fontweight='bold')
            self.ax1.set_xlabel('ВРЕМЯ (СЕК)', color='#888')
            self.ax1.set_ylabel('Mbps', color='#888')
            self.ax1.tick_params(colors='#888')
            self.ax1.grid(True, alpha=0.3, color='#444')
            self.download_line, = self.ax1.plot([], [], 'g-', linewidth=2, color='#00ff88')
            self.ax1.set_ylim(0, 1000)

            self.ax2 = self.figure.add_subplot(212)
            self.ax2.set_facecolor('#0f0f1a')
            self.ax2.set_title('ОТДАЧА (UPLOAD)', color='#ffaa00', fontsize=11, fontweight='bold')
            self.ax2.set_xlabel('ВРЕМЯ (СЕК)', color='#888')
            self.ax2.set_ylabel('Mbps', color='#888')
            self.ax2.tick_params(colors='#888')
            self.ax2.grid(True, alpha=0.3, color='#444')
            self.upload_line, = self.ax2.plot([], [], 'y-', linewidth=2, color='#ffaa00')
            self.ax2.set_ylim(0, 1000)

            self.figure.tight_layout(pad=2.0)

            self.canvas = FigureCanvasTkAgg(self.figure, right_panel)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)

            graph_controls = ctk.CTkFrame(right_panel, fg_color="transparent")
            graph_controls.pack(pady=5)

            ctk.CTkButton(graph_controls, text="📊 ОЧИСТИТЬ ГРАФИК", width=130,
                          command=self.clear_graphs,
                          fg_color="#d35400", corner_radius=8).pack(side="left", padx=5)

            ctk.CTkButton(graph_controls, text="🔄 СБРОСИТЬ МАСШТАБ", width=130,
                          command=self.reset_graph_scale,
                          fg_color="#d35400", corner_radius=8).pack(side="left", padx=5)
        else:
            no_graph_frame = ctk.CTkFrame(right_panel, fg_color="#1a1a2a", corner_radius=10)
            no_graph_frame.pack(fill="both", expand=True)
            ctk.CTkLabel(no_graph_frame, text="📊 ГРАФИКИ НЕДОСТУПНЫ",
                         font=ctk.CTkFont(size=16, weight="bold")).pack(pady=30)
            ctk.CTkLabel(no_graph_frame, text="Установите matplotlib:\npip install matplotlib",
                         font=ctk.CTkFont(size=12), text_color="#ffaa00").pack()

    def start_monitoring(self):
        self.after(500, self.update_speed)

    def update_speed(self):
        try:
            net_io = psutil.net_io_counters()
            current_time = time.time()

            if self.last_net_io is not None:
                time_diff = current_time - self.last_time
                if time_diff > 0:
                    down = (net_io.bytes_recv - self.last_net_io.bytes_recv) * 8 / 1024 / 1024 / time_diff
                    up = (net_io.bytes_sent - self.last_net_io.bytes_sent) * 8 / 1024 / 1024 / time_diff

                    down = min(down, 1000)
                    up = min(up, 1000)

                    self.speed_label.configure(text=f"{down:.1f}")
                    self.progress_bar.set(min(down / 100, 1.0))
                    self.down_label.configure(text=f"📥 ЗАГРУЗКА: {down:.1f} Mbps")
                    self.up_label.configure(text=f"📤 ОТДАЧА: {up:.1f} Mbps")

                    self.download_history.append(down)
                    self.upload_history.append(up)
                    self.time_history.append(self.counter)
                    self.counter += 1

                    self.update_graphs()
                    self.app.update_tray_speed(down)

            self.last_net_io = net_io
            self.last_time = current_time
        except:
            pass

        self.after(500, self.update_speed)

    def update_graphs(self):
        if not MATPLOTLIB_AVAILABLE or len(self.time_history) == 0:
            return

        times = list(self.time_history)
        downloads = list(self.download_history)
        uploads = list(self.upload_history)

        self.download_line.set_data(times, downloads)
        self.ax1.set_xlim(max(0, times[-1] - 60), max(60, times[-1]))

        if downloads:
            max_down = max(downloads)
            self.ax1.set_ylim(0, max(50, max_down * 1.2))

        self.upload_line.set_data(times, uploads)
        self.ax2.set_xlim(max(0, times[-1] - 60), max(60, times[-1]))

        if uploads:
            max_up = max(uploads)
            self.ax2.set_ylim(0, max(50, max_up * 1.2))

        self.canvas.draw_idle()

    def clear_graphs(self):
        self.download_history.clear()
        self.upload_history.clear()
        self.time_history.clear()
        self.counter = 0

        if MATPLOTLIB_AVAILABLE:
            self.download_line.set_data([], [])
            self.upload_line.set_data([], [])
            self.ax1.set_ylim(0, 1000)
            self.ax2.set_ylim(0, 1000)
            self.canvas.draw_idle()

        self.show_message("📊 Графики очищены")

    def reset_graph_scale(self):
        if MATPLOTLIB_AVAILABLE and len(self.download_history) > 0:
            max_down = max(self.download_history)
            max_up = max(self.upload_history)
            self.ax1.set_ylim(0, max(50, max_down * 1.2))
            self.ax2.set_ylim(0, max(50, max_up * 1.2))
            self.canvas.draw_idle()
            self.show_message("📊 Масштаб сброшен")

    def run_speedtest(self):
        if not SPEEDTEST_AVAILABLE:
            self.show_result("❌ Speedtest не установлен\npip install speedtest-cli")
            return

        self.test_btn.configure(state="disabled", text="⏳ ТЕСТИРУЕМ...")
        self.show_result("📡 ЗАПУСК ТЕСТА СКОРОСТИ...\n")
        threading.Thread(target=self.speedtest_thread, daemon=True).start()

    def speedtest_thread(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()

            self.after(0, lambda: self.show_result("📥 ИЗМЕРЯЕМ ЗАГРУЗКУ...\n"))
            download = st.download() / 1_000_000

            self.after(0, lambda: self.show_result("📤 ИЗМЕРЯЕМ ОТДАЧУ...\n"))
            upload = st.upload() / 1_000_000

            ping = st.results.ping

            result = f"\n✅ РЕЗУЛЬТАТЫ:\n📥 ЗАГРУЗКА: {download:.1f} Mbps\n📤 ОТДАЧА: {upload:.1f} Mbps\n🏓 ПИНГ: {ping:.0f} ms"
            self.after(0, lambda: self.show_result(result))

            if hasattr(self.app, 'pages') and 'stats' in self.app.pages:
                stats_page = self.app.pages['stats']
                if hasattr(stats_page, 'add_test_result'):
                    stats_page.add_test_result(download, upload, ping)

        except Exception as e:
            self.after(0, lambda: self.show_result(f"❌ ОШИБКА: {str(e)[:100]}"))
        finally:
            self.after(0, lambda: self.test_btn.configure(state="normal", text="⚡ ЗАПУСТИТЬ SPEEDTEST ⚡"))

    def show_result(self, text):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")

    def show_message(self, message):
        label = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=11),
                             fg_color="#2c3e66", corner_radius=8, padx=15, pady=8)
        label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(2000, label.destroy)