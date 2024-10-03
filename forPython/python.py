from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess
import os
import tempfile
import threading
import queue
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Client-specific storage
clients = {}

# Main page
@app.route('/')
def index():
    return render_template('python.html')


# Function to execute the Python code
def execute_python_code(client_id, code):
    try:
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_py:
            temp_py.write(code.encode('utf-8'))
            temp_py.flush()
            temp_py_filename = temp_py.name

        # Run the Python code in a separate process
        process = subprocess.Popen(
            ["python", "-u", temp_py_filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        clients[client_id]['process'] = process

        # Start threads to handle output and input
        threading.Thread(target=process_output, args=(client_id, process.stdout,)).start()
        threading.Thread(target=process_output, args=(client_id, process.stderr,)).start()
        threading.Thread(target=handle_input, args=(client_id,)).start()

        # Wait for the process to complete
        process.wait(timeout=60)  # Add timeout to prevent long-running processes

    except subprocess.TimeoutExpired:
        socketio.emit('outputArea', {'data': 'Process timed out!'}, room=client_id)

    except Exception as e:
        socketio.emit('outputArea', {'data': f'Error: {str(e)}'}, room=client_id)

    finally:
        os.remove(temp_py_filename)
        clients[client_id]['process'] = None


# Handle process output
def process_output(client_id, pipe):
    while True:
        output = pipe.readline()
        if output:
            socketio.emit('outputArea', {'data': output.strip()}, room=client_id)
        else:
            break


# Handle user input to the process
def handle_input(client_id):
    process = clients.get(client_id, {}).get('process')
    input_queue = clients.get(client_id, {}).get('input_queue')

    while process and process.poll() is None:
        try:
            user_input = input_queue.get(timeout=1)
            if user_input:
                process.stdin.write(user_input + '\n')
                process.stdin.flush()
        except queue.Empty:
            continue


# Handle user input event from the frontend
@socketio.on('user_input')
def handle_user_input(data):
    client_id = request.sid
    input_queue = clients.get(client_id, {}).get('input_queue')
    if input_queue:
        input_queue.put(data['input'])


# Handle code execution event
@socketio.on('run_code')
def handle_run_code(data):
    client_id = request.sid
    code = data['code']

    # Initialize client-specific storage
    if client_id not in clients:
        clients[client_id] = {'process': None, 'input_queue': queue.Queue()}

    # Execute the Python code in a separate thread
    threading.Thread(target=execute_python_code, args=(client_id, code)).start()


if __name__ == '__main__':
    socketio.run(app, port=5003, debug=True)
