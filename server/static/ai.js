// ai.js

document.addEventListener("DOMContentLoaded", () => {
  const aiBtn = document.getElementById("ai-btn");
  if (!aiBtn) return;

  // Wire the button to the shared toggleChat defined in app.js
  aiBtn.addEventListener("click", toggleChat);
});
function parseRecipes(text) {
  const recipes = [];

  const regex = /Recipe:\s*(.*?)\s*ID:\s*(\d+)\s*Description:\s*(.*?)(?=Recipe:|$)/gis;

  let match;
  while ((match = regex.exec(text)) !== null) {
    recipes.push({
      name: match[1].trim(),
      id: match[2].trim(),
      description: match[3].trim()
    });
  }

  return recipes;
}
function createRecipeCard(recipe) {
  const card = document.createElement("div");
  card.className = "recipe-card";

  card.innerHTML = `
    <div class="recipe-title">${recipe.name}</div>
    <div class="recipe-desc">${recipe.description}</div>
  `;

  card.onclick = () => {
    window.location.href = `/static/recipe.html?id=${recipe.id}`;
  };

  return card;
}
async function sendMessage() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;

  const messagesDiv = document.getElementById("chat-messages");

  // prevent spam clicking
  input.disabled = true;

  // ---------------- USER MESSAGE ----------------
  const userDiv = document.createElement("div");
  userDiv.className = "message user-message";
  userDiv.textContent = message;
  messagesDiv.appendChild(userDiv);

  input.value = "";
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  // ---------------- BOT MESSAGE (empty, will fill live) ----------------
  const botDiv = document.createElement("div");
  botDiv.className = "message bot-message";
  botDiv.textContent = "Thinking...";
  messagesDiv.appendChild(botDiv);

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({ message })
    });

    if (!res.body) {
      botDiv.textContent = "No response stream.";
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();


    // ---------------- STREAM LOOP ----------------
let fullText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      fullText += chunk;

      botDiv.textContent = fullText; // show typing

      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    // AFTER stream ends → render cards
    const recipes = parseRecipes(fullText);

    if (recipes.length > 0) {
      botDiv.innerHTML = "";

      recipes.forEach(r => {
        botDiv.appendChild(createRecipeCard(r));
      });
    }
      } catch (err) {
        botDiv.textContent = "Connection error. Please try again.";
      } finally {
        input.disabled = false;
        input.focus();
      }
}

document.addEventListener("DOMContentLoaded", () => {
  const chatInput = document.getElementById("chat-input");
  if (!chatInput) return;

  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
});