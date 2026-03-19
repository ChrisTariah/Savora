// ---------- DOM ----------
const nameInput = document.getElementById("name");
const instructionsInput = document.getElementById("instructions");
const ingredientNameInput = document.getElementById("ingredient-name");
const ingredientQtyInput = document.getElementById("ingredient-qty");
const ingredientListEl = document.getElementById("ingredient-list");

let ingredients = [];

// ---------- Ingredients ----------
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

// ---------- Add Recipe ----------
async function addRecipe() {
  const name = nameInput.value.trim();
  const instructions = instructionsInput.value.trim();
  const imageUrl = document.getElementById("image-url").value.trim();

  if (!name || !instructions) return alert("Fill all fields");
  if (!ingredients.length) return alert("Add ingredients");

  const tagsInput = document.getElementById("tag-input").value;
  const tags = tagsInput.split(",").map(t => t.trim()).filter(t => t);

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
    alert("Recipe created!");

    nameInput.value = "";
    instructionsInput.value = "";
    document.getElementById("image-url").value = "";
    document.getElementById("tag-input").value = "";
    ingredients = [];

    renderIngredientList();
  } else {
    alert("Failed to create recipe");
  }
}

// ---------- Profile ----------
async function loadProfile() {
  await checkAuth();

  const res = await fetch("/me", { credentials: "same-origin" });
  const user = await res.json();

  document.getElementById("welcome-msg").innerText =
    `Welcome, ${user.username} 👋`;
}


function toggleCreate() {
  const section = document.getElementById("create-section");
  section.style.display = section.style.display === "none" ? "block" : "none";
}


async function loadMyRecipes() {
  const res = await fetch("/my-recipes", { credentials: "same-origin" });
  const recipes = await res.json();

  const list = document.getElementById("my-recipes");
  list.innerHTML = recipes.length
    ? recipes.map(renderRecipe).join("")
    : "<p>No recipes yet 🍳</p>";
}
function renderRecipe(r) {
  const image = r.image || "https://images.unsplash.com/photo-1569246294372-ed319c674f14";

  return `
    <div class="recipe-card">
      <img src="${image}" class="recipe-img">
      <h3>${r.name}</h3>
      <p>${r.instructions}</p>
      <a class="view-btn" href="/static/recipe.html?id=${r.id}">View Recipe</a>
    </div>
  `;
}
async function loadFridge() {
  const res = await fetch("/fridge", { credentials: "same-origin" });
  if (!res.ok) return;

  const fridge = await res.json();
  const list = document.getElementById("fridge-list");
  list.innerHTML = "";

  fridge.forEach(item => {
    const li = document.createElement("li");
    li.innerText = `${item.name} - ${item.quantity} ${item.unit || ""}`;
    list.appendChild(li);
  });
}
async function addToFridge() {
  const name = document.getElementById("fridge-id").value;
  const qty = document.getElementById("fridge-qty").value;

  await fetch("/fridge", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({
      name: name,
      quantity: qty
    })
  });

  loadFridge();
}
function selectIngredient(id, name, unit) {
  selectedIngredient = { id, name, unit };

  document.getElementById("ingredient-search").value = name;
  document.getElementById("unit-label").innerText = unit;

  document.getElementById("ingredient-results").innerHTML = "";
}
function addIngredient() {
  const qty = document.getElementById("ingredient-qty").value;

  if (!selectedIngredient || !qty) {
    return alert("Select ingredient and quantity");
  }

  ingredients.push({
    ingredientID: selectedIngredient.id,
    name: selectedIngredient.name,
    quantity: qty
  });

  renderIngredientList();
}

function selectFridgeIngredient(id, name, unit) {
  selectedFridgeIngredient = { id, name, unit };

  document.getElementById("fridge-search").value = name;
  document.getElementById("fridge-unit").innerText = unit;
  document.getElementById("fridge-results").innerHTML = "";
}
async function addToFridge() {
  const qty = document.getElementById("fridge-qty").value;

  if (!selectedFridgeIngredient || !qty) {
    return alert("Select ingredient and quantity");
  }

  await fetch("/fridge", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({
      ingredientID: selectedFridgeIngredient.id,
      quantity: qty
    })
  });

  loadFridge();
}

let selectedIngredient = null;

let searchTimeout;

document.getElementById("ingredient-search").addEventListener("input", (e) => {
  clearTimeout(searchTimeout);

  searchTimeout = setTimeout(async () => {
    const query = e.target.value;

    if (!query) {
      document.getElementById("ingredient-results").innerHTML = "";
      return;
    }

    const res = await fetch(`/ingredients?q=${query}`);
    const data = await res.json();

    const results = document.getElementById("ingredient-results");

    results.innerHTML = data.map(i => `
      <li onclick="selectIngredient(${i.id}, '${i.name}', '${i.unit}')">
        ${i.name}
      </li>
    `).join("");

  }, 250); // 250ms delay
});

let selectedFridgeIngredient = null;

let fridgeTimeout;

document.getElementById("fridge-search").addEventListener("input", (e) => {
  clearTimeout(fridgeTimeout);

  fridgeTimeout = setTimeout(async () => {
    const query = e.target.value;

    if (!query) {
      document.getElementById("fridge-results").innerHTML = "";
      return;
    }

    const res = await fetch(`/ingredients?q=${query}`);
    const data = await res.json();

    const results = document.getElementById("fridge-results");

    results.innerHTML = data.map(i => `
      <li onclick="selectFridgeIngredient(${i.id}, '${i.name}', '${i.unit}')">
        ${i.name}
      </li>
    `).join("");

  }, 250);
});


document.addEventListener("DOMContentLoaded", () => {
   loadProfile();
   loadMyRecipes();
   loadFridge();
});