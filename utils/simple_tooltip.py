import tkinter as tk


class SimpleToolTip:
    """Простая подсказка через стандартный tkinter (без лишних окон)"""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.after_id = None
        self.widget.bind('<Enter>', self.schedule_tip, add="+")
        self.widget.bind('<Leave>', self.hide_tip, add="+")

    def schedule_tip(self, event=None):
        self.cancel_scheduled_tip()
        self.after_id = self.widget.after(350, self.show_tip)

    def cancel_scheduled_tip(self):
        if self.after_id:
            try:
                self.widget.after_cancel(self.after_id)
            except tk.TclError:
                pass
            self.after_id = None

    def show_tip(self, event=None):
        self.after_id = None
        if self.tip_window:
            return

        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 12
        y = self.widget.winfo_rooty() + max(0, (self.widget.winfo_height() - 24) // 2)

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_attributes("-topmost", True)
        self.tip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tip_window,
            text=self.text,
            background="#1a1a2a",
            foreground="#00d4ff",
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=4,
            font=("Consolas", 9)
        )
        label.pack()

    def hide_tip(self, event=None):
        self.cancel_scheduled_tip()
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


def add_tooltip(widget, text):
    return SimpleToolTip(widget, text)
