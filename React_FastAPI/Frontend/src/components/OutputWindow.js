import React, { useState, useRef } from "react";

const OutputWindow = ({ outputDetails, showCopyToast }) => {
  // Начальный размер шрифта
  const [fontSize, setFontSize] = useState(16);
  // Ссылка для блока с выводом, чтобы управлять прокруткой
  const outputRef = useRef(null);

  // Увеличение шрифта
  const handleIncreaseFont = () => {
    setFontSize((prevFontSize) => prevFontSize + 2);
  };

  // Уменьшение шрифта
  const handleDecreaseFont = () => {
    setFontSize((prevFontSize) => prevFontSize - 2);
  };

  // Копирование содержимого в буфер обмена
  const handleCopy = () => {
    const textToCopy = `${outputDetails?.output}\n${outputDetails?.status}\n${outputDetails?.time}\n${outputDetails?.memory}`;
    navigator.clipboard.writeText(textToCopy)
      .then(() => {
          showCopyToast('Copy output!')
      })
      .catch((err) => {
        console.error("Ошибка при копировании:", err);
      });
  };

  // Прокрутка блока до самого низа
  const handleScrollToBottom = () => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  };

  return (
    <div className="output-container">
      <div className="button-column">
        <button onClick={handleIncreaseFont} title='Increase'>➕</button>
        <button onClick={handleDecreaseFont} title='Decrease'>➖</button>
        <button onClick={handleCopy} title='Copy'>📋</button>
        <button onClick={handleScrollToBottom} title='Down the text'>⬇</button>
      </div>
      <div
        className="output-block"
        ref={outputRef}
        style={{ fontSize: `${fontSize}px`, overflowY: "auto", maxHeight: "300px" }}
      >
        <pre>
          {outputDetails?.output}
          <p>{outputDetails?.status}</p>
          <p>{outputDetails?.time}</p>
          <p>{outputDetails?.memory}</p>
        </pre>
      </div>
    </div>
  );
};

export default OutputWindow;
