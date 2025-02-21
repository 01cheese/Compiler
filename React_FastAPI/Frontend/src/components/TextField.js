import {FaGithub, FaTelegram} from "react-icons/fa";
import React from "react";

const TextField = () => {
    return (
        <div className="textBlock">
            {/* Заголовок */}
            <div>
                <h1 className='para'>Hello everyone!</h1>
                <p>---------/----------/--///----/</p>
                <p>
                    This project is an online compiler supporting Python, JavaScript, and C++.
                    It is built using cutting-edge technologies on both the frontend and backend sides.
                </p>
                <p>---------/----------/--///----/</p>
                <h2 className="para">Technologies Used</h2>
                <p>---------/----------/--///----/</p>
                <ul>
                    <a href='https://react.dev/'>
                        <li>⚡ React - for creating a dynamic user interface</li>
                    </a>
                    <a href='https://tailwindcss.com/'>
                        <li>🎨 Tailwind CSS - for responsive and modern styling</li>
                    </a>

                    <a href='https://en.wikipedia.org/wiki/WebSocket'>
                        <li>🔗 WebSockets - for real-time communication</li>
                    </a>

                </ul>

                <p>---------/----------/--///----/</p>
                <ul>
                    <a href='https://fastapi.tiangolo.com/'>
                        <li>🚀 FastAPI - for handling API requests</li>
                    </a>
                    <a href='https://redis.io/'>
                        <li>📡 Celery & Redis - for executing and managing compilation tasks</li>
                    </a>

                    <a href='https://www.python.org/'>
                        <li>🛠 Python & Node.js - for secure code execution</li>
                    </a>

                    <a href=''>
                        <li>🔍 Security Filters - to prevent malicious code execution</li>
                    </a>

                </ul>
                <p>---------/----------/--///----/</p>

                <div className="container mx-auto px-4">
                    <div className="flex flex-col items-center gap-y-2 justify-center">
                        <div className="flex gap-x-3 text-lg text-[#ddd]">
                            <a href="https://github.com/01cheese">
                                <FaGithub size={20}/>
                            </a>
                            <a href="https://t.me/vzbbsi">
                                <FaTelegram size={20}/>
                            </a>
                        </div>
                        <div className="text-[#ddd] font-medium text-sm">
                            &copy; 2025. All rights reserved.
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TextField;