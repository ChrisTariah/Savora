const userId = new URLSearchParams(window.location.search).get("id");

// ---------- Load Profile ----------
async function loadUser() {
  const res = await fetch(`/user-profile?id=${userId}`);

  if (!res.ok) {
    document.getElementById("username").innerText = "User not found";
    return;
  }

  const user = await res.json();

  document.getElementById("username").innerText = user.username;
  document.getElementById("likes").innerText = user.likes;
  document.getElementById("views").innerText = user.views;

  const recipesEl = document.getElementById("recipes");

  recipesEl.innerHTML = user.recipes.length
    ? user.recipes.map(r => `
        <div class="recipe-card">
          <img src="${r.image || 'https://images.unsplash.com/photo-1569246294372-ed319c674f14'}" class="recipe-img">
          <h3>${r.name}</h3>
          <a class="view-btn" href="/static/recipe.html?id=${r.id}">View Recipe</a>
        </div>
      `).join("")
    : "<p>No recipes yet 🍳</p>";
}

// ---------- Track View ----------
async function trackView() {
  await fetch("/view-profile", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ userID: userId })
  });
}

// ---------- Like Profile ----------
async function likeProfile() {
  const res = await fetch("/like-profile", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ userID: userId })
  });

  if (res.ok) {
    alert("Liked!");
    loadUser(); // refresh count
  } else {
    alert("Login required");
  }
}

async function checkFollow() {
  const res = await fetch(`/is-following?id=${userId}`, {
    credentials: "same-origin"
  });

  const data = await res.json();

  document.getElementById("follow-btn").innerText =
    data.following ? "Unfollow" : "Follow";
}

async function toggleFollow() {
  const resCheck = await fetch(`/is-following?id=${userId}`, {
    credentials: "same-origin"
  });

  const data = await resCheck.json();
  const endpoint = data.following ? "/unfollow" : "/follow";

  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ userID: userId })
  });

  if (res.ok) {
    checkFollow(); // refresh button
  }
}
// ---------- Init ----------
document.addEventListener("DOMContentLoaded", () => {
  loadNavbar();
  loadUser();
  trackView();
  checkFollow();
});