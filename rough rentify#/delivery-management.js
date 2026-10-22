let companies = [
  { name: "TCS", contact: "021-111-123-456" },
  { name: "DHL", contact: "042-111-222-333" }
];


const dummyOrders = [
    { orderId: "ORD101", status: "Shipped", company: "FastTrack Delivery" },
    { orderId: "ORD102", status: "In Transit", company: "QuickShip" },
    { orderId: "ORD103", status: "Delivered", company: "SuperFast Courier" },
    { orderId: "ORD104", status: "Processing", company: "SwiftPost" }
  ];
  
  // Search Function for Orders
  function searchOrder() {
    const searchInput = document.getElementById('searchInput').value.trim();
    const resultBox = document.getElementById('searchResult');
    const order = dummyOrders.find(order => order.orderId === searchInput);
  
    if (order) {
      resultBox.innerHTML = `<p>✅ Order ID: ${order.orderId}</p><p>Status: ${order.status}</p><p>Company: ${order.company}</p>`;
    } else {
      resultBox.innerHTML = "<p>❌ No order found with that ID. Please check and try again.</p>";
    }
  }

function renderCompanies() {
  const table = document.getElementById("companyTable").getElementsByTagName("tbody")[0];
  table.innerHTML = "";
  companies.forEach((company, index) => {
    let row = table.insertRow();
    row.innerHTML = `
      <td>${company.name}</td>
      <td>${company.contact}</td>
      <td><button class="remove-btn" onclick="removeCompany(${index})">Remove</button></td>
    `;
  });

  // Update seller dropdown
  const dropdown = document.getElementById("sellerCompany");
  dropdown.innerHTML = "";
  companies.forEach(company => {
    let option = document.createElement("option");
    option.value = company.name;
    option.text = company.name;
    dropdown.appendChild(option);
  });
}

function addCompany() {
  const name = document.getElementById("companyName").value.trim();
  const contact = document.getElementById("companyContact").value.trim();

  if (name === "" || contact === "") {
    alert("Please fill out both fields.");
    return;
  }

  companies.push({ name, contact });
  document.getElementById("companyName").value = "";
  document.getElementById("companyContact").value = "";
  renderCompanies();
}

function removeCompany(index) {
  if (confirm("Are you sure you want to remove this company?")) {
    companies.splice(index, 1);
    renderCompanies();
  }
}

  
function searchDelivery() {
  const query = document.getElementById("searchDelivery").value.trim();
  const resultDiv = document.getElementById("deliveryStatusResult");

  if (query === "") {
    resultDiv.innerText = "Please enter a company name or tracking ID.";
    return;
  }

  const result = deliveryStatuses[query] || "No delivery status found.";
  resultDiv.innerText = `Status: ${result}`;
}

// Initial render
renderCompanies();
