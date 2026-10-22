"use strict";

async function loadUsers() {
  const res = await fetch("http://127.0.0.1:8000/api/accounts/users/");
  const users = await res.json();

  const tbody = document.getElementById("userBody");
  tbody.innerHTML = "";

  users.forEach(u => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${u.id}</td>
      <td>${u.username}</td>
      <td>${u.cnic}</td>
       <td>${u.type}</td>
      <td>${u.email}</td>
      <td><button onclick="deleteUser('${u.type}', ${u.id})">Delete</button></td>
    `;
    tbody.appendChild(row);
  });
}

async function deleteUser(type, id) {
  if (confirm(`Are you sure you want to delete this ${type}?`)) {
    const res = await fetch(`http://127.0.0.1:8000/api/accounts/delete_user/${type}/${id}/`, {
      method: "DELETE",
    });
    const data = await res.json();
    alert(data.message || data.error);
    loadUsers();
  }
}

function SearchUser() {
  const searchValue = document.getElementById("username").value.trim().toLowerCase();
  const rows = document.querySelectorAll("#userBody tr");

  rows.forEach(row => {
    const usernameCell = row.children[1].textContent.toLowerCase();
    if (usernameCell.includes(searchValue) && searchValue !== "") {
      row.style.backgroundColor = "#ffeb3b"; // highlight
    } else {
      row.style.backgroundColor = "";
    }
  });
}

loadUsers();
