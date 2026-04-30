import threading

try:
    import speedtest

    SPEEDTEST_AVAILABLE = True
except ImportError:
    SPEEDTEST_AVAILABLE = False


class SpeedtestEngine:
    """Выполнение тестов скорости"""

    def __init__(self):
        self.is_testing = False
        self.last_result = None

    def run_test(self, callback):
        """Запуск теста скорости"""
        if not SPEEDTEST_AVAILABLE:
            if callback:
                callback(None, error="Speedtest не установлен. Установите: pip install speedtest-cli")
            return

        if self.is_testing:
            return

        self.is_testing = True

        def test():
            try:
                st = speedtest.Speedtest()
                st.get_best_server()

                # Измеряем загрузку
                if callback:
                    callback(None, progress="📥 Измеряем загрузку...")
                download = st.download() / 1_000_000

                # Измеряем отдачу
                if callback:
                    callback(None, progress="📤 Измеряем отдачу...")
                upload = st.upload() / 1_000_000

                ping = st.results.ping

                result = {
                    'download': round(download, 1),
                    'upload': round(upload, 1),
                    'ping': round(ping, 0)
                }
                self.last_result = result

                if callback:
                    callback(result)

            except Exception as e:
                if callback:
                    callback(None, error=str(e))
            finally:
                self.is_testing = False

        threading.Thread(target=test, daemon=True).start()

    def get_last_result(self):
        return self.last_result

    def is_available(self):
        return SPEEDTEST_AVAILABLE