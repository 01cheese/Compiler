import os
import time
import subprocess
import tempfile
import psutil
import logging

# Запрещённые модули (для безопасности)
FORBIDDEN_MODULES = {"os", "sys", "shutil", "subprocess", "pathlib", "socket", "threading"}
MAX_OUTPUT_LENGTH = 150000  # Лимит на вывод

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def truncate_output(output):
    """Ограничивает размер вывода"""
    if len(output) > MAX_OUTPUT_LENGTH:
        return output[:MAX_OUTPUT_LENGTH] + "\n[Вывод обрезан...]"
    return output

def check_code_safety(source_code):
    """Проверяет, есть ли запрещённые конструкции"""
    if any(module in source_code for module in FORBIDDEN_MODULES):
        return "Ошибка: использование запрещённых модулей!"
    if "eval(" in source_code or "exec(" in source_code:
        return "Ошибка: использование eval() и exec() запрещено!"
    return None

def run_py(request):
    """Запускает Python-код и обрабатывает ошибки"""
    source_code = request["source_code"]
    stdin = request["stdin"]

    safety_error = check_code_safety(source_code)
    if safety_error:
        return {"output": safety_error, "status": "failed", "memory": "N/A", "time": "0 sec"}

    # Создаём временный файл в папке проекта
    temp_dir = "../timeFiles"
    os.makedirs(temp_dir, exist_ok=True)

    # Создаём файл
    fd, temp_file_name = tempfile.mkstemp(suffix=".py", dir=temp_dir)
    os.close(fd)  # Закрываем файловый дескриптор

    try:
        with open(temp_file_name, "w", encoding="utf-8") as temp_file:
            temp_file.write(source_code)

        run_cmd = ["python", temp_file_name]
        start_time = time.time()

        process = subprocess.run(
            run_cmd,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=5
        )

        execution_time = time.time() - start_time
        memory_used = psutil.Process(os.getpid()).memory_info().rss / 1024

        # Удаляем файл после выполнения
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)

        if process.returncode != 0:
            logging.error(f"Ошибка выполнения: {process.stderr.strip()}")
            return {
                "output": truncate_output(process.stderr.strip()),
                "status": "failed",
                "memory": f"{memory_used:.2f} KB",
                "time": f"{execution_time:.3f} sec"
            }

        return {
            "output": truncate_output(process.stdout.strip()),
            "status": "finished",
            "memory": f"{memory_used:.2f} KB",
            "time": f"{execution_time:.3f} sec"
        }

    except subprocess.TimeoutExpired:
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
        return {
            "output": "Ошибка: выполнение кода превысило лимит времени!",
            "status": "failed",
            "memory": "N/A",
            "time": "5 sec"
        }

    except Exception as e:
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
        return {
            "output": f"Ошибка выполнения: {str(e)}",
            "status": "failed",
            "memory": "N/A",
            "time": "0 sec"
        }
