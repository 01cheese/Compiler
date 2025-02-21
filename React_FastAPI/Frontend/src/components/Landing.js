import React, {useEffect, useRef, useState} from "react";
import CodeEditorWindow from "./CodeEditorWindow";
import './Landing.css'
import axios from "axios";
import {classnames} from "../utils/general";
import {languageOptions} from "../constants/languageOptions";
import {ToastContainer, toast} from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {defineTheme} from "../lib/defineTheme";
import useKeyPress from "../hooks/useKeyPress";
import OutputWindow from "./OutputWindow";
import CustomInput from "./CustomInput";

import ThemeDropdown from "./ThemeDropdown";
import LanguagesDropdown from "./LanguagesDropDown";
import TextField from "./TextField";
import languagesDropDown from "./LanguagesDropDown";

const javascriptDefault =
    `// Write your C++ code here 
#include <iostream>

int main() {
    std::cout << "Hello World!";
    return 0;
}`;

const Landing = () => {


    const [code, setCode] = useState(javascriptDefault);
    const [customInput, setCustomInput] = useState("");
    const [outputDetails, setOutputDetails] = useState(null);
    const [processing, setProcessing] = useState(null);
    const [theme, setTheme] = useState("cobalt");
    const [language, setLanguage] = useState(languageOptions[1]);

    const [isDarkMode, setIsDarkMode] = useState(true); // Отслеживаем текущую тему


    const enterPress = useKeyPress("Enter");
    const ctrlPress = useKeyPress("Control");

    const targetRef = useRef(null);

  const handleScroll = () => {
    targetRef.current.scrollIntoView({ behavior: 'smooth' });
  };


    const onSelectChange = (sl) => {
        setLanguage(sl);
    };

    useEffect(() => {
        if (isDarkMode) {
            document.body.classList.add("dark-mode");
            document.body.classList.remove("light-mode");
        } else {
            document.body.classList.add("light-mode");
            document.body.classList.remove("dark-mode");
        }
    }, [isDarkMode]);
    const toggleTheme = () => {
        setIsDarkMode((prevMode) => !prevMode);
    };

    useEffect(() => {
        if (enterPress && ctrlPress) {
            handleCompile();
        }
    }, [ctrlPress, enterPress]);
    const onChange = (action, data) => {
        switch (action) {
            case "code": {
                setCode(data);
                break;
            }
        }
    };

    const handleCompile = async () => {
        setProcessing(true);

        const payload = {
            language_id: language.id, // ID языка
            source_code: code, // Код
            stdin: customInput, // Входные данные
        };

        try {
            // 🔹 Отправляем код на сервер
            const response = await axios.post("http://localhost:8000/execute", payload, {
                headers: {"Content-Type": "application/json"}
            });

            const taskId = response.data.task_id;

            // 🔹 Ждём выполнения кода и запрашиваем результат
            let result;
            let attempts = 10; // Количество попыток запроса результата
            while (attempts > 0) {
                await new Promise((resolve) => setTimeout(resolve, 1000)); // Ждём 1 сек

                const resultResponse = await axios.get(`http://localhost:8000/result/${taskId}`);

                if (resultResponse.data.status === "finished") {
                    result = resultResponse.data;
                    break;
                } else if (resultResponse.data.status === "failed") {
                    result = resultResponse.data
                    break
                }

                attempts--;
            }

            if (!result) {
                throw new Error("Ошибка: сервер не вернул результат.");
            }

            // 🔹 Сохраняем результат выполнения
            setOutputDetails(result);
            showSuccessToast("Код успешно выполнен!");
        } catch (error) {
            showErrorToast("Ошибка выполнения кода!");
        }

        setProcessing(false);
    };

    function handleThemeChange(th) {
        const theme = th;
        if (["light", "vs-dark"].includes(theme.value)) {
            setTheme(theme);
        } else {
            defineTheme(theme.value).then((_) => setTheme(theme));
        }
    }

    useEffect(() => {
        defineTheme("tomorrow-night-bright").then((_) =>
            setTheme({value: "tomorrow-night-bright", label: "Tomorrow-Night-Bright"})
        );
    }, []);

    const showSuccessToast = (msg) => {
        toast.success(msg || `Compiled Successfully!`, {
            position: "top-right",
            autoClose: 2000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
        });
    };
    const showCopyToast = (msg) => {
        toast.success(msg || `Copy output!`, {
            position: "top-right",
            autoClose: 1000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
        });
    };
    const showErrorToast = (msg, timer) => {
        toast.error(msg || `Something went wrong in server!`, {
            position: "top-right",
            autoClose: timer ? timer : 2000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
        });
    };

    return (
        <>
            <header>
                <h2 className="logo">
                    <a onClick={handleScroll}>About</a>
                    <a href='https://vzbb.site'>Me</a>
                    <a href='https://github.com/01cheese'>GitHub</a>
                </h2>
            </header>

            <ToastContainer
                position="top-right"
                autoClose={2000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
            />

            <div className="editorContainer">
                <CodeEditorWindow code={code} onChange={onChange} language={language?.value} theme={theme.value}/>
            </div>

            <div className="toolbar">
                <button
                    onClick={handleCompile}
                    disabled={!code || processing} // Кнопка отключена, если нет кода или идёт обработка
                    className={`themeButton ${isDarkMode ? "dark" : "light"} ${processing ? 'process' : 'run'}`}
                >
                    {processing ? "Process" : " ▶ Run"}
                </button>


                <button onClick={toggleTheme} className={`themeButton ${isDarkMode ? "dark" : "light"}`}>
                    {isDarkMode ? "🌙 Theme" : "☀️ Theme"}
                </button>
                <LanguagesDropdown onSelectChange={onSelectChange} theme={isDarkMode}/>
            </div>

            <div className="bottom-container">
                <div className="output-section">
                    <OutputWindow outputDetails={outputDetails} showCopyToast={showCopyToast}/>
                </div>
                <div className='input-section'>
                <CustomInput customInput={customInput} setCustomInput={setCustomInput}/>
                </div>
            </div>
            <div ref={targetRef}></div>
            <TextField/>
        </>
    );
};
export default Landing;