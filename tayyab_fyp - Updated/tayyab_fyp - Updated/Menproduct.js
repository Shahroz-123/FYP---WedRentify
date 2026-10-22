// productData.js

const product = {
    title: "Heavy Brocade Black Wedding Wear Embroidery Work Sherwani",
    image: "data:image/jpeg;base64,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",
    price: 7000,
    rating: 3,
    description: "This heavy brocade sherwani is the perfect choice for weddings and festive occasions. Intricate embroidery and a rich black-red contrast make it a standout piece.",
    city: "Lahore",
    occasionType: "Wedding",
    color: "Black",
    length: "Floor Length",
    size: "M",
    sizeDescription: "Fits waist 34 inches",
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
