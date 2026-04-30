import threading
import time
from concurrent.futures import ThreadPoolExecutor


class BackgroundWorker:
    """Очередь задач с пулом потоков"""

    def __init__(self, max_workers=3):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.tasks = {}
        self._running = True
        self.lock = threading.Lock()

    def submit(self, key, func, callback=None, *args, **kwargs):
        future = self.executor.submit(func, *args, **kwargs)
        with self.lock:
            self.tasks[key] = (future, callback)

        # Запускаем проверку в отдельном потоке
        threading.Thread(target=self._check_tasks, daemon=True).start()
        return future

    def _check_tasks(self):
        time.sleep(0.1)  # Небольшая задержка
        with self.lock:
            for key, (future, callback) in list(self.tasks.items()):
                if future.done():
                    try:
                        result = future.result()
                        if callback:
                            callback(result)
                    except Exception as e:
                        if callback:
                            callback(None, error=str(e))
                    del self.tasks[key]

    def shutdown(self):
        self._running = False
        self.executor.shutdown(wait=False)