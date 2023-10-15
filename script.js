const apiUrl = "http://192.168.0.231:8000";

// Function to handle the click event for the "Join!" button
const gameIdInput = document.getElementById("gameIdInput");
const usernameInput = document.getElementById("usernameInput");

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

function getCookieValue(key) {
    const cookies = document.cookie.split("; ");
    
    for (const cookie of cookies) {
        const [cookieKey, cookieValue] = cookie.split("=");
        if (cookieKey === key) {
            return cookieValue;
        }
    }
    
    return null;  // Return null if no cookie with the provided game ID is found
}

function joinGameButton() {
	var gameid = gameIdInput.value;
	var username = usernameInput.value;

	if (checkInput(username, gameid)) {
		return;
	}

	if (getCookieValue(gameid)){
		window.location.href = "lobby.html?game_id=" + gameid;
		return;
	}

	var apiEndpointUrl = apiUrl + "/join_game";
	var jsonData = {
		game_id: gameid,
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
		if (!response.ok) {
			throw new Error("Network response was not ok");
		}
		return response.json();
	})
	.then((data) => {
		if (data.detail === "Game is full") {
			console.error("Game is full");
		} else {
			document.cookie = `${data.game_id}=${data.player_id}; `;
			window.location.href = "lobby.html?game_id=" + data.game_id;
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
			document.cookie = `${data.game_id}=${data.player_id}; `;
			window.location.href = "lobby.html?game_id=" + data.game_id;
		})
		.catch((error) => {
			console.error("There was a problem with the fetch operation:", error);
		});
}

function loadLobby() {
	sessionStorage.setItem('username', 'john_doe');  // Store the username in localStorage
	sessionStorage.setItem('username', 'john_doe');  // Store the username in localStorage
	sessionStorage.setItem('username', 'john_doe');  // Store the username in localStorage
	console.log(cookies = document.cookie);
	const urlParams = new URLSearchParams(window.location.search);
	const gameId = urlParams.get('game_id');
	const playerId = getCookieValue(gameId)

	// If the user enters an invalid id (e.g. a game that doesn't exist), they will be directed to index
	if (!getCookieValue(gameId)){
		console.error("Invalid game ID");
		window.location.href = "index.html";
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
