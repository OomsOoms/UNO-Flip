import React from "react";
import "../styles/joinGame.css";
import apiUrl from "../index.js";

function JoinGameForm() {
  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();

    // Get input values
    const usernameInput = document.getElementById("usernameInput");
    const username = usernameInput.value;
    const gameIdInput = document.getElementById("gameIdInput");
    const gameId = parseInt(gameIdInput.value);

    // Check if game ID is a number
    if (isNaN(gameId)) {
      console.log("Game ID must be a number");
      return;
    }

    // Check if the game ID is already in the session storage and redirect
    if (sessionStorage.getItem(gameId)) {
      console.log("Redirecting to previous joined game in session storage");
      window.location.href = "lobby.html?id=" + gameId;
      return;
    }

    // Check if the username and game ID are not empty
    if (username && gameId) {
      // Send a POST request to the server to create a new player
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
        // Check the response status
        .then((response) => {
          console.log("Join game button: " + response.status);
          if (response.status === 201) {
            // 201 PLayer created
            return response.json();
          } else {
            throw new Error("Cannot join game!");
          }
        })
        // Redirect to the lobby page
        .then((data) => {
          console.log("Join game API response, redirecting to lobby, adding game ID to session storage " + data);
          sessionStorage.setItem(data.game_id, data.player_id);
          window.location.href = "lobby.html?id=" + data.game_id;
        })
        // Catch any errors and log them to the console
        .catch((error) => {
          //TODO: Show error message sent from server as notification
          console.log(error);
        });
    } else {
      // Make the input boxes red for 1 second if they are empty
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
    <>
      <h1>Join Game</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <input type="text" placeholder="Username" id="usernameInput" />
        </div>
        <div>
          <input type="text" placeholder="Game ID" id="gameIdInput" />
        </div>
        <div>
          <button type="submit" id="joinGameButton">
            Join!
          </button>
        </div>
      </form>
    </>
  );
}



export default JoinGameForm;
