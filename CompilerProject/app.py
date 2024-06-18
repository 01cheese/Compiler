from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

def execute_code(code):
    process = subprocess.Popen(
        ["python", "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    for line in process.stdout:
        socketio.sleep(0)  # Very important for not blocking the event loop
        emit('message', {'message': line.strip()}, broadcast=True)
    for line in process.stderr:
        socketio.sleep(0)
        emit('message', {'message': "Error: " + line.strip()}, broadcast=True)
    process.wait()

@socketio.on('run_code')
def handle_run_code(json):
    code = json['code']
    execute_code(code)

def main():
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    main()
