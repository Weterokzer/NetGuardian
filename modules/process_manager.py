import psutil
import threading


class ProcessManager:
    """Управление системными процессами"""

    def __init__(self):
        self.process_cache = []
        self.cache_time = 0

    def get_processes(self, limit=80, sort_by='memory'):
        """Получение списка процессов"""
        processes = []
        try:
            for proc in psutil.process_iter(['name', 'pid', 'memory_percent', 'cpu_percent']):
                try:
                    info = proc.info
                    if info['name']:
                        processes.append({
                            'name': info['name'],
                            'pid': info['pid'],
                            'memory': info['memory_percent'] or 0,
                            'cpu': proc.cpu_percent(interval=0.1)
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Сортировка
            if sort_by == 'memory':
                processes.sort(key=lambda x: x['memory'], reverse=True)
            else:
                processes.sort(key=lambda x: x['cpu'], reverse=True)

            return processes[:limit]
        except Exception as e:
            return []

    def kill_process(self, pid):
        """Завершение процесса"""
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            proc.terminate()
            # Ждём завершения
            import time
            time.sleep(1)
            if proc.is_running():
                proc.kill()
            return True, name
        except psutil.NoSuchProcess:
            return True, "Процесс уже завершён"
        except Exception as e:
            return False, str(e)

    def get_process_info(self, pid):
        """Информация о конкретном процессе"""
        try:
            proc = psutil.Process(pid)
            return {
                'name': proc.name(),
                'pid': pid,
                'memory': proc.memory_percent(),
                'cpu': proc.cpu_percent(),
                'status': proc.status(),
                'create_time': proc.create_time()
            }
        except:
            return None