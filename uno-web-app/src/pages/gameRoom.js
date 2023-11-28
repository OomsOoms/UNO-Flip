import React, { useState, useEffect } from "react";
import "../scss/gameLobby.scss";
import { apiUrl, webSocketUrl } from "../index.js";

export default function GameRoom() {
  const urlParams = new URLSearchParams(window.location.search);

  const gameId = urlParams.get("id");
  const playerId = sessionStorage.getItem(gameId);

  // When the value changes the component will re-render
  const [lobbyData, setLobbyData] = useState({});

  useEffect(() => {
    const ws = new WebSocket(`${webSocketUrl}/lobby?game_id=${gameId}&player_id=${playerId}`);

    ws.onopen = () => {
      console.log("WebSocket connection opened");
    };
    ws.onclose = () => {
      console.log("WebSocket connection disconnected");
    };
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLobbyData(data);
      console.log("Received data from websocket: ", data);
    };
    ws.onerror = () => {
      if (document.referrer.includes(window.location.origin)) {
        window.history.back();
      } else {
        window.location.href = "/";
      }
      return;
    }
    return () => {
      console.log("component unmounted");
      ws.close();
    };

  }, [gameId, playerId]);

  switch (lobbyData.type) {
    case "lobby":
      return <Lobby lobbyData={lobbyData} />;
    case "game":
      return <Game lobbyData={lobbyData} />;
    default:
      return <p>Loading...</p>;
  }
}

const Lobby = ({ lobbyData: { playerNames, isHost, gameId, playerId } }) => {
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
      .then((data) => console.log("Start game button detail:", data.detail));
  };

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
        {playerNames.map((playerName, index) => (
          <p key={index}>{playerName}</p>
        ))}

        {isHost && (
          <button id="startGameButton" onClick={startGame} disabled={playerNames.length < 2} className={playerNames.length < 2 ? "disabled" : ""}>
            Start Game
          </button>
        )}
      </div>
    </>
  );
}

function Card({ index, card: { colour, action, isPlayable } }) {
  
  const selectCard = () => {
    console.log(index)
  }

  return (
    <button
      style={{ backgroundColor: colour }}
      className={`card playable ${isPlayable ? "" : "disabled"}`}
      onClick={selectCard}
    >
      {action}
    </button>
  );
}

function Game({ lobbyData: { discard, playerHand, opponentHands } }) {
  return (
    <div id="gameContainer">
      <div id="opponentContainer">
        <p>{JSON.stringify(opponentHands)}</p>
      </div>

      <div id="discardContainer">
        <div
          style={{ backgroundColor: discard.colour }}
          className="card"
        >
          {discard.action}
        </div>
      </div>
      
      {playerHand.map((card, index) => (
        <Card 
          key={`${card.colour}-${card.action}-${index}`} 
          index={index}
          card={card}
        />
      ))}
    </div>
  );
}