import os
import time
import subprocess
import tempfile
import psutil
import logging


# Запрещённые модули (для безопасности)
FORBIDDEN_MODULES = {"fs", "child_process", "os", "process", "path", "net", "http"}
MAX_OUTPUT_LENGTH = 5000  # Лимит на вывод

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def truncate_output(output):
    """Ограничивает размер вывода"""
    if len(output) > MAX_OUTPUT_LENGTH:
        return output[:MAX_OUTPUT_LENGTH] + "\n[Вывод обрезан...]"
    return output


def check_code_safety(source_code):
    """Проверяет код на запрещённые конструкции"""
    if any(module in source_code for module in FORBIDDEN_MODULES):
        return "Ошибка: использование запрещённых модулей!"
    if "require(" in source_code or "import " in source_code:
        return "Ошибка: использование `require()` и `import` запрещено!"
    if "eval(" in source_code:
        return "Ошибка: использование `eval()` запрещено!"
    return None
