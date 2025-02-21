import os
import time
import subprocess
import tempfile
import psutil
import logging

# Запрещенные заголовочные файлы
FORBIDDEN_HEADERS = {
    "fstream", "sstream", "cstdio", "cstdlib", "cctype",
    "sys/types.h", "sys/stat.h", "fcntl.h", "unistd.h",
    "windows.h", "process.h", "pthread.h",
    "sys/socket.h", "arpa/inet.h", "netinet/in.h", "netdb.h"
}

# Запрещенные функции
FORBIDDEN_FUNCTIONS = {
    "system(", "popen(", "exec(", "execl(", "execlp(", "execle(", "execv(", "execvp(",
    "fork(", "vfork(", "kill(", "exit(", "_exit(", "abort(", "raise(", "sigaction(",
    "socket(", "connect(", "send(", "recv(", "bind(", "listen(", "accept(",
    "open(", "close(", "read(", "write(", "fopen(", "freopen(", "fclose(",
    "ifstream", "ofstream", "fstream"
}

# Лимит вывода
MAX_OUTPUT_LENGTH = 150000

# Настраиваем логгер
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def truncate_output(output):
    """Ограничивает размер вывода"""
    if len(output) > MAX_OUTPUT_LENGTH:
        return output[:MAX_OUTPUT_LENGTH] + "\n[Вывод обрезан...]"
    return output


def check_code_safety(source_code):
    """Проверяет код на запрещенные библиотеки и функции"""
    for header in FORBIDDEN_HEADERS:
        if f"#include <{header}>" in source_code:
            return f"Ошибка: использование запрещенной библиотеки {header}!"

    for func in FORBIDDEN_FUNCTIONS:
        if func in source_code:
            return f"Ошибка: использование запрещенной функции {func}!"

    return None


def run_cpp(request):
    source_code = request["source_code"]
    stdin = request["stdin"]

    # Проверяем код на безопасность
    safety_error = check_code_safety(source_code)
    if safety_error:
        return {
            "output": safety_error,
            "status": "failed",
            "memory": "N/A",
            "time": "0 sec"
        }

    # Создаем временный C++ файл в ./timeFiles/
    temp_dir = "../timeFiles"
    os.makedirs(temp_dir, exist_ok=True)

    fd, temp_file_name = tempfile.mkstemp(suffix=".cpp", dir=temp_dir)
    os.close(fd)  # Закрываем дескриптор файла

    exec_file = temp_file_name.replace(".cpp", ".exe")

    try:
        # Записываем код в временный C++ файл
        with open(temp_file_name, "w", encoding="utf-8") as temp_file:
            temp_file.write(source_code)

        compile_cmd = ["g++", temp_file_name, "-o", exec_file, "-O2", "-std=c++17"]
        run_cmd = [exec_file]

        start_time = time.time()

        # Компиляция кода
        compile_process = subprocess.run(
            compile_cmd,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Если компиляция не удалась
        if compile_process.returncode != 0:
            return {
                "output": truncate_output(compile_process.stderr.strip()),
                "status": "failed",
                "memory": "N/A",
                "time": "0 sec"
            }

        # Запуск исполняемого файла
        run_process = subprocess.run(
            run_cmd,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=5
        )

        execution_time = time.time() - start_time
        memory_used = psutil.Process(os.getpid()).memory_info().rss / 1024

        if run_process.returncode != 0:
            return {
                "output": truncate_output(run_process.stderr.strip()),
                "status": "failed",
                "memory": f"{memory_used:.2f} KB",
                "time": f"{execution_time:.3f} sec"
            }

        return {
            "output": truncate_output(run_process.stdout.strip()),
            "status": "finished",
            "memory": f"{memory_used:.2f} KB",
            "time": f"{execution_time:.3f} sec"
        }

    except subprocess.TimeoutExpired:
        return {
            "output": "Ошибка: выполнение кода превысило лимит времени!",
            "status": "failed",
            "memory": "N/A",
            "time": "5 sec"
        }

    except Exception as e:
        return {
            "output": f"Ошибка: {str(e)}",
            "status": "failed",
            "memory": "N/A",
            "time": "0 sec"
        }

    finally:
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)
        if os.path.exists(exec_file):
            os.remove(exec_file)
