// Get the form and table body
const venueForm = document.getElementById('venue-form');
const venueTableBody = document.getElementById('venue-table-body');

// Handle form submission
venueForm.addEventListener('submit', function (e) {
  e.preventDefault(); // Prevent default form submission

  // Get form values
  const venueName = document.getElementById('venue-name').value;
  const venueImageUrl = document.getElementById('venue-image-url').value;
  const numPersons = document.getElementById('num-persons').value;
  const perHeadPrice = document.getElementById('per-head-price').value;
  const availableDate = document.getElementById('available-date').value;
  const contactNumber = document.getElementById('contact-number').value;

  // Create a new row
  const newRow = document.createElement('tr');
  newRow.innerHTML = `
    <td class="px-4 py-2 border-b">${venueName}</td>
    <td class="px-4 py-2 border-b"><img src="${venueImageUrl}" alt="Venue Image" class="w-24 h-24 object-cover rounded-md"></td>
    <td class="px-4 py-2 border-b">${numPersons}</td>
    <td class="px-4 py-2 border-b">${perHeadPrice}rs</td>
    <td class="px-4 py-2 border-b">${availableDate}</td>
    <td class="px-4 py-2 border-b">${contactNumber}</td>
    <td class="px-4 py-2 border-b">
      <button class="bg-red-500 text-white py-1 px-3 rounded-md hover:bg-red-600 transition delete-btn">Delete</button>
    </td>
  `;

  // Append to the table
  venueTableBody.appendChild(newRow);

  // Add event listener for the delete button
  const deleteButton = newRow.querySelector('.delete-btn');
  deleteButton.addEventListener('click', function () {
    newRow.remove(); // Remove the row when delete button is clicked
  });

  // Reset form
  venueForm.reset();
});
