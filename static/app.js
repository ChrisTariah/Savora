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

async function register() {
  const username = document.getElementById("username");
  const password = document.getElementById("password");
  const msg = document.getElementById("msg");

  const res = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  });

  const data = await res.json();
  msg.innerText = data.status || data.error || "Unknown error";
}

async function logout() {
  await fetch("/logout", {
    method: "POST",
    credentials: "same-origin"
  });
  location.href = "/static/index.html";
}

// ---------- Shared helper ----------
async function checkAuth() {
  const res = await fetch("/me", { credentials: "same-origin" });
  if (!res.ok) {
    location.href = "/static/login.html";
  }
}



async function loadNavbar() {
  const nav = document.getElementById("nav-links");
  if (!nav) return;

  try {
    const res = await fetch("/me", { credentials: "same-origin" });

    if (res.ok) {
      nav.innerHTML = `
        <a href="/static/index.html">Home</a>
        <a href="/static/profile.html">Profile</a>
        <a href="#" onclick="logout()">Logout</a>
      `;
    } else {
      nav.innerHTML = `
        <a href="/static/index.html">Home</a>
        <a href="/static/login.html">Login</a>
      `;
    }
  } catch (err) {
    console.error("Navbar error:", err);
  }
}


document.addEventListener("DOMContentLoaded", loadNavbar);
