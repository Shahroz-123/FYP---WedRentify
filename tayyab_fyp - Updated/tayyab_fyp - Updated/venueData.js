// venueData.js

const venue = {
    name: "Royal Grand Marriage Hall",
    image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSckISTbBCaHAwCUCAC82E9cS2OfEK8qqmFIg&s",
    capacity: 500,
    availableFrom: "2025-06-01",
    availableTo: "2025-06-30",
    contactNumber: "+91-9876543210",
    timeSlot: "12:00 PM to 4:00 PM",
    pricePerHead: 1200,
    description: "A premium venue for weddings with top-class amenities, AC banquet, catering and valet services.",
    city: "Pune"
};

document.addEventListener("DOMContentLoaded", () => {
    // Main section
    document.getElementById("venue-name").innerText = venue.name;
    document.getElementById("venue-image").src = venue.image;
    document.getElementById("venue-description").innerText = venue.description;
    document.getElementById("venue-price").innerText = `Rs ${venue.pricePerHead} / head`;

    // Venue detail section below
    const detailSection = document.getElementById("venue-details");
    const fields = {
        "City": venue.city,
        "Capacity": `${venue.capacity} people`,
        "Available From": venue.availableFrom,
        "Available To": venue.availableTo,
        "Contact Number": venue.contactNumber,
        "Time Slot": venue.timeSlot,
        "Price Per Head": venue.pricePerHead    
    };

    Object.entries(fields).forEach(([label, value]) => {
        const item = document.createElement("div");
        item.innerHTML = `<strong>${label}:</strong> ${value}`;
        detailSection.appendChild(item);
    });
});
const isLoggedIn = localStorage.getItem("isLoggedIn");
const navLoginCart = document.querySelector(".nav-login-cart"); // ✅ fix added

if (isLoggedIn === "true") {
  navLoginCart.innerHTML = `
    <button id="logoutBtn" class="bg-red-700 text-white px-3 py-1 rounded hover:bg-red-800">Logout</button>
    <a href="cart.html"><img src="cart.png" alt="Cart"></a>
    <div class="nav-cart-count">0</div>
  `;

  document.getElementById("logoutBtn").addEventListener("click", () => {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("buyer_id");
    localStorage.removeItem("buyer_username");
    window.location.href = "index.html";
  });
} else {
  navLoginCart.innerHTML = `
    <a href="login.html"><button>Login</button></a>
    <a href="cart.html"><img src="cart.png" alt="Cart"></a>
    <div class="nav-cart-count">0</div>
  `;
}

