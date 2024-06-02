from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
import subprocess

app = Flask(__name__)
socketio = SocketIO(app)

TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Python Code Executor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.0/socket.io.js"></script>
    <script type="text/javascript">
        var socket = io.connect();
        socket.on('message', function(data) {
            var output = document.getElementById('output');
            output.innerHTML += data.message + '\\n';
        });
        function runCode() {
            var code = document.getElementById('code').value;
            socket.emit('run_code', {code: code});
        }
    </script>
</head>
<body>
    <h1>Python Code Executor</h1>
    <textarea id="code" rows="10" cols="50"></textarea><br>
    <button onclick="runCode()">Run Code</button>
    <h2>Output:</h2>
    <pre id="output"></pre>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(TEMPLATE)

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

if __name__ == "__main__":
    socketio.run(app, debug=True)
