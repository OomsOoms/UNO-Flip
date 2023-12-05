import React, { useState, useEffect } from "react";
import "../scss/gameLobby.scss";
import { apiUrl, webSocketUrl } from "../index.js";

export default function GameRoom() {
  const urlParams = new URLSearchParams(window.location.search);

  const gameId = urlParams.get("id");
  const playerId = sessionStorage.getItem(gameId);

  document.title = "UNO | Lobby " + gameId;

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
      // These messages change the state of the component
      if (data.type === "game" || data.type === "lobby" || data.type === "game_over") {
        data.ws = ws;
        setLobbyData(data);
      // These messages do not change the state of the component
      } else if (data.type === "call_uno") {
        console.log(`${data.playerName} called UNO!`);
      }
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
    case "game_over":
      return <p>Game Over</p>;
    default:
      return <p>Loading...</p>;
  }
}

const Lobby = ({ lobbyData: { playerNames, isHost, gameId, playerId } }) => {

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

function Game({ lobbyData: { discard, playerHand, isTurn, unoCalled, ws } }) {

  const pickCard = () => {
    ws.send(JSON.stringify({
      type: "pick_card",
    }));
  };

  const callUno = () => {
    ws.send(JSON.stringify({
      type: "call_uno",
    }));
  };


  
  return (
    <div id="gameContainer">
      <div id="discardContainer">
        <div
          style={{ backgroundColor: discard.colour }}
          className="card"
        >
          {discard.action}
        </div>
        <button
          id="callUnoButton"
          onClick={callUno}
          className={`${unoCalled ? "disabled" : ""}`}
        >
          Call UNO!
        </button>
        <button
          id="pickCardButton"
          onClick={pickCard}
          className={`${isTurn ? "" : "disabled"}`}
        >
          Pick up card
        </button>
      </div>
      
      {playerHand.map((card, index) => (
        <Card 
          key={`${card.colour}-${card.action}-${index}`} 
          index={index}
          card={card}
          ws={ws}
        />
      ))}
    </div>
  );
}

function Card({ index, card: { colour, action, isPlayable }, ws }) {
  
  const selectCard = () => {
    ws.send(JSON.stringify({
      type: "play_card",
      index: index,
    }));
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