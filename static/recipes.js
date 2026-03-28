// recipes.js
let allRecipes = [];

async function loadRecipes() {
  const res = await fetch("/recipes", { credentials: "same-origin" });
  allRecipes = await res.json();
  renderList(allRecipes);
}

// --- SEARCH FILTER (new) ---
function filterRecipes() {
  const query = document.getElementById("recipe-search").value.toLowerCase().trim();
  if (!query) {
    renderList(allRecipes);
    return;
  }
  const filtered = allRecipes.filter(r => {
    const nameMatch = r.name.toLowerCase().includes(query);
    const tagMatch  = r.tags?.some(t => t.toLowerCase().includes(query));
    return nameMatch || tagMatch;
  });
  renderList(filtered);
}

function renderList(recipes) {
  const list = document.getElementById("recipe-list");
  const noResults = document.getElementById("no-results");

  if (!recipes.length) {
    list.innerHTML = "";
    noResults.style.display = "block";
  } else {
    noResults.style.display = "none";
    list.innerHTML = recipes.map(renderRecipe).join("");
  }
}

function renderRecipe(r) {
  const image = r.image && !r.image.startsWith("REPLACE")
    ? r.image
    : "https://images.unsplash.com/photo-1569246294372-ed319c674f14?w=600&q=80";

  const tagPills = r.tags?.length
    ? r.tags.map(t => `<span class="tag-pill">${t}</span>`).join("")
    : '<span style="color:var(--text-muted);font-size:12px;">No tags</span>';

  return `
    <div class="recipe-card">
      <img src="${image}" class="recipe-img" alt="${r.name}" loading="lazy">
      <div class="recipe-card-body">
        <h3>${r.name}</h3>
        <div class="tags">${tagPills}</div>
        <a class="view-btn" href="/static/recipe.html?id=${r.id}">View Recipe →</a>
      </div>
    </div>
  `;
}

document.addEventListener("DOMContentLoaded", loadRecipes);