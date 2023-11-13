import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./scss/index.scss";
import Header from "./pages/header.js";
import Home from "./pages/home.js";
import JoinGameForm from "./pages/joinGame.js";
import CreateGame from "./pages/createGame.js";
import GameLobby from "./pages/gameLobby.js";

const apiUrl = "http://127.0.0.1:8000";
const webSocketUrl = "ws://127.0.0.1:8000";
export { apiUrl, webSocketUrl};

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/join-game" element={<JoinGameForm />} />
        <Route path="/create-game" element={<CreateGame />} />
        <Route path="/lobby" element={<GameLobby />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
