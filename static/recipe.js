// ---------- DOM Elements ----------
const nameEl = document.getElementById("recipe-name");
const instructionsEl = document.getElementById("recipe-instructions");
const ingredientsEl = document.getElementById("recipe-ingredients");
const imageEl = document.getElementById("recipe-image");

// ---------- Get recipe ID from URL ----------
const recipeId = new URLSearchParams(window.location.search).get("id");

async function loadRecipe() {
  if (!recipeId) {
    nameEl.innerText = "No recipe selected";
    return;
  }

  try {
    const res = await fetch(`/recipes?id=${recipeId}`, { credentials: "same-origin" });
    if (!res.ok) {
      nameEl.innerText = "Recipe not found";
      return;
    }

    const r = await res.json();
    imageEl.src = r.image || "/static/images.jpg";
    nameEl.innerText = r.name;
    instructionsEl.innerText = r.instructions;
    ingredientsEl.innerHTML = r.ingredients
      .map(i => `<li>${i.name} - ${i.quantity}</li>`)
      .join("");
    const tagsEl = document.getElementById("recipe-tags");  // Add this <ul> in recipe.html
    tagsEl.innerHTML = r.tags ? r.tags.map(t => `<li>${t}</li>`).join("") : "";
  } catch (err) {
    console.error(err);
    nameEl.innerText = "Error loading recipe";
  }
}

document.addEventListener("DOMContentLoaded", loadRecipe);