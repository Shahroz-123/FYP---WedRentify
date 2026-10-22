// productData.js

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


// Show modal on "Rent Now" button click
document.querySelectorAll("button").forEach((btn) => {
    if (btn.textContent.includes("Rent Now")) {
        btn.addEventListener("click", () => {
            document.getElementById("rent-modal").classList.remove("hidden");
        });
    }
});

// Close modal
document.getElementById("cancel-btn").addEventListener("click", () => {
    document.getElementById("rent-modal").classList.add("hidden");
});

// Submit handler
document.getElementById("rent-form").addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Order placed successfully!");
    document.getElementById("rent-modal").classList.add("hidden");
});
