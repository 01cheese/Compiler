from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os
import tempfile

app = Flask(__name__)
socketio = SocketIO(app)

# Храним процесс выполнения программы
process = None

# Главная страница с интерфейсом для ввода JavaScript кода
@app.route('/')
def index():
    return render_template('js.html')

# Функция для выполнения JavaScript кода
def execute_js_code(code):
    global process  # Используем глобальный процесс для передачи в него ввода
    # Создаём временный файл с расширением .js
    with tempfile.NamedTemporaryFile(suffix=".js", delete=False) as temp_js:
        temp_js.write(code.encode('utf-8'))
        temp_js.flush()
        temp_js_filename = temp_js.name

    # Выполняем JavaScript код с помощью Node.js
    process = subprocess.Popen(["node", temp_js_filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)

    # Чтение stdout и stderr в реальном времени
    while True:
        output = process.stdout.readline()
        if output:
            socketio.emit('outputArea', {'data': output.strip()})
        else:
            break

    # Закрываем процесс, если он завершён
    process.wait()

    # Удаляем временный файл
    os.remove(temp_js_filename)

# Обработчик для передачи данных в программу через stdin
@socketio.on('user_input')
def handle_user_input(data):
    global process
    if process:
        try:
            process.stdin.write(data['input'] + '\n')  # Передаём данные в процесс
            process.stdin.flush()  # Очищаем буфер
        except OSError as e:
            print(f"Error writing to stdin: {e}")

# Обработчик событий для выполнения кода
@socketio.on('run_code')
def handle_run_code(data):
    code = data['code']  # Получаем код от клиента
    execute_js_code(code)

if __name__ == '__main__':
    socketio.run(app, port=5002, debug=True)
