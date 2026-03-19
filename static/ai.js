// ai.js

document.addEventListener("DOMContentLoaded", () => {
  // Toggle AI chat
  const aiBtn = document.getElementById("ai-btn");
  const chatDiv = document.getElementById("ai-chat");

  if (!aiBtn || !chatDiv) return;

  aiBtn.addEventListener("click", () => {
    chatDiv.style.display = chatDiv.style.display === "none" ? "block" : "none";
  });
});

async function sendMessage() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;

  const messagesDiv = document.getElementById("chat-messages");
  messagesDiv.innerHTML += `<div><b>You:</b> ${message}</div>`;
  input.value = "";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      credentials: "same-origin",
      body: JSON.stringify({message})
    });

    if (!res.ok) {
      messagesDiv.innerHTML += "<div><b>AI:</b> Error contacting server</div>";
      return;
    }

    const data = await res.json();
    messagesDiv.innerHTML += `<div><b>AI:</b> ${data.response}</div>`;
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  } catch (err) {
    messagesDiv.innerHTML += `<div><b>AI:</b> ${err}</div>`;
  }
}