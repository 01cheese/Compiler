window.onload = () => {
    const socket = io();
    const codeEditor = CodeMirror.fromTextArea(document.getElementById('codeEditor'), {
        lineNumbers: true,
        mode: "python",
        theme: "material-darker",
    });

    Split(['#editorSection', '#outputSection'], {
    sizes: [50, 50],
    minSize: [320, 160],
    gutterSize: 10,
    cursor: 'col-resize',
});


document.querySelectorAll('.icon').forEach(icon => {
    icon.addEventListener('click', () => {
        const lang = icon.getAttribute('data-lang');
        let mode;
        switch (lang) {
            case 'python':
                mode = 'python';
                break;
            case 'cpp':
                mode = 'text/x-c++src';
                break;
            case 'javascript':
                mode = 'javascript';
                break;
            case 'sql':
                mode = 'text/x-sql';
                break;
            default:
                mode = 'python';
        }
        codeEditor.setOption('mode', mode);
        document.querySelector('.filename').textContent = `main.${lang}`;
    });
});




// Listen for output from the server
socket.on('outputArea', (data) => {
    const outputArea = document.getElementById('outputArea');
    outputArea.textContent += data.data + '\n';
});

    function runCode() {
        var code = document.getElementById('pythonCode').value;
        document.getElementById('outputArea').innerHTML = '';  // Очищаем предыдущее
        socket.emit('run_code', { code: code + '\nprint()\nprint("=== Code Execution Successful ===")'});
    }


    document.getElementById('runButton').addEventListener('click', () => {
        document.getElementById('outputArea').textContent = '';
    });


    // Event for running code
    document.getElementById('runButton').addEventListener('click', () => {
        const code = codeEditor.getValue();
        socket.emit('run_code', { code: code });
    });


    //document.getElementById('runButton').addEventListener('click', runCode  => {
      //  document.getElementById('outputArea').textContent = '=== Code Execution Successful ===';
    //});


    // Event for sending input
    document.getElementById('sendInput').addEventListener('click', () => {
        const userInput = document.getElementById('userInput').value;
        socket.emit('user_input', { input: userInput });
        document.getElementById('userInput').value = '';  // Clear input field
    });



    document.getElementById('saveButton').addEventListener('click', () => {
        const code = codeEditor.getValue();
        const blob = new Blob([code], { type: 'text/plain' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'code.txt';
        link.click();
    });

    // Clear output
    document.getElementById('clearButton').addEventListener('click', () => {
        document.getElementById('outputArea').textContent = '';
    });

    document.getElementById('themeToggleButton').addEventListener('click', () => {
        const body = document.body;
        const isDark = body.classList.toggle('light-theme');
        body.classList.toggle('dark-theme', !isDark);
        codeEditor.setOption('theme', isDark ? 'default' : 'material-darker');
    });

    document.getElementById('fullscreenButton').addEventListener('click', () => {
        const body = document.body;
        const sidebar = document.querySelector('.sidebar');
        const mainContent = document.querySelector('.main-content');
        const isFullscreen = body.classList.toggle('fullscreen-mode');
        sidebar.classList.toggle('hidden', isFullscreen);

        if (isFullscreen) {
            if (body.requestFullscreen) {
                body.requestFullscreen();
            } else if (body.mozRequestFullScreen) { // Firefox
                body.mozRequestFullScreen();
            } else if (body.webkitRequestFullscreen) { // Chrome, Safari and Opera
                body.webkitRequestFullscreen();
            } else if (body.msRequestFullscreen) { // IE/Edge
                body.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.mozCancelFullScreen) { // Firefox
                document.mozCancelFullScreen();
            } else if (document.webkitExitFullscreen) { // Chrome, Safari and Opera
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) { // IE/Edge
                document.msExitFullscreen();
            }
        }
    });
};
