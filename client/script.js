const apiUrl = "http://127.0.0.1:8000";
//const apiUrl = "http://192.168.0.231:8000";
//const apiUrl = "https://xw2fbn56-8000.uks1.devtunnels.ms"

const gameIdInput = document.getElementById("gameIdInput");
const usernameInput = document.getElementById("usernameInput");

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

function joinGameButton() {
	// Disable the button to prevent multiple clicks
	joinGameButton.disabled = true;
	const gameId = gameIdInput.value;
	const username = usernameInput.value;

	// If the username is invalid return
	if (checkInput(username, gameId)) {
		console.log("Invalid details");
		return;
	} 
	// If the user already has the gamein their session
	if (sessionStorage.getItem(gameId)) {
		console.log("Already joined game");
		window.location.href = "lobby.html?game_id=" + gameId;
		return;
	}

	var apiEndpointUrl = apiUrl + "/join_game";
	var jsonData = {
		game_id: gameId,
		player_name: username,
	};
	var jsonString = JSON.stringify(jsonData);
	console.log(jsonString);

	fetch(apiEndpointUrl, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: jsonString,
	})
	.then((response) => {
		console.log("Response status: " + response.status)
		if (response.status !== 200) {
			console.log("Status not 200");
			showNotification("Invalid game ID");
			return;
		} else {
			return response.json();
		}
	})
	.then((data) => {
		if (data.detail === "Game is full") {
			showNotification("Game is full");
			console.error("Game is full");
			return;
		} if(data.detail === "Game has already started") {
			showNotification("Game has already started");
			console.log("Game has already started");
			return;
		} else {
			console.log("Found game")
			sessionStorage.setItem(data.game_id, data.player_id)
			//window.location.href = "lobby.html?game_id=" + data.game_id;
		}
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
			sessionStorage.setItem(data.game_id, data.player_id)
			window.location.href = "lobby.html?game_id=" + data.game_id;
		})
		.catch((error) => {
			console.error("There was a problem with the fetch operation:", error);
		});
}

function loadLobby() {
	const urlParams = new URLSearchParams(window.location.search);
	const gameId = urlParams.get('game_id');
	const playerId = sessionStorage.getItem(gameId); // Fetch the player ID stored under the game ID

	// If the user enters an invalid id (e.g. a game that doesn't exist), they will be directed to index
	if (!playerId){
		console.error("Invalid game ID");
		window.location.href = "index.html";
		return;
	}

	var apiEndpointUrl = apiUrl + "/lobby";
	var jsonData = {
		game_id: gameId,
		player_id: playerId,
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
		if (response.status === 400) {
			window.location.href = "index.html";
		} else {
			return response.json();
		}
	})
	.then((data) => {
		console.log("Data received:", data);

		const gameIdSpan = document.getElementById("gameId");
		const playerListDiv = document.getElementById("playerList");
		const playerNames = data.player_names;

		gameIdSpan.textContent = gameId;
		playerListDiv.innerHTML = "";
		
		for (const playerName of playerNames) {
			const playerElement = document.createElement("p");
			playerElement.textContent = playerName;
			playerListDiv.appendChild(playerElement);
		}
	})
	.catch((error) => {
		console.error("Fetch error:", error);
	});
}



  