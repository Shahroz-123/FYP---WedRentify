// productData.js
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
const product = {
    title: "Heavy Brocade Black Wedding Wear Embroidery Work Lehenga Choli",
    image: "https://images.wholesalesalwar.com/2024y/July/51464/Black-Heavy%20Brocade-Wedding%20Wear-Embroidery%20Work-Lehenga%20Choli(%20only%20in%20size%2034%20to%2040)-TEV-16.jpg",
    price: 7000,
    rating: 3,
    description: "This heavy brocade lehenga choli is the perfect choice for weddings and festive occasions. Intricate embroidery and a rich black-red contrast make it a standout piece.",
    city: "Mumbai",
    occasionType: "Wedding",
    color: "Black",
    length: "Floor Length",
    size: "M",
    sizeDescription: "Fits waist 28-30 inches",
    availableFrom: "2025-05-10",
    availableTo: "2025-05-20"
};

document.addEventListener("DOMContentLoaded", () => {
    // Main section
    document.getElementById("product-title").innerText = product.title;
    document.getElementById("product-image").src = product.image;
    document.getElementById("product-price").innerText = `Rs ${product.price}`;
    document.getElementById("product-description").innerText = product.description;

    // Rating
    const ratingContainer = document.getElementById("product-rating");
    let stars = "";
    for (let i = 1; i <= 5; i++) {
        stars += i <= product.rating ? "★ " : "☆ ";
    }
    ratingContainer.innerHTML = `<span>${stars}</span><span class="text-sm text-gray-500">(${product.rating}/5)</span>`;

    // Dress detail section below
    const detailSection = document.getElementById("product-details");
    const fields = {
        "City": product.city,
        "Occasion Type": product.occasionType,
        "Dress Color": product.color,
        "Dress Length": product.length,
        "Size": product.size,
        "Size Description": product.sizeDescription,
        "Available From": product.availableFrom,
        "Available To": product.availableTo
    };

    Object.entries(fields).forEach(([label, value]) => {
        const item = document.createElement("div");
        item.innerHTML = `<strong>${label}:</strong> ${value}`;
        detailSection.appendChild(item);
    });
});



// Show auction modal on "Auction Now" button click
document.querySelectorAll("button").forEach((btn) => {
    if (btn.textContent.includes("Auction Now")) {
      btn.addEventListener("click", () => {
        document.getElementById("auction-modal").classList.remove("hidden");
      });
    }
  });
  
  // Hide auction modal on cancel
  document.getElementById("auction-cancel-btn").addEventListener("click", () => {
    document.getElementById("auction-modal").classList.add("hidden");
  });
  
  // Handle auction bid submission
  document.getElementById("auction-form").addEventListener("submit", (e) => {
    e.preventDefault();
  
    const name = document.getElementById("bidder-name").value.trim();
    const bid = document.getElementById("bid-amount").value.trim();
    const bidList = document.getElementById("bids-list");
  
    if (name && bid && parseFloat(bid) > 0) {
      const li = document.createElement("li");
      li.textContent = `${name} placed a bid of Rs ${bid}`;
      bidList.appendChild(li);
  
      // Reset form
      document.getElementById("bidder-name").value = "";
      document.getElementById("bid-amount").value = "";
  
      // Optionally close modal
      document.getElementById("auction-modal").classList.add("hidden");
    } else {
      alert("Please enter valid details.");
    }
  });
  


