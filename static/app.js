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

  ingredients.push({ name, quantity: qty });
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
  const tagsHtml = r.tags && r.tags.length
    ? `<p class="tags">${r.tags.join(", ")}</p>`
    : "";

  return `
    <div class="recipe-card">
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
  if (!name || !instructions) return alert("Fill name and instructions");
  if (!ingredients.length) return alert("Add at least one ingredient");

  const tagsInput = document.getElementById("tag-input").value;
  const tags = tagsInput.split(",").map(t => t.trim()).filter(t => t);

  try {
    const res = await fetch("/recipes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({ name, instructions, ingredients })
    });

    if (res.ok) {
      nameInput.value = "";
      instructionsInput.value = "";
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
