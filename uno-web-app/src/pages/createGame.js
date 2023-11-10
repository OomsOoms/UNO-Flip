import React from "react";
import "../styles/joinGame.css";
import apiUrl from "../index.js";

function CreateGameForm() {
  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();

    const usernameInput = document.getElementById("usernameInput");
    const username = usernameInput.value;

    // Check if the username is empty
    if (username) {
      // Send a POST request to the server to create a new player
      fetch(apiUrl + "/create_game", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          player_name: username,
        }),
      })
        // Check the response status
        .then((response) => {
          console.log("Create game button: " + response.status);
          return response.json();
        })
        // Redirect to the lobby page
        .then((data) => {
          console.log("Create game API response, redirecting to lobby " + data);
          sessionStorage.setItem(data.game_id, data.player_id);
          window.location.href = "lobby.html?id=" + data.game_id;
        })
        // Catch any errors and log them to the console
        .catch((error) => {
          console.error("There was a problem with the fetch operation:", error);
        });
    } else {
      // Make the input boxes red for 1 second if they are empty
      if (!usernameInput.value) {
        usernameInput.style.borderColor = "red";
      }
      setTimeout(() => {
        usernameInput.style.borderColor = "rgb(70, 70, 70)";
      }, 1000);
      return;
    }
  };

  return (
    <>
      <h1>Create Game</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <input type="text" placeholder="Username" id="usernameInput" />
        </div>
        <div>
          <button type="submit" id="createGameButton">
            Create!
          </button>
        </div>
      </form>
    </>
  );
}

export default CreateGameForm;
