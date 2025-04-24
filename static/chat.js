const API_BASE = "http://127.0.0.1:8000";
let chatSocket = null;
let chatId = null;
let isConnected = false;

const urlParams = new URLSearchParams(window.location.search);
chatId = urlParams.get("chat_id");

const userId = localStorage.getItem("user_id");

async function connectWebSocket() {
    const token = localStorage.getItem("access");
    if (!token || !chatId || isConnected) return;

    chatSocket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${chatId}/?token=${token}`);

    chatSocket.onopen = function () {
        console.log("Connected to WebSocket.");
        isConnected = true;
    };

    chatSocket.onmessage = function (event) {
		const data = JSON.parse(event.data);
		console.log("Received message:", data);
		displayMessage(data.sender, data.message);
	};


    chatSocket.onerror = function (error) {
        console.error("WebSocket error:", error);
    };

    chatSocket.onclose = function () {
        console.log("WebSocket closed. Reconnecting in 3 seconds...");
        isConnected = false;
        setTimeout(connectWebSocket, 3000);
    };
}
async function sendMessage() {
    const messageInput = document.getElementById("messageInput").value;

    if (!messageInput || !chatSocket || chatSocket.readyState !== WebSocket.OPEN) {
        alert("WebSocket is not connected.");
        return;
    }
	
    const messageData = {
        user: userId,
        chat: chatId,
        text: messageInput,
    };

    chatSocket.send(JSON.stringify(messageData));

    document.getElementById("messageInput").value = "";
}
async function loadMessages() {
    const token = localStorage.getItem("access");

    if (!chatId) return;

    const response = await fetch(`${API_BASE}/chat/message/${chatId}/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.ok) {
        const messages = await response.json();
        const messagesContainer = document.getElementById("messages");
        messagesContainer.innerHTML = "";

        messages.forEach(msg => {
            displayMessage(msg.user ? msg.user : '', msg.text);
        });

        if (!isConnected) {
            connectWebSocket();
        }
    } else {
        alert("Failed to load messages.");
    }
}

function displayMessage(sender, message) {
    const messagesContainer = document.getElementById("messages");
    const msgElement = document.createElement("p");
    msgElement.innerHTML = sender ? `<strong>${sender}:</strong> ${message}` : `${message}`;
    messagesContainer.appendChild(msgElement);
}

window.onload = loadMessages;
