import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import JoinGame from "./joinGame.js"

const apiUrl = "http://127.0.0.1:8000";
export default apiUrl;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<JoinGame />);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
