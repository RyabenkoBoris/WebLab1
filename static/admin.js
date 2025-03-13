async function getUsers(){
	const token = localStorage.getItem("access");
	if(!token) return;

	const socket = new WebSocket(`ws://127.0.0.1:8000/ws/admin/?token=${token}`);

	socket.onmessage = function(event) {
		const data = JSON.parse(event.data);
		const usersDiv = document.getElementById("online-users");
		usersDiv.innerHTML = "";  // Clear previous list

		if (data.online_users.length === 0) {
			usersDiv.innerHTML = "<p>No users online</p>";
			return;
		}

		data.online_users.forEach(user => {
			const userElement = document.createElement("div");
			userElement.classList.add("user");

			// Format the user information
			userElement.textContent = `Id: ${user.id}, Username: ${user.username}, Email: ${user.email}`;
			
			// Append the user element to the container
			usersDiv.appendChild(userElement);
		});
	};

	socket.onclose = function(event) {
		document.getElementById("online-users").innerHTML = "<p>Connection lost</p>";
	};
}

window.onload = getUsers;
