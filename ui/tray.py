import threading
import os
import sys

try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont

    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False


class SystemTray:
    """Системный трей для приложения"""

    def __init__(self, app):
        self.app = app
        self.icon = None
        self.current_speed = 0
        self.running = False
        self.thread = None

        if not TRAY_AVAILABLE:
            print("pystray не установлен. Установите: pip install pystray pillow")

    def create_icon_image(self, speed=None):
        """Создание иконки с отображением скорости"""
        size = 64
        image = Image.new('RGB', (size, size), color='#0f0f1a')
        draw = ImageDraw.Draw(image)

        # Рисуем круг
        draw.ellipse((8, 8, 56, 56), fill='#00d4ff')
        draw.ellipse((12, 12, 52, 52), fill='#0f0f1a')

        # Текст "🛡"
        try:
            # Пытаемся использовать emoji
            draw.text((22, 18), "🛡", fill='#00d4ff')
        except:
            # Если emoji не поддерживается
            draw.rectangle((20, 20, 44, 44), fill='#00d4ff')

        # Если есть скорость, показываем её маленькими цифрами
        if speed and speed > 0:
            try:
                font = ImageFont.truetype("arial.ttf", 14)
                speed_text = f"{int(speed)}"
                draw.text((8, 48), speed_text, fill='#00ff88', font=font)
            except:
                pass

        return image

    def setup(self):
        """Настройка иконки в трее"""
        if not TRAY_AVAILABLE:
            return False

        # Создаём меню
        menu = pystray.Menu(
            pystray.MenuItem("📡 Показать окно", self.show_window),
            pystray.MenuItem("🔍 Быстрый тест скорости", self.run_speedtest),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("🚪 Выход", self.exit_app)
        )

        # Создаём иконку
        self.icon = pystray.Icon(
            "netguardian",
            self.create_icon_image(),
            "🛡️ NET GUARDIAN",
            menu
        )
        return True

    def run(self):
        """Запуск трея в отдельном потоке"""
        if not TRAY_AVAILABLE or not self.icon:
            return

        self.running = True
        self.icon.run()

    def stop(self):
        """Остановка трея"""
        self.running = False
        if self.icon:
            self.icon.stop()

    def show_window(self):
        """Показать главное окно"""
        if self.app.main_window:
            self.app.main_window.deiconify()
            self.app.main_window.lift()
            self.app.main_window.focus_force()

    def hide_window(self):
        """Скрыть главное окно"""
        if self.app.main_window:
            self.app.main_window.withdraw()

    def run_speedtest(self):
        """Запуск speedtest из трея"""
        if hasattr(self.app, 'pages') and 'speed' in self.app.pages:
            speed_page = self.app.pages['speed']
            if hasattr(speed_page, 'run_speedtest'):
                # Показываем окно
                self.show_window()
                # Запускаем тест с небольшой задержкой
                self.app.main_window.after(500, speed_page.run_speedtest)

    def exit_app(self):
        """Выход из приложения"""
        self.stop()
        self.app.quit()

    def update_speed(self, speed_mbps):
        """Обновление скорости в иконке трея"""
        self.current_speed = speed_mbps
        if self.icon:
            # Обновляем иконку с новой скоростью
            self.icon.icon = self.create_icon_image(speed_mbps)
            # Обновляем подсказку
            self.icon.title = f"🛡️ NET GUARDIAN\nСкорость: {speed_mbps:.1f} Mbps"