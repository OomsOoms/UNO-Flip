import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./scss/index.scss";
import Header from "./pages/header.js";
import Home from "./pages/home.js";
import JoinGameForm from "./pages/joinGame.js";
import CreateGameForm from "./pages/createGame.js";
import GameRoom from "./pages/gameRoom.js";
import AdminStats from "./pages/adminStats.js";

const apiUrl = "http://127.0.0.1:8000";
const webSocketUrl = "ws://127.0.0.1:8000";
export { apiUrl, webSocketUrl};

function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" >
          <Route path="/" element={<Home />} />
          <Route path="join-game" element={<JoinGameForm />} />
          <Route path="create-game" element={<CreateGameForm />} />
          <Route path="lobby" element={<GameRoom />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Route>
        <Route path="/admin" element={<AdminStats />} />
      </Routes>
    </BrowserRouter>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
