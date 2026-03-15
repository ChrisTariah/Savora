// ---------- DOM Elements ----------
const msg = document.getElementById("msg");
const username = document.getElementById("username");
const password = document.getElementById("password");

const nameInput = document.getElementById("name");
const instructionsInput = document.getElementById("instructions");
const ingredientNameInput = document.getElementById("ingredient-name");
const ingredientQtyInput = document.getElementById("ingredient-qty");
const ingredientListEl = document.getElementById("ingredient-list");
const recipeListEl = document.getElementById("recipe-list");

let ingredients = []; // temp storage for ingredients

// ---------- Ingredient Functions ----------
function addIngredient() {
  const name = ingredientNameInput.value.trim();
  const qty = ingredientQtyInput.value.trim();
  if (!name || !qty) return alert("Enter both name and quantity");

  if (isNaN(parseFloat(qty))) return alert("Quantity must be a number!");

  ingredients.push({ name, quantity: parseFloat(qty) });
  ingredientNameInput.value = "";
  ingredientQtyInput.value = "";
  renderIngredientList();
}

function removeIngredient(index) {
  ingredients.splice(index, 1);
  renderIngredientList();
}

function renderIngredientList() {
  ingredientListEl.innerHTML = "";
  ingredients.forEach((ing, i) => {
    const li = document.createElement("li");
    li.innerText = `${ing.name} - ${ing.quantity}`;
    const btn = document.createElement("button");
    btn.innerText = "❌";
    btn.onclick = () => removeIngredient(i);
    li.appendChild(btn);
    ingredientListEl.appendChild(li);
  });
}

// ---------- Recipe Functions ----------
function renderRecipe(r) {
const imageHtml = `<img src="${r.image || 'https://images.unsplash.com/photo-1569246294372-ed319c674f14?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'}" class="recipe-img">`;

  const tagsHtml = r.tags && r.tags.length
    ? `<p class="tags">${r.tags.join(", ")}</p>`
    : "";

  return `
    <div class="recipe-card">
      ${imageHtml}
      <h3>${r.name}</h3>
      ${tagsHtml}
      <a class="view-btn" href="/static/recipe.html?id=${r.id}">View Recipe</a>
    </div>
  `;
}

async function loadRecipes() {
  try {
    const res = await fetch("/recipes", { credentials: "same-origin" });
    if (!res.ok) return;
    const recipes = await res.json();
    recipeListEl.innerHTML = recipes.length
      ? recipes.map(renderRecipe).join("")
      : "<p>No recipes yet.</p>";
  } catch (err) {
    console.error(err);
  }
}

async function addRecipe() {
  const name = nameInput.value.trim();
  const instructions = instructionsInput.value.trim();
  const imageUrl = document.getElementById("image-url").value.trim();

  if (!name || !instructions) return alert("Fill name and instructions");
  if (!ingredients.length) return alert("Add at least one ingredient");

  const tagsInput = document.getElementById("tag-input").value;
  const tags = tagsInput.split(",").map(t => t.trim()).filter(t => t);

  try {
    const res = await fetch("/recipes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({
        name,
        instructions,
        ingredients,
        tags,
        image: imageUrl
      })
    });

    if (res.ok) {
      nameInput.value = "";
      instructionsInput.value = "";
      document.getElementById("image-url").value = "";
      ingredients = [];
      document.getElementById("tag-input").value = "";
      renderIngredientList();
      loadRecipes();
    } else {
      const error = await res.json();
      alert(error.error || "You must be logged in");
    }
  } catch (err) {
    console.error(err);
  }
}

// ---------- Auth Functions ----------
async function login() {
  const res = await fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ username: username.value, password: password.value })
  });

  const data = await res.json();
  if (res.ok) {
    msg.innerText = "Logged in!";
    location.href = "/static/recipes.html";
  } else {
    msg.innerText = data.error || "Login failed";
  }
}

async function register() {
  const res = await fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ username: username.value, password: password.value })
  });

  const data = await res.json();
  msg.innerText = data.status || data.error || "Unknown error";
}

// ---------- Init ----------
document.addEventListener("DOMContentLoaded", () => {
  if (recipeListEl) loadRecipes();
});