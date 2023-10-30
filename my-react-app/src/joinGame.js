import React, { useState } from 'react';
import "./joinGame.css"

function JoinGameForm() {
  const [gameId, setGameId] = useState(''); // Use state to manage the gameId input

  const handleGameIdChange = (event) => {
    setGameId(event.target.value); // Update the gameId state when input changes
  };

  return (
    <form action="/lobby">
      <div>
        <input type="text" placeholder="Username" id="usernameInput"/>
      </div>
      <div>
        <input
          placeholder="Game ID"
          id="gameIdInput"
          name="id" // Add a name attribute for the gameId input
          value={gameId}
          onChange={handleGameIdChange} // Update the gameId state when input changes
        />
        <button type="submit" id="joinGameButton">Join!</button>
      </div>
    </form>
  );
}

function CreateGameForm() {
  return (
    <form>
      <div>
        <input placeholder="Username" id="usernameInput"/>
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
            <span className="close-btn" >&times;</span>
            <p id="notification-message">This is a notification message.</p>
          </div>
        </div>
      </>
  );
}

export default JoinGame;
