// app.js

// ---------- Auth Functions ----------

async function logout() {
  await fetch("/logout", {
    method: "POST",
    credentials: "same-origin"
  });
  location.href = "/static/index.html";
}

async function login() {
  const username = document.getElementById("username");
  const password = document.getElementById("password");
  const msg = document.getElementById("msg");

  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  });

  const data = await res.json();

  if (res.ok) {
    msg.innerText = "Logged in!";
    location.href = "/static/profile.html";
  } else {
    msg.innerText = data.error || "Login failed";
  }
}

async function registerUser() {
  const username = document.getElementById("register-username");
  const email = document.getElementById("register-email");
  const password = document.getElementById("register-password");
  const msg = document.getElementById("register-msg");

  if (!username.value || !email.value || !password.value) {
    msg.innerText = "Please fill in all fields";
    return;
  }

  const res = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({
      username: username.value,
      email: email.value,
      password: password.value
    })
  });

  const data = await res.json();

  if (res.ok) {
    msg.innerText = data.status || "Registration successful!";
  } else {
    msg.innerText = data.error || "Registration failed";
  }
}

// ---------- Shared helpers ----------

async function checkAuth() {
  const res = await fetch("/me", { credentials: "same-origin" });
  if (!res.ok) {
    location.href = "/static/login.html";
  }
}

// ---------- Consistent Navbar (used by all pages via id="nav-links") ----------
async function loadNavbar() {
  const nav = document.getElementById("nav-links");
  if (!nav) return;

  try {
    const res = await fetch("/me", { credentials: "same-origin" });

    if (res.ok) {
      // Logged-in nav
      nav.innerHTML = `
        <a href="/static/index.html">Home</a>
        <a href="/static/recipes.html">Recipes</a>
        <a href="/static/profile.html">Profile</a>
        <a href="#" onclick="logout()" class="nav-cta">Logout</a>
      `;
    } else {
      // Logged-out nav
      nav.innerHTML = `
        <a href="/static/index.html">Home</a>
        <a href="/static/recipes.html">Recipes</a>
        <a href="/static/login.html">Login</a>
        <a href="/static/register.html" class="nav-cta">Register</a>
      `;
    }
  } catch (err) {
    console.error("Navbar error:", err);
  }
}

// ---------- Chat toggle (shared across pages) ----------
function toggleChat() {
  const chatDiv = document.getElementById("ai-chat");
  if (!chatDiv) return;
  chatDiv.style.display = chatDiv.style.display === "none" ? "flex" : "none";
  // Use flex so the column layout works
  if (chatDiv.style.display === "flex") {
    chatDiv.style.flexDirection = "column";
  }
}

document.addEventListener("DOMContentLoaded", loadNavbar);