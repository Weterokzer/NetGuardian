#!/usr/bin/env python3
"""
NetGuardian Ultimate - Защитник сети
Модульная архитектура
"""

import sys
import os

# Добавляем текущую папку в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.app import NetGuardianApp

if __name__ == "__main__":
    app = NetGuardianApp()

    # Устанавливаем иконку окна (если файл существует)
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    if os.path.exists(icon_path):
        try:
            app.main_window.iconbitmap(icon_path)
        except:
            pass

    app.run()