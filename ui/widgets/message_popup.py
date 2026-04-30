import customtkinter as ctk


class MessagePopup:
    """Всплывающие сообщения"""

    @staticmethod
    def show(parent, message, duration=3000, type="info"):
        """Показать всплывающее сообщение"""
        colors = {
            "info": "#2c3e66",
            "success": "#2ecc71",
            "error": "#e74c3c",
            "warning": "#f39c12"
        }

        label = ctk.CTkLabel(parent, text=message, font=ctk.CTkFont(size=12),
                             fg_color=colors.get(type, "#2c3e66"),
                             corner_radius=10, padx=20, pady=10)
        label.place(relx=0.5, rely=0.95, anchor="center")
        parent.after(duration, label.destroy)