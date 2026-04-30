import psutil
import time


class NetworkMonitor:
    """Мониторинг сетевой активности"""

    def __init__(self):
        self.last_net_io = None
        self.last_time = 0
        self.current_down = 0
        self.current_up = 0

    def update(self):
        """Обновление показателей скорости"""
        try:
            net_io = psutil.net_io_counters()
            current_time = time.time()

            if self.last_net_io is not None:
                time_diff = current_time - self.last_time
                if time_diff > 0:
                    self.current_down = (net_io.bytes_recv - self.last_net_io.bytes_recv) * 8 / 1024 / 1024 / time_diff
                    self.current_up = (net_io.bytes_sent - self.last_net_io.bytes_sent) * 8 / 1024 / 1024 / time_diff

                    # Ограничиваем значения
                    self.current_down = max(0, min(self.current_down, 1000))
                    self.current_up = max(0, min(self.current_up, 1000))

            self.last_net_io = net_io
            self.last_time = current_time

            return self.current_down, self.current_up
        except:
            return 0, 0

    def get_speed(self):
        """Получение текущей скорости"""
        return self.current_down, self.current_up

    def get_total_traffic(self):
        """Получение общего трафика"""
        try:
            net_io = psutil.net_io_counters()
            down_mb = net_io.bytes_recv / 1024 / 1024
            up_mb = net_io.bytes_sent / 1024 / 1024
            return down_mb, up_mb
        except:
            return 0, 0