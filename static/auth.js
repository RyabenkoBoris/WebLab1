const API_BASE = "http://127.0.0.1:8000";

async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE}/account/token/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    if (response.ok) {
        localStorage.setItem("access", data.access);
        localStorage.setItem("refresh", data.refresh);

        document.getElementById("loginForm").style.display = "none";
        document.getElementById("logoutBtn").style.display = "block";
        document.getElementById("adminLinkContainer").style.display = "none"; 
        
        await fetchUserId(); // Get user ID after login
        loadChats();
    } else {
        alert("Login failed!");
    }
}

async function fetchUserId() {
    const token = localStorage.getItem("access");

    if (!token) {
        console.error("No token found.");
        return;
    }

    const response = await fetch(`${API_BASE}/account/profile/`, {
        method: "GET",
        headers: { 
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });
	
	
    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("user_id", data.id);
    } else {
        console.error("Failed to fetch user ID.");
    }
}


async function refreshAccessToken() {
    const refreshToken = localStorage.getItem("refresh");

    if (!refreshToken) {
        alert("Session expired. Please log in again.");
        return;
    }

    const response = await fetch(`${API_BASE}/account/token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken })
    });

    const data = await response.json();
    if (response.ok) {
        localStorage.setItem("access", data.access);
    } else {
        alert("Session expired. Please log in again.");
        logout();
    }
}

async function loadChats() {
    let token = localStorage.getItem("access");
    if (!token) return; // Don't fetch if not logged in

    let response = await fetch(`${API_BASE}/chat/`, {
        headers: { "Authorization": `Bearer ${token}` }
    });

    if (response.status === 401) {
        await refreshAccessToken();
        token = localStorage.getItem("access");

        response = await fetch(`${API_BASE}/chat/`, {
            headers: { "Authorization": `Bearer ${token}` }
        });
    }

    if (response.ok) {
        document.getElementById("loginForm").style.display = "none"; // Hide login form
        document.getElementById("logoutBtn").style.display = "block"; // Show logout button
        document.getElementById("adminLinkContainer").style.display = "block"; // Show logout button
        
        const chats = await response.json();
        const chatList = document.getElementById("chatList");
        chatList.innerHTML = "";
        chats.forEach(chat => {
            const li = document.createElement("li");
            li.innerHTML = `<a href="chat.html?chat_id=${chat.id}">Chat ${chat.id}</a>`;
            chatList.appendChild(li);
        });
    } else {
        alert("Failed to load chats.");
    }
}

function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    location.reload();
}

window.onload = function() {
    if (localStorage.getItem("access")) {
        document.getElementById("loginForm").style.display = "none";
        document.getElementById("logoutBtn").style.display = "block";
        loadChats();
    }
};
