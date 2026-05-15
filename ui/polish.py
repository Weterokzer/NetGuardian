import customtkinter as ctk


COLORS = {
    "app_bg": "#0b0f14",
    "surface": "#111827",
    "surface_soft": "#151a2a",
    "surface_deep": "#090d18",
    "border": "#24324c",
    "border_soft": "#1d2940",
    "text": "#eef6ff",
    "muted": "#8a95a8",
    "cyan": "#00d4ff",
    "blue": "#1f5b98",
    "blue_hover": "#2b6fb6",
    "orange": "#e66a00",
    "orange_hover": "#f27a18",
    "red": "#e74c3c",
    "green": "#20c979",
}


def safe_configure(widget, **kwargs):
    try:
        widget.configure(**kwargs)
    except Exception:
        pass


def normalize_color(value):
    if isinstance(value, (list, tuple)):
        return value[-1] if value else None
    return value


def polish_widget_tree(widget):
    for child in widget.winfo_children():
        cls_name = child.__class__.__name__

        if cls_name in {"CTkFrame", "CTkScrollableFrame"}:
            try:
                fg = normalize_color(child.cget("fg_color"))
            except Exception:
                fg = None

            if fg not in {"transparent", COLORS["app_bg"]}:
                safe_configure(
                    child,
                    fg_color=COLORS["surface_soft"],
                    border_width=1,
                    border_color=COLORS["border_soft"],
                    corner_radius=10,
                )

        elif cls_name == "CTkTextbox":
            safe_configure(
                child,
                fg_color=COLORS["surface_deep"],
                text_color=COLORS["text"],
                border_width=1,
                border_color=COLORS["border"],
                corner_radius=8,
                scrollbar_button_color=COLORS["border"],
                scrollbar_button_hover_color=COLORS["blue"],
            )

        elif cls_name == "CTkEntry":
            safe_configure(
                child,
                fg_color=COLORS["surface_deep"],
                text_color=COLORS["text"],
                placeholder_text_color=COLORS["muted"],
                border_width=1,
                border_color=COLORS["border"],
                corner_radius=7,
            )

        elif cls_name == "CTkButton":
            try:
                current = normalize_color(child.cget("fg_color"))
            except Exception:
                current = None

            color = current
            hover = None
            if current in {"#d35400", "#e67e22"}:
                color = COLORS["orange"]
                hover = COLORS["orange_hover"]
            elif current in {"#2c3e66", "#1a2a3a"}:
                color = COLORS["blue"]
                hover = COLORS["blue_hover"]

            kwargs = {
                "corner_radius": 7,
                "border_width": 0,
            }
            if color:
                kwargs["fg_color"] = color
            if hover:
                kwargs["hover_color"] = hover
            safe_configure(child, **kwargs)

        elif cls_name == "CTkOptionMenu":
            safe_configure(
                child,
                fg_color=COLORS["blue"],
                button_color="#184a79",
                button_hover_color=COLORS["blue_hover"],
                dropdown_fg_color=COLORS["surface_deep"],
                dropdown_hover_color=COLORS["blue"],
                dropdown_text_color=COLORS["text"],
                text_color=COLORS["text"],
                corner_radius=7,
            )

        elif cls_name == "CTkSwitch":
            safe_configure(
                child,
                progress_color=COLORS["cyan"],
                button_color="#d6dde8",
                button_hover_color="#ffffff",
                text_color=COLORS["text"],
            )

        elif cls_name == "CTkLabel":
            try:
                text_color = normalize_color(child.cget("text_color"))
            except Exception:
                text_color = None
            if text_color in {"#666", "#888", "#999"}:
                safe_configure(child, text_color=COLORS["muted"])

        polish_widget_tree(child)
