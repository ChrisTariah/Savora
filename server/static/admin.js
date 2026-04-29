const searchInput = document.getElementById("user-search");
const resultsTable = document.getElementById("user-results");

let timeout;

searchInput.addEventListener("input", (e) => {
  clearTimeout(timeout);

  timeout = setTimeout(() => {
    searchUsers(e.target.value);
  }, 300);
});

async function searchUsers(query) {
  if (!query) {
    resultsTable.innerHTML = `
      <tr>
        <td colspan="3" class="empty-msg">Start typing to search users</td>
      </tr>
    `;
    return;
  }

  const res = await fetch(`/admin/users?q=${query}`, {
    credentials: "same-origin"
  });

  if (!res.ok) {
    resultsTable.innerHTML = `
      <tr>
        <td colspan="3" class="empty-msg">Error loading users</td>
      </tr>
    `;
    return;
  }

  const users = await res.json();

  resultsTable.innerHTML = users.length
    ? users.map(u => `
        <tr>
          <td>${u.id}</td>
          <td>${u.username}</td>
          <td>
            <button class="action-btn delete-btn" onclick="deleteUser(${u.id})">
              Delete
            </button>

            <button class="action-btn" onclick="makeAdmin(${u.id})">
              Make Admin
            </button>
          </td>
        </tr>
      `).join("")
    : `
      <tr>
        <td colspan="3" class="empty-msg">No users found</td>
      </tr>
    `;
}


async function makeAdmin(id) {
  if (!confirm("Make this user an admin?")) return;

  const res = await fetch("/admin/make-admin", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ userID: id })
  });

  if (res.ok) {
    alert("User is now admin");
    searchUsers(searchInput.value); // refresh list
  } else {
    alert("Failed to update user");
  }
}


async function deleteUser(id) {
  if (!confirm("Are you sure you want to delete this user?")) return;

  const res = await fetch("/admin/delete-user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ userID: id })
  });

  if (res.ok) {
    alert("User deleted");
    searchUsers(searchInput.value);
  } else {
    alert("Failed to delete user");
  }
}