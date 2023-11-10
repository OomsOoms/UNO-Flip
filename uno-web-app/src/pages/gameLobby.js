import React from "react";
import "../styles/gameLobby.css";
import { apiUrl, webSocketUrl } from "../index.js";

function GameLobby() {


  return (
    <>
      <div id="lobbyContainer">
        <h1>Game Lobby</h1>
        <div>
          <p>
            <strong>Players:</strong> <span id="playerCount">/10</span> |{" "}
            <strong>ID:</strong> <span id="gameId" className="large"></span>
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


function loadLobby() {
	// Get the values from the URL
	const urlParams = new URLSearchParams(window.location.search);
	const gameId = urlParams.get("id");
	const playerId = sessionStorage.getItem(gameId); // Fetch the player ID stored under the game ID
	// Check session storage for the game ID, if it doesn't exist redirect to the index page
	if (!playerId){
		console.log("No game ID in session storage, redirecting to index");
		window.location.href = "index.html";
		return;
	}
	// Send the request to the server
  fetch(apiUrl + "/lobby", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      game_id: gameId,
      player_name: playerId,
    }),
  })
	.then((response) => {
		console.log("Lobby API response: " + response.status)
		if (response.status === 200) {
			return response.json();
		} else {
			window.location.href = "index.html";
			return;
		}
	})
	.then((data) => {
		console.log("Lobby data received:", data);

		const loader = document.getElementById("loader");
		const playerListContainer = document.getElementById("playerListContainer");
		const lobbyContainer = document.getElementById("lobbyContainer");

		loader.style.display = "none";
		playerListContainer.style.display = "block";
		lobbyContainer.style.display = "block";

		const gameIdSpan = document.getElementById("gameId");
		const playerListDiv = document.getElementById("playerList");
		const playerNames = data.player_names;
		const playerCount = document.getElementById("playerCount");
		
		playerCount.textContent = playerNames.length + "/10";
		gameIdSpan.textContent = gameId;
		playerListDiv.innerHTML = "";

		if (data.is_host) {

			const playerListContainer = document.getElementById("playerListContainer");
			const startGameButton = document.createElement("button");
			startGameButton.textContent = "Start Game";
			startGameButton.id = "startGameButton";
			startGameButton.onclick = function() {
				console.log("Start game button clicked");
			}
			playerListContainer.appendChild(startGameButton);
		}
		
		for (const playerName of playerNames) {
			const playerElement = document.createElement("p");
			playerElement.textContent = playerName;
			playerListDiv.appendChild(playerElement);
		}

		var ws = new WebSocket(WebSocketUrl + "/ws");
		ws.onmessage = function (event) {
			if (event.data === "new_player") {
				console.log("New player joined, reloading lobby");
				// Close connection to the server then reload the lobby
				ws.close();
				loadLobby();
			};
		};
	})
	.catch((error) => {
		console.error("Fetch error:", error);
	});
}