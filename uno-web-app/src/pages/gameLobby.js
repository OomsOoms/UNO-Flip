import React from "react";
import "../scss/gameLobby.scss";
import { apiUrl, webSocketUrl } from "../index.js";

function GameLobby() {
  // Get the values from the URL
  const urlParams = new URLSearchParams(window.location.search);
  const gameId = urlParams.get("id");
  const playerId = sessionStorage.getItem(gameId);
  document.title = "UNO | Lobby " + gameId;

  if (!playerId) {
    console.log("No game ID in session storage for this game ID");

    if (document.referrer.includes(window.location.origin)) {
      window.history.back();
    } else {
      window.location.href = "/";
    }
    return;
  }

  // Send the request to the server
  const requestBody = {
    game_id: gameId,
    player_id: playerId,
  };

  const options = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(requestBody),
  };

  const url = apiUrl + "/lobby";
  // Send the POST request to the server
  fetch(url, options)
    // Check the response status
    .then((response) => {
      console.log("Lobby API response: " + response.status);
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error("Cannot load game lobby");
      }
    })
    // Update the lobby page with the game ID and player list with the json returned from the API
    .then((data) => {
      const gameIdSpan = document.getElementById("gameId");
      const playerListDiv = document.getElementById("playerList");
      const playerNames = data.player_names;
      const playerCount = document.getElementById("playerCount");

      playerCount.textContent = playerNames.length + "/10";
      gameIdSpan.textContent = gameId;
      playerListDiv.innerHTML = "";

      if (data.is_host) {
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
      for (const playerName of playerNames) {
        const playerElement = document.createElement("p");
        playerElement.textContent = playerName;
        playerListDiv.appendChild(playerElement);
      }
      const ws = new WebSocket(`${webSocketUrl}/ws?game_id=${gameId}&player_id=${playerId}`);
      ws.onopen = () => {
        console.log("WebSocket connection opened");
      };
      ws.onmessage = (event) => {
        // listen to data sent from the websocket server
        const message = event.data;
        if (message === "update_lobby") {
          console.log("Player change detected, updating lobby");
          ws.close();
          GameLobby();
        }
      };
      ws.onclose = () => {
        console.log("disconnected");
        // TODO: automatically try to reconnect on connection loss
      };
    })
    // Catch any errors and log them to the console
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
      if (document.referrer.includes(window.location.origin)) {
        window.history.back();
      } else {
        window.location.href = "/";
      }
      return;
    });

  return (
    <>
      <div id="lobbyContainer">
        <h1>Game Lobby</h1>
        <div>
          <p>
            <strong>Players:</strong> <span id="playerCount">/10</span> | <strong>ID:</strong> <span id="gameId" className="large"></span>
          </p>
        </div>
      </div>

      <div id="playerListContainer">
        <ul id="playerList"></ul>
      </div>
    </>
  );
}

export default GameLobby;
