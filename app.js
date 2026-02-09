async function login() {
  const res = await fetch("/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  });

  msg.innerText = res.ok ? "Logged in!" : "Login failed";
  if (res.ok) location.href = "/static/recipes.html";
}

async function register() {
  const res = await fetch("/register", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  });

  msg.innerText = res.ok ? "Registered!" : "User exists";
}

function renderRecipe(r) {
  return `
    <div class="recipe">
      <div class="recipe-title">${r.title}</div>
      <div>${r.content}</div>
    </div>
  `;
}

async function loadRecipes() {
  const res = await fetch("/recipes");
  const recipes = await res.json();

  const list = document.getElementById("recipe-list");
  list.innerHTML = "";

  recipes.forEach(r => {
    list.innerHTML += renderRecipe(r);
  });
}


async function addRecipe() {
  const res = await fetch("/recipes", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      title: title.value,
      content: content.value
    })
  });

  if (res.ok) {
    loadRecipes();
    title.value = "";
    content.value = "";
  } else {
    alert("Login required");
  }
}
