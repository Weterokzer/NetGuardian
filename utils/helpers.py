from datetime import datetime

def format_bytes(bytes):
    """Форматирование байтов в читаемый вид"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.1f} PB"

def get_timestamp(format_str="%H:%M:%S"):
    """Получение текущей метки времени"""
    return datetime.now().strftime(format_str)

def truncate_string(text, max_length=50):
    """Обрезка строки до нужной длины"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def is_admin():
    """Проверка прав администратора (Windows)"""
    import ctypes
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False