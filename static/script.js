document.addEventListener("DOMContentLoaded", function () {
    const loginBtn = document.getElementById("loginBtn");
    const chatSection = document.getElementById("chatSection");
    const roomList = document.getElementById("roomList");
    const createRoomBtn = document.getElementById("createRoomBtn");
    const messageList = document.getElementById("messageList");
    const messageInput = document.getElementById("messageInput");
    const sendBtn = document.getElementById("sendBtn");

    let userData;
    let socket;
    let currentRoom = null;

    // Telegram Login
    loginBtn.addEventListener("click", function () {
        const tg = window.Telegram.WebApp;
        const user = tg.initDataUnsafe.user;

        fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(user),
        })
        .then(res => res.json())
        .then(data => {
            userData = data.user;
            chatSection.style.display = "block";
            loadRooms();
            setupSocket();
        })
        .catch(console.error);
    });

    // Load Chat Rooms
    function loadRooms() {
        fetch("/chat/list")
            .then(res => res.json())
            .then(data => {
                roomList.innerHTML = "";
                data.rooms.forEach(room => {
                    const li = document.createElement("li");
                    li.textContent = room.room_name;
                    li.addEventListener("click", () => joinRoom(room.room_id));
                    roomList.appendChild(li);
                });
            });
    }

    // Create Chat Room
    createRoomBtn.addEventListener("click", function () {
        const roomName = prompt("Enter room name:");
        if (!roomName) return;

        fetch("/chat/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userData.user_id, room_name: roomName }),
        })
        .then(loadRooms);
    });

    // Setup WebSocket
    function setupSocket() {
        socket = io();
        socket.on("new_message", msg => {
            const li = document.createElement("li");
            li.textContent = msg.message;
            messageList.appendChild(li);
        });

        sendBtn.addEventListener("click", function () {
            const message = messageInput.value;
            if (message) socket.emit("message", { user_id: userData.user_id, room_id: currentRoom, message });
        });
    }
});
