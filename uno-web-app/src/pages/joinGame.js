import React, { useState } from "react";
import "../styles/enterGameForms.css";
import { apiUrl } from "../index.js";

function JoinGameForm() {
  const [username, setUsername] = useState("");
  const [usernameStyle, setUsernameStyle] = useState("");
  const [gameId, setGameId] = useState("");
  const [gameIdStyle, setgameIdStyle] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    if (isNaN(gameId)) {
      console.log("Game ID must be a number");
      return;
    }
    if (sessionStorage.getItem(gameId)) {
      console.log("Redirecting to previous joined game in session storage");
      window.location.href = "lobby?id=" + gameId;
      return;
    }
    if (username && parseInt(gameId)) {
      const requestBody = {
        game_id: gameId,
        player_name: username,
      };

      const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      };

      const url = apiUrl + "/join_game";

      fetch(url, options)
        .then((response) => {
          console.log(`Join game button: ${response.status}`);
          if (response.status === 201) {
            // If the response status is 201, the player was created successfully)
            return response.json();
          } else {
            // If the response status is not 201, throw an error
            throw new Error("Cannot join game!");
          }
        })
        .then((data) => {
          console.log("Redirecting to lobby, adding game ID to session storage");
          // Add the game ID and player ID to session storage
          sessionStorage.setItem(data.game_id, data.player_id);
          // Redirect the user to the lobby page with the game ID as a query parameter
          window.location.href = "lobby?id=" + data.game_id;
        })
        // Catch any errors and log them to the console
        .catch((error) => {
          //TODO: Show error message sent from server as notification
          console.log(error);
        });
    } else {
      if (!username) {
        setUsernameStyle("red");
      }
      if (!gameId) {
        setgameIdStyle("red");
      }
      setTimeout(() => {
        setUsernameStyle("");
        setgameIdStyle("");
      }, 1000);
      return;
    }
  };

  return (
    <>
      <h1>Join Game</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <input type="text" placeholder="Username" className={usernameStyle} value={username} onChange={(event) => setUsername(event.target.value)} />
        </div>
        <div>
          <input type="text" placeholder="Game ID" className={gameIdStyle} value={gameId} onChange={(event) => setGameId(event.target.value)} />
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
