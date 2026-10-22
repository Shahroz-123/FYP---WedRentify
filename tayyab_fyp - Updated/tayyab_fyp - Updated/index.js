'use strict';
const exploreNow = document.querySelector('.hero-latest-btn');

exploreNow.addEventListener('click', function () {
  window.location.href = 'Women.html';
});



// Add click listener to the cyan feature card
document.querySelector('.cyan-feature-card')?.addEventListener('click', function () {
  // Redirect to the auction page
  window.location.href = "auction.html"; // Replace 'auction.html' with the actual URL of your auction page
});

// Add click listener to the red feature card
document.querySelector('.red-feature-card')?.addEventListener('click', function () {
  // Scroll to the footer-links section
  document.querySelector('.footer-links')?.scrollIntoView({ behavior: 'smooth' });
});

document.querySelector('.orange-feature-card')?.addEventListener('click', function () {
  window.location.href = 'damage-detection.html'; // replace with actual page
});

document.querySelector('.blue-feature-card')?.addEventListener('click', function () {
  window.location.href = 'Venue.html'; // replace with actual page
});
document.addEventListener("DOMContentLoaded", function () {
    const navLoginCart = document.querySelector(".nav-login-cart");

    // Check login status from localStorage/sessionStorage
    const isLoggedIn = localStorage.getItem("isLoggedIn");
     
    if (isLoggedIn === "true") {
        // Show Logout Button
        navLoginCart.innerHTML = `
            <button id="logoutBtn">Logout</button>
            <a href="cart.html"></a>
         
        `;

        // Logout Event
        document.getElementById("logoutBtn").addEventListener("click", () => {
            localStorage.removeItem("isLoggedIn");
             // Clear login status
             localStorage.removeItem("buyer_id");
             localStorage.removeItem("buyer_username");
            window.location.href = "index.html"; // Redirect to login page
        });
    } else {
        // Show Login Button
        navLoginCart.innerHTML = `
            <a href="login.html"><button>Login</button></a>
            <a href="cart.html"></a>
          
        `;
    }
});
