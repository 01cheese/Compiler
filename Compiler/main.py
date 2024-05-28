from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('python.html')

@app.route('/run_python', methods=['POST'])
def run_python():
    code = request.form['code']
    result_stdout, result_stderr = run_python_code(code)
    return jsonify({'result_stdout': result_stdout, 'result_stderr': result_stderr})

def run_python_code(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as tmp_file:
        tmp_file.write(code.encode('utf-8'))
        tmp_file_path = tmp_file.name

    try:
        result = subprocess.run(
            ['python', tmp_file_path],
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr
    finally:
        os.remove(tmp_file_path)

if __name__ == '__main__':
    app.run(debug=True)
