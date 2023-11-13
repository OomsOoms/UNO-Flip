import React, { useState, useEffect } from "react";
import "../scss/gameLobby.scss";
import { apiUrl, webSocketUrl } from "../index.js";

function GameLobby() {
  const urlParams = new URLSearchParams(window.location.search);

  const gameId = urlParams.get("id");
  const playerId = sessionStorage.getItem(gameId);

  const [playerNames, setPlayerNames] = useState([]);
  const [isHost, setIsHost] = useState(false);

  document.title = "UNO | Lobby " + gameId;

  const startGame = () => {
    const requestbody = {
      game_id: gameId,
      player_id: playerId,
    };
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestbody),
    };
    fetch(`${apiUrl}/start_game`, requestOptions)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Game started successfully" + data.message);
        } else {
          console.log("Error:", data.detail);
        }
      })
      .catch((error) => console.log("Error:", error));
  };

  useEffect(() => {
    if (playerId === null) {
      console.log("Player ID not found in session storage")
      if (document.referrer.includes(window.location.origin)) {
        window.history.back();
      } else {
        window.location.href = "/";
      }
      return;
    }
    const ws = new WebSocket(`${webSocketUrl}/lobby?game_id=${gameId}&player_id=${playerId}`);

    ws.onopen = () => {
      console.log("WebSocket connection opened");
    };

    ws.onclose = () => {
      console.log("WebSocket connection disconnected");
      if (document.referrer.includes(window.location.origin)) {
        window.history.back();
      } else {
        window.location.href = "/";
      }
      return;
    };

    ws.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);

      const message = JSON.parse(event.data);

      switch (message.type) {
        case "lobby":
          setPlayerNames(message.player_names);
          setIsHost(message.is_host);
          break;
        case "game_state":
          console.log(`Game state: ${message.game_state}`);
          break;
        default:
          console.log("Unknown message type:", message.type);
      }
    };
  }, [gameId, playerId]);

  return (
    <>
      <div id="lobbyContainer">
        <h1>Game Lobby</h1>
        <div>
          <p>
            Players: {playerNames.length}/10 | ID {gameId}
          </p>
        </div>
      </div>

      <div id="playerListContainer">
        <ul id="playerList">
          {playerNames.map((playerName, index) => (
            <p key={index}>{playerName}</p>
          ))}
        </ul>

        {isHost && (
          <button id="startGameButton" onClick={startGame}>
            Start Game
          </button>
        )}
      </div>
    </>
  );
}

export default GameLobby;
