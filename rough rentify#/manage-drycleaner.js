// Get the form and table body
const drycleanerForm = document.getElementById('drycleaner-form');
const drycleanerTableBody = document.getElementById('drycleaner-table-body');

// Handle form submission
drycleanerForm.addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent default form submission

  // Get form values
  const drycleanerName = document.getElementById('drycleaner-name').value;
  const contactNumber = document.getElementById('contact-number').value;
  const priceRange = document.getElementById('price-range').value;

  // Create a new row
  const newRow = document.createElement('tr');
  newRow.innerHTML = `
    <td class="px-4 py-2 border-b">${drycleanerName}</td>
    <td class="px-4 py-2 border-b">${contactNumber}</td>
    <td class="px-4 py-2 border-b">${priceRange}</td>
    <td class="px-4 py-2 border-b">
      <button class="bg-red-500 text-white py-1 px-3 rounded-md hover:bg-red-600 transition delete-btn">Delete</button>
    </td>
  `;

  // Append to the table
  drycleanerTableBody.appendChild(newRow);

  // Add event listener for the delete button
  const deleteButton = newRow.querySelector('.delete-btn');
  deleteButton.addEventListener('click', function () {
    newRow.remove(); // Remove the row when delete button is clicked
  });

  // Reset form
  drycleanerForm.reset();
});
