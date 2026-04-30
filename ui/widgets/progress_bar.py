import customtkinter as ctk


class GradientProgressBar(ctk.CTkProgressBar):
    """Прогресс-бар с градиентными цветами"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.last_value = 0

    def set_with_color(self, value):
        """Установка значения с автоматическим выбором цвета"""
        self.set(value)

        if value < 0.3:
            self.configure(progress_color="#00ff88")
        elif value < 0.7:
            self.configure(progress_color="#ffaa00")
        else:
            self.configure(progress_color="#ff3366")