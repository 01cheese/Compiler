import React, { useState } from "react";
import Editor from "@monaco-editor/react";

const CodeEditorWindow = ({ onChange, language, code, theme }) => {
    const [value, setValue] = useState(code || "");

    const handleEditorChange = (value) => {
        setValue(value);
        onChange("code", value);
    };

    return (
        <div className="overlay rounded-md overflow-hidden w-full h-full shadow-4xl">
            <Editor
                height="85vh"
                language={language || "cpp"}
                value={value}
                theme={theme}
                defaultValue="// some comment"
                onChange={handleEditorChange}
            />
        </div>
    );
};
export default CodeEditorWindow;