async function loadFeed() {
  const res = await fetch("/feed", { credentials: "same-origin" });

  if (!res.ok) {
    document.getElementById("feed-list").innerHTML =
      "<p>Login to see your feed</p>";
    return;
  }

  const recipes = await res.json();
  const list = document.getElementById("feed-list");

  list.innerHTML = recipes.length
    ? recipes.map(r => `
        <div class="recipe-card">

          <img src="${r.image}" class="recipe-img">

          <h3>${r.name}</h3>
          <p>by ${r.username}</p>

          <a href="/static/recipe.html?id=${r.id}">View</a>

          <button onclick="toggleLike(${r.id}, this)">
            ❤️ ${r.likes || 0}
          </button>

          <div class="comments">
            <div id="comments-${r.id}"></div>
            <input placeholder="Write a comment..."
                   onkeydown="addComment(event, ${r.id})">
          </div>

        </div>
      `).join("")
    : "<p>No recipes yet. Follow people 👀</p>";

  recipes.forEach(r => loadComments(r.id));
}


async function toggleLike(id, btn) {
  const res = await fetch("/feed/like", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    credentials: "same-origin",
    body: JSON.stringify({ recipe_id: id })
  });

  const data = await res.json();
  btn.innerText = `❤️ ${data.count}`;
  btn.classList.toggle("liked", data.liked);
}
async function addComment(e, id) {
  if (e.key !== "Enter") return;

  await fetch("/feed/comment", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    credentials: "same-origin",
    body: JSON.stringify({
      recipe_id: id,
      text: e.target.value
    })
  });

  e.target.value = "";
}


document.addEventListener("DOMContentLoaded", () => {
  loadNavbar();
  loadFeed();
});