window.onload = () => {
    let mode = 'javascript';  // Default mode
    const port = window.location.port;  // Get the current port
    let path = '';

    // Set the mode based on the port
    if (port === '5001') {
        mode = 'text/x-c++src';
        path = 'cpp'
    } else if (port === '5002') {
        mode = 'javascript';
        path = 'js'
    } else if (port === '5003') {
        mode = 'python';
        path = 'py'
    }

    const socket = io();
    const codeEditor = CodeMirror.fromTextArea(document.getElementById('codeEditor'), {
        lineNumbers: true,
        mode: mode,
        theme: "material-darker",
    });

    Split(['#editorSection', '#outputSection'], {
        sizes: [50, 50],
        minSize: [320, 160],
        gutterSize: 10,
        cursor: 'col-resize',
    });

    // Listen for output from the server
    socket.on('outputArea', (data) => {
        const outputArea = document.getElementById('outputArea');
        outputArea.textContent += data.data + '\n';
        // Проверяем статус выполнения
        if (data.status === 'finished') {
            outputArea.textContent += "---код выполнен---\n";
        }
    });

    // Clear output and run the code when 'Run' button is clicked
    document.getElementById('runButton').addEventListener('click', () => {
        document.getElementById('outputArea').textContent = '';  // Clear previous output
        const code = codeEditor.getValue();
        socket.emit('run_code', { code: code });  // Send the code to the server
    });

    // Send input from the user
    document.getElementById('sendInput').addEventListener('click', () => {
        const userInput = document.getElementById('userInput').value;
        socket.emit('user_input', { input: userInput });
        document.getElementById('userInput').value = '';  // Clear input field
    });

    // Save the code to a file
    document.getElementById('saveButton').addEventListener('click', () => {
        const code = codeEditor.getValue();
        const blob = new Blob([code], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'code.'+path;
        link.click();
    });

    // Clear the output area
    document.getElementById('clearButton').addEventListener('click', () => {
        document.getElementById('outputArea').textContent = '';
    });

    // Toggle theme between light and dark
    document.getElementById('themeToggleButton').addEventListener('click', () => {
        const body = document.body;
        const isDark = body.classList.toggle('light-theme');
        body.classList.toggle('dark-theme', !isDark);
        codeEditor.setOption('theme', isDark ? 'default' : 'material-darker');
    });
};
