//const apiUrl = "https://l7sr6hzb-8000.uks1.devtunnels.ms"
const apiUrl = "http://127.0.0.1:8000";
//const apiUrl = "http://192.168.0.231:8000";

//const WebSocketUrl = "wss://l7sr6hzb-8000.uks1.devtunnels.ms"
const WebSocketUrl = "ws://127.0.0.1:8000";
//const WebSocketUrl = "ws://192.168.0.231:8000";

const gameIdInput = document.getElementById("gameIdInput");
const usernameInput = document.getElementById("usernameInput");


function joinGameButton() {
	// Get the values from the input fields
	const gameId = gameIdInput.value;
	const username = usernameInput.value;

	// Check if the inputs are valid
	if (checkInput(username, gameId)) {
		return;
	}

	// Check if the game ID is already in the session storage and redirect
	if (sessionStorage.getItem(gameId)){
		window.location.href = "lobby.html?id=" + gameId;
		return;
	}

	// Create the JSON data to send to the server
	var jsonData = {
		game_id: gameId,
		player_name: username,
	};
	var jsonString = JSON.stringify(jsonData);
	var apiEndpointUrl = apiUrl + "/join_game";

	fetch(apiEndpointUrl, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: jsonString,
	})
	.then((response) => {
		if (response.status === 201) {
			return response.json();
		} else {
			// TODO: Show error message send from server
			showNotification("Cannot join game!");
			throw new Error("Cannot join game!");
		}
	})
	.then((data) => {
		console.log(data);
		sessionStorage.setItem(data.game_id, data.player_id);
		window.location.href = "lobby.html?id=" + data.game_id;
	})
	.catch((error) => {
		console.error("There was a problem with the fetch operation:", error);
	});
}

// Function to handle the click event for the "Create game" button
function createGameButton() {
	var username = usernameInput.value;
	if (checkInput(username, null)) {
		return;
	}

	var apiEndpointUrl = apiUrl + "/create_game";
	var jsonData = {
		player_name: username,
	};
	var jsonString = JSON.stringify(jsonData);

	fetch(apiEndpointUrl, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: jsonString,
	})
	.then((response) => {
		return response.json();
	})
	.then((data) => {
			console.log(data);
			sessionStorage.setItem(data.game_id, data.player_id);
			window.location.href = "lobby.html?id=" + data.game_id;
	})
	.catch((error) => {
		console.error("There was a problem with the fetch operation:", error);
	});
}

function loadLobby() {
	// Get the values from the 
	const urlParams = new URLSearchParams(window.location.search);
	const gameId = urlParams.get("id");
	const playerId = sessionStorage.getItem(gameId); // Fetch the player ID stored under the game ID
	// Check session storage for the game ID, if it doesn't exist redirect to the index page
	if (!playerId){
		window.location.href = "index.html";
		return;
	}
	// Create the JSON data to send to the server
	var jsonData = {
		game_id: gameId,
		player_id: playerId,
	};
	var jsonString = JSON.stringify(jsonData);
	var apiEndpointUrl = apiUrl + "/lobby";
	// Send the request to the server
	fetch(apiEndpointUrl, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: jsonString,
	})
	.then((response) => {
		if (response.status === 200) {
			return response.json();
		} else {
			window.location.href = "index.html";
			return;
		}
	})
	.then((data) => {
		console.log("Data received:", data);

		const gameIdSpan = document.getElementById("gameId");
		const playerListDiv = document.getElementById("playerList");
		const playerNames = data.player_names;
		const playerCount = document.getElementById("playerCount");
		
		playerCount.textContent = playerNames.length + "/10";
		gameIdSpan.textContent = gameId;
		playerListDiv.innerHTML = "";
		
		for (const playerName of playerNames) {
			const playerElement = document.createElement("p");
			playerElement.textContent = playerName;
			playerListDiv.appendChild(playerElement);
		}

		var ws = new WebSocket(WebSocketUrl + "/ws");
		ws.onmessage = function(event) {
			console.log("reloading, received: " + event.data);
			ws.close(); // would otherwise create 2 websockets per player as the server sends the message to all players which creates a second websocket only for the new player
			loadLobby();
		};
	})
	.catch((error) => {
		console.error("Fetch error:", error);
	});
}

function showNotification(message) {
	const notification = document.querySelector('.notification');
	const notificationMessage = document.querySelector('#notification-message');
	notificationMessage.textContent = message;
	notification.style.display = 'block';
  
	setTimeout(() => {
	  closeNotification();
	}, 5000); // Auto-close the notification after 5 seconds
  }
  
  function closeNotification() {
	const notification = document.querySelector('.notification');
	notification.style.display = 'none';
  }

// Function to handle the click event for the "Join!" button
function checkInput(username, gameId) {
	let usernameEmpty = false;
	let gameIdEmpty = false;

	if (username !== null) {
		if (username.trim() === "") {
			usernameInput.style.borderColor = "red";
			usernameEmpty = true;
		}
	}

	if (gameId !== null) {
		if (gameId.trim() === "") {
			gameIdInput.style.borderColor = "red";
			gameIdEmpty = true;
		}
	}

	setTimeout(() => {
		if (usernameEmpty) {
			usernameInput.style.borderColor = "rgb(70, 70, 70)";
		}

		if (gameIdEmpty) {
			gameIdInput.style.borderColor = "rgb(70, 70, 70)";
		}
	}, 1000);

	return usernameEmpty || gameIdEmpty;
}


  