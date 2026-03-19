

async function loadRecipes() {
  const res = await fetch("/recipes", { credentials: "same-origin" });
  const recipes = await res.json();

  const list = document.getElementById("recipe-list");

  list.innerHTML = recipes.length
    ? recipes.map(renderRecipe).join("")
    : "<p>No recipes yet 🍳</p>";
}

function renderRecipe(r) {
  const image = r.image || "https://images.unsplash.com/photo-1569246294372-ed319c674f14";

  const tags = r.tags?.length
    ? `<p class="tags">${r.tags.join(", ")}</p>`
    : "";

  return `
    <div class="recipe-card">
      <img src="${image}" class="recipe-img">
      <h3>${r.name}</h3>
      ${tags}
      <a class="view-btn" href="/static/recipe.html?id=${r.id}">View Recipe</a>
    </div>
  `;
}



document.addEventListener("DOMContentLoaded", loadRecipes);
