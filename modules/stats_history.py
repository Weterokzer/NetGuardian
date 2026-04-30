from collections import deque
from datetime import datetime


class StatsHistory:
    """История тестов скорости"""

    def __init__(self, max_size=20):
        self.history = deque(maxlen=max_size)

    def add_test(self, download, upload, ping):
        """Добавление результата теста"""
        self.history.appendleft({
            "timestamp": datetime.now().strftime("%H:%M %d.%m"),
            "download": round(download, 1),
            "upload": round(upload, 1),
            "ping": round(ping, 0)
        })

    def get_history(self):
        """Получение всей истории"""
        return list(self.history)

    def get_stats(self):
        """Получение статистики"""
        if not self.history:
            return None

        downloads = [h['download'] for h in self.history]
        uploads = [h['upload'] for h in self.history]
        pings = [h['ping'] for h in self.history]

        return {
            'max_download': max(downloads),
            'min_download': min(downloads),
            'avg_download': sum(downloads) / len(downloads),
            'max_upload': max(uploads),
            'min_upload': min(uploads),
            'avg_upload': sum(uploads) / len(uploads),
            'avg_ping': sum(pings) / len(pings),
            'min_ping': min(pings),
            'max_ping': max(pings),
            'total_tests': len(self.history)
        }

    def clear(self):
        """Очистка истории"""
        self.history.clear()

    def export_to_dict(self):
        """Экспорт в словарь (для сохранения)"""
        return list(self.history)