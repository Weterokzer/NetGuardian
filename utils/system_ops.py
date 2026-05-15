import ctypes
import logging
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path


logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    ok: bool
    message: str
    stdout: str = ""
    stderr: str = ""
    returncode: int | None = None


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def run_command(args, timeout=10, admin_required=False):
    if admin_required and not is_admin():
        return CommandResult(False, "Нужен запуск от имени администратора")

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
            encoding="utf-8",
            errors="ignore",
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        ok = result.returncode == 0
        message = stdout or stderr or ("Готово" if ok else f"Команда завершилась с кодом {result.returncode}")
        if not ok:
            logger.warning("Command failed: %s | %s", args, message)
        return CommandResult(ok, message, stdout, stderr, result.returncode)
    except subprocess.TimeoutExpired:
        logger.warning("Command timed out: %s", args)
        return CommandResult(False, "Операция заняла слишком много времени")
    except Exception as exc:
        logger.exception("Command error: %s", args)
        return CommandResult(False, str(exc))


def clean_temp_files(min_age_seconds=3600):
    targets = [
        Path(os.environ.get("TEMP", "")),
        Path(os.environ.get("TMP", "")),
    ]
    system_temp = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "Temp"
    if is_admin():
        targets.append(system_temp)

    now = time.time()
    cleaned = 0
    skipped = 0
    failed = 0
    freed = 0
    seen = set()

    for target in targets:
        try:
            target = target.resolve()
        except Exception:
            continue

        if target in seen or not target.exists() or not target.is_dir():
            continue
        seen.add(target)

        for item in target.iterdir():
            try:
                age = now - item.stat().st_mtime
                if age < min_age_seconds:
                    skipped += 1
                    continue

                if item.is_file() or item.is_symlink():
                    freed += item.stat().st_size
                    item.unlink()
                elif item.is_dir():
                    freed += sum(p.stat().st_size for p in item.rglob("*") if p.is_file())
                    shutil.rmtree(item)
                cleaned += 1
            except Exception:
                failed += 1
                logger.debug("Failed to remove temp item: %s", item, exc_info=True)

    mb = freed / 1024 / 1024
    message = f"Удалено: {cleaned}, пропущено свежих: {skipped}, ошибок: {failed}, освобождено: {mb:.1f} MB"
    logger.info("Temp cleanup: %s", message)
    return cleaned, skipped, failed, mb, message
