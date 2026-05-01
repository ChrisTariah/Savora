// ai.js

document.addEventListener("DOMContentLoaded", () => {
  const aiBtn = document.getElementById("ai-btn");
  if (!aiBtn) return;

  // Wire the button to the shared toggleChat defined in app.js
  aiBtn.addEventListener("click", toggleChat);
});

async function sendMessage() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;

  const messagesDiv = document.getElementById("chat-messages");

  // User bubble
  const userDiv = document.createElement("div");
  userDiv.className = "message user-message";
  userDiv.textContent = message;
  messagesDiv.appendChild(userDiv);
  input.value = "";
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({ message })
    });

    const botDiv = document.createElement("div");
    botDiv.className = "message bot-message";

    if (!res.ok) {
      botDiv.textContent = "Sorry, I couldn't reach the server.";
    } else {
      const data = await res.json();
      botDiv.textContent = data.response || "No response received.";
    }

    messagesDiv.appendChild(botDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  } catch (err) {
    const errDiv = document.createElement("div");
    errDiv.className = "message bot-message";
    errDiv.textContent = "Connection error. Please try again.";
    messagesDiv.appendChild(errDiv);
  }
}

// Allow sending with Enter key
document.addEventListener("DOMContentLoaded", () => {
  const chatInput = document.getElementById("chat-input");
  if (!chatInput) return;
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});