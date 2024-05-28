const resizer = document.querySelector('.resizer');
const editorContainer = document.querySelector('.editor-container');
const outputContainer = document.querySelector('.output-container');

let isResizing = false;

resizer.addEventListener('mousedown', function(e) {
    isResizing = true;

    document.addEventListener('mousemove', resize);
    document.addEventListener('mouseup', stopResize);
});

function resize(e) {
    if (isResizing) {
        const containerOffsetLeft = document.querySelector('.main-container').offsetLeft;
        const pointerRelativeXpos = e.clientX - containerOffsetLeft;
        const editorWidth = pointerRelativeXpos;
        const outputWidth = document.querySelector('.main-container').clientWidth - editorWidth;

        editorContainer.style.width = `${editorWidth}px`;
        outputContainer.style.width = `${outputWidth}px`;
    }
}

function stopResize() {
    isResizing = false;

    document.removeEventListener('mousemove', resize);
    document.removeEventListener('mouseup', stopResize);
}

function runPython() {
    var code = document.getElementById('code').value;
    fetch('/run_python', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            code: code
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerText = data.result_stdout; // Используйте 'result_stdout' для вывода стандартного вывода
    });
}

function clearOutput() {
    document.getElementById('output').innerText = '';
}
