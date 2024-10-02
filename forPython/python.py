from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import tempfile
import threading
import queue

app = Flask(__name__)
socketio = SocketIO(app)

process = None
input_queue = queue.Queue()


# Главная страница с интерфейсом для ввода Python кода
@app.route('/')
def index():
    return render_template('python.html')


# Функция для выполнения Python кода
def execute_python_code(code):
    global process

    # Создаём временный файл с расширением .py
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_py:
        temp_py.write(code.encode('utf-8'))
        temp_py.flush()
        temp_py_filename = temp_py.name

    # Запускаем процесс выполнения Python кода
    process = subprocess.Popen(
        ["python", temp_py_filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    # Запуск потока для обработки вывода программы
    threading.Thread(target=process_output, args=(process.stdout,)).start()

    # Запуск потока для обработки ошибок программы
    threading.Thread(target=process_output, args=(process.stderr,)).start()

    # Поток для передачи ввода в процесс
    threading.Thread(target=handle_input).start()

    process.wait()

    os.remove(temp_py_filename)


# Обработчик вывода процесса
def process_output(pipe):
    while True:
        output = pipe.readline()
        if output:
            socketio.emit('output', {'data': output.strip()})
        else:
            break


# Поток для обработки пользовательского ввода
def handle_input():
    global process
    while process and process.poll() is None:
        try:
            # Ждём ввода от очереди
            user_input = input_queue.get(timeout=1)
            if user_input:
                process.stdin.write(user_input + '\n')
                process.stdin.flush()
        except queue.Empty:
            continue


# Обработчик для передачи данных в программу через stdin
@socketio.on('user_input')
def handle_user_input(data):
    input_queue.put(data['input'])


# Обработчик событий для выполнения кода
@socketio.on('run_code')
def handle_run_code(data):
    code = data['code']
    execute_python_code(code)


if __name__ == '__main__':
    socketio.run(app, debug=True)
