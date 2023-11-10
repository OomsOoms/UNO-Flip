import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./styles/index.css";
import Header from "./pages/header.js";
import Home from "./pages/home.js";
import JoinGameForm from "./pages/joinGame.js";
import CreateGame from "./pages/createGame.js";
import NoPage from "./pages/noPage";

const apiUrl = "http://127.0.0.1:8000";
export default apiUrl;

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<NoPage />} />
        <Route path="/join-game" element={<JoinGameForm />} />
        <Route path="/create-game" element={<CreateGame />} />
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
