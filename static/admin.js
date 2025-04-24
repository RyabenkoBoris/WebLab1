async function getUsers() {
    const token = localStorage.getItem("access");
    if (!token) return;

    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/admin/?token=${token}`);
    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.online_users) {
            const usersDiv = document.getElementById("user-list");
            usersDiv.innerHTML = "";

            if (data.online_users.length === 0) {
                usersDiv.innerHTML = "<p>No users online</p>";
                return;
            }

            data.online_users.forEach(user => {
                const userElement = document.createElement("div");
                userElement.classList.add("user");
                userElement.textContent = `Id: ${user.id}, Username: ${user.username}, Email: ${user.email}`;
                usersDiv.appendChild(userElement);
            });
        }

        if (data.operation_status) {
            const status = data.operation_status;
            const table = document.getElementById("operation-status-table").querySelector("tbody");
            const row = table.insertRow();
            row.insertCell(0).innerText = status.result.data[0];
            row.insertCell(1).innerText = status.result.data[1];
            row.insertCell(2).innerText = status.result.data[2];
            row.insertCell(3).innerText = status.completion_time;
        }
    };

    socket.onclose = function(event) {
        document.getElementById("user-list").innerHTML = "<p>Connection lost</p>";
    };
}

window.onload = getUsers;
