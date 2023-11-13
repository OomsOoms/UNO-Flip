import React, { useState, useEffect } from "react";
import "../scss/gameLobby.scss";
import { webSocketUrl } from "../index.js";

function GameLobby() {
  const urlParams = new URLSearchParams(window.location.search);

  const gameId = urlParams.get("id")
  const playerId = sessionStorage.getItem(gameId)
  const [playerNames, setPlayerNames] = useState([]);

  document.title = "UNO | Lobby " + gameId;

  useEffect(() => {
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
    }

    ws.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
  
      const message = JSON.parse(event.data);

      switch (message.type) {
        case "lobby":
          setPlayerNames(message.player_names);

          if (message.is_host) {
            const playerListContainer = document.getElementById("playerListContainer");
            let startGameButton = document.getElementById("startGameButton");
            if (!startGameButton) {
              startGameButton = document.createElement("button");
              startGameButton.textContent = "Start Game";
              startGameButton.id = "startGameButton";
              startGameButton.onclick = function () {
              console.log("Start game button clicked");
              };
              playerListContainer.appendChild(startGameButton);
            }
          }
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
            <strong>Players:</strong> <span>{playerNames.length}/10</span> | <strong>ID:</strong> <span>{gameId}</span>
          </p>
        </div>
      </div>

      <div id="playerListContainer">
        <ul id="playerList">
          {playerNames.map((playerName, index) => (
            <p key={index}>{playerName}</p>
          ))}
        </ul>
      </div>
    </>
  );
}

export default GameLobby;
