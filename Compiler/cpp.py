import os

import subprocess
import tempfile
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import queue
import os
import subprocess
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import queue

app = Flask(__name__)
socketio = SocketIO(app)

process = None
input_queue = queue.Queue()

@app.route('/')
def index():
    return render_template('cpp.html')


def execute_cpp_code(code):
    global process

    # Создаем временный файл с расширением .cpp
    with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as temp_cpp:
        temp_cpp.write(code.encode('utf-8'))
        temp_cpp.flush()
        temp_cpp_filename = temp_cpp.name

    # Определяем имя скомпилированного файла
    compiled_file = temp_cpp_filename.replace('.cpp', '')
    if os.name == 'nt':  # Windows платформа
        compiled_file += ".exe"

    # Компилируем C++ файл
    compilation = subprocess.run(["g++", temp_cpp_filename, "-o", compiled_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Если есть ошибки компиляции, отправляем их на клиент
    if compilation.stderr:
        socketio.emit('outputArea', {'data': 'Compilation Error:\n' + compilation.stderr})
        return

    # Проверяем существование скомпилированного файла
    if os.path.exists(compiled_file):
        process = subprocess.Popen(
            [compiled_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            universal_newlines=True
        )

        # Запускаем потоки для обработки вывода
        threading.Thread(target=process_output, args=(process.stdout,)).start()
        threading.Thread(target=process_output, args=(process.stderr,)).start()

        # Поток для обработки пользовательского ввода
        threading.Thread(target=handle_input).start()

        process.wait()
    else:
        socketio.emit('outputArea', {'data': 'Compiled file not found.'})

def process_output(pipe):
    while True:
        output = pipe.readline()
        if output:
            socketio.emit('outputArea', {'data': output.strip()})
        else:
            break

def handle_input():
    global process
    while process and process.poll() is None:
        try:
            user_input = input_queue.get(timeout=1)
            if user_input:
                process.stdin.write(user_input + '\n')
                process.stdin.flush()
        except queue.Empty:
            continue

@socketio.on('user_input')
def handle_user_input(data):
    input_queue.put(data['input'])

@socketio.on('run_code')
def handle_run_code(data):
    code = data['code']
    execute_cpp_code(code)

if __name__ == '__main__':
    socketio.run(app, port=5001, debug=True)
