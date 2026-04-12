// =============================
// TOGGLE CHAT
// =============================
function toggleChat() {
    const chat = document.getElementById("chatContainer");

    if (chat.style.display === "flex") {
        chat.style.display = "none";
    } else {
        chat.style.display = "flex";
    }
}

// =============================
// ADD MESSAGE
// =============================
function addMessage(sender, text) {
    const chatBody = document.getElementById("chatBox");

    const msg = document.createElement("div");
    msg.className = "message " + sender;
    msg.innerText = text;

    chatBody.appendChild(msg);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// =============================
// SEND MESSAGE
// =============================
function sendMessage() {
    const input = document.getElementById("userInput");
    const text = input.value.trim();

    if (!text) return;

    addMessage("user", text);
    input.value = "";

    sendToBot(text);
}

// =============================
// QUICK BUTTONS (FIXED)
// =============================
function sendQuick(text) {
    addMessage("user", text);
    sendToBot(text);
}

// =============================
// SEND TO BACKEND
// =============================
function sendToBot(message) {
    addMessage("bot", "⏳ Thinking...");

    fetch("/chatbot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: message })
    })
    .then(res => res.json())
    .then(data => {
        // remove last "Thinking..." message
        const chatBody = document.getElementById("chatBox");
        chatBody.removeChild(chatBody.lastChild);

        addMessage("bot", data.response);
    })
    .catch(() => {
        addMessage("bot", "⚠️ Server error");
    });
}

// =============================
// ENTER KEY SUPPORT
// =============================
document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("userInput");

    if (input) {
        input.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                sendMessage();
            }
        });
    }
});
