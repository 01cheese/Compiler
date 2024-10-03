# Online Compiler
![image](https://github.com/user-attachments/assets/bb8a9f8a-661c-4a65-9af1-ac2987badff0)

## Overview
This project is a multi-language online code editor supporting C++, JavaScript, and Python. Users can write code in a web-based editor, execute it on the server, and see the output in real-time. The project is built using Flask, Flask-SocketIO, and CodeMirror for syntax highlighting and code editing.

## Features
- **Real-time Code Execution**: Users can write code in C++, JavaScript, or Python and run it on the server.
- **Syntax Highlighting**: Provided by CodeMirror, with theme toggling between light and dark modes.
- **Input Handling**: Users can provide input to their code through the interface.
- **File Saving**: Users can save their code to a local file.
- **Live Output**: Output is displayed live, including any errors or results from the code execution.

## Technologies Used
- **Frontend**: HTML, CSS (with theme switching), CodeMirror for code editing.
- **Backend**: Flask, Flask-SocketIO for real-time communication.
- **Languages Supported**: C++, JavaScript, Python.

## Installation
1. Clone the repository:
2. Install the required dependencies:
   ```bash
   pip install flask flask-socketio
   ```
3. Start the servers for each language:
   - For C++:
     ```bash
     python cpp.py
     ```
   - For JavaScript:
     ```bash
     python js.py
     ```
   - For Python:
     ```bash
     python python.py
     ```

## Usage
- Navigate to the corresponding URLs for each language:
  - C++: `http://127.0.0.1:5001`
  - JavaScript: `http://127.0.0.1:5002`
  - Python: `http://127.0.0.1:5003`

Once on the page:
1. Write your code in the editor.
2. Click **Run** to execute the code.
3. Provide any input required by the program and see the output displayed in real-time.

## Future Enhancements
- Add support for additional languages.
- Implement more advanced error handling.
- Improve UI responsiveness across different devices.
