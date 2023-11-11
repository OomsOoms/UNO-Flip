import React, { useState } from "react";
import "../scss/enterGameForms.scss";
import { apiUrl } from "../index.js";

function CreateGameForm() {
  document.title = "UNO | Create Game"
  // Create a state variable for the username
  const [username, setUsername] = useState("");
  const [usernameStyle, setUsernameStyle] = useState("enterGameInput");

  // Handle the form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    // If the username is not empty create a POST request to send to the server
    if (username) {
      const requestBody = {
        player_name: username,
      };

      const options = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      };

      const url = apiUrl + "/create_game";
      // Send the POST request to the server
      fetch(url, options)
        .then((response) => {
          console.log("Create game button: " + response.status);
          return response.json();
        })
        .then((data) => {
          console.log("Redirecting to lobby, added game ID to session storage");
          // Add the game ID and player ID to session storage
          sessionStorage.setItem(data.game_id, data.player_id);
          // Redirect the user to the lobby page with the game ID as a query parameter
          window.location.href = "lobby?id=" + data.game_id;
        })
        .catch((error) => {
          //TODO: Show error message sent from server as notification
          console.error("There was a problem with the fetch operation:", error);
        });
    } else {
      // If the username is empty, add a red border to the input field for 1 second
      if (!username) {
        setUsernameStyle("enterGameInput redBorder");
      }
      setTimeout(() => {
        setUsernameStyle("enterGameInput");
      }, 1000);
      return;
    }
  };

  return (
    <>
      <h1>Create Game</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <input type="text" placeholder="Username" className={usernameStyle} value={username} onChange={(event) => setUsername(event.target.value)} />
        </div>
        <div>
          <button type="submit" className={"enterGameInput"} id="joinGameButton">
            Create!
          </button>
        </div>
      </form>
    </>
  );
}

export default CreateGameForm;
