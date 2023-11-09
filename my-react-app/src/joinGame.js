import React from "react";
import "./joinGame.css";
import apiUrl from "./index.js";
import showNotification from "./notification.js"; // close notif doesnt work when importing like this

function JoinGameForm() {
  const handleSubmit = (event) => {
    event.preventDefault();

    const usernameInput = document.getElementById("usernameInput");
    const gameIdInput = document.getElementById("gameIdInput");
    const username = usernameInput.value;
    const gameId = gameIdInput.value;

    if (usernameInput.value && gameIdInput.value) {
      // Check if the game ID is already in the session storage and redirect
      if (sessionStorage.getItem(gameId)) {
        console.log("Redirecting to previous joined game in session storage");
        window.location.href = "lobby.html?id=" + gameId;
        return;
      }

      fetch(apiUrl + "/join_game", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          game_id: gameId,
          player_name: username,
        }),
      })
        .then((response) => {
          console.log("Join game button: " + response.status);
          if (response.status === 201) {
            return response.json();
          } else {
            // TODO: Show error message sent from server
            throw new Error("Cannot join game!");
          }
        })
        .then((data) => {
          console.log("Join game API response, redirecting to lobby, adding game ID to session storage " + data);
          sessionStorage.setItem(data.game_id, data.player_id);
          window.location.href = "lobby.html?id=" + data.game_id;
        })
        .catch((error) => {
          showNotification("Cannot join game!, no reason yet because its not been coded yet");
        });
    } else {
      if (!usernameInput.value) {
        usernameInput.style.borderColor = "red";
      }
      if (!gameIdInput.value) {
        gameIdInput.style.borderColor = "red";
      }
      setTimeout(() => {
        usernameInput.style.borderColor = "rgb(70, 70, 70)";
        gameIdInput.style.borderColor = "rgb(70, 70, 70)";
      }, 1000);
      return;
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input type="text" placeholder="Username" id="usernameInput" />
      </div>
      <div>
        <input type="text" placeholder="Game ID" id="gameIdInput" />
        <button type="submit" id="joinGameButton">
          Join!
        </button>
      </div>
    </form>
  );
}

function CreateGameForm() {
  return (
    <form>
      <div>
        <input placeholder="Username" id="usernameInput" />
      </div>
      <div>
        <button id="createGameButton">Create Game</button>
      </div>
    </form>
  );
}

function JoinGame() {
  return (
    <>
      <h1>Join Game</h1>

      <JoinGameForm />

      <p>or</p>
      <h1>Create Game</h1>
      <CreateGameForm />

      <div className="notification">
        <div className="notification-content">
          <span className="close-btn">&times;</span>
          <p id="notification-message">This is a notification message.</p>
        </div>
      </div>
    </>
  );
}

export default JoinGame;
