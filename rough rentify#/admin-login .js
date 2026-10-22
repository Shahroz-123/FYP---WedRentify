"use strict";

const login_btn = document.querySelector(".login-btn");
const incorrect = document.querySelector(".incorrect"); // Use class or id to select the error element

login_btn.addEventListener("click", function (e) {
  e.preventDefault();
  
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;


  if (username === "admin" && password === "root" && email === "admin@gmail.com") {
    
    window.location.href = 'admin.html';
  } else {
 
    incorrect.innerHTML = "Please try again! Incorrect inputs.";

    
    setTimeout(() => {
      incorrect.innerHTML = ""; 
    }, 10000); 
  }
});
