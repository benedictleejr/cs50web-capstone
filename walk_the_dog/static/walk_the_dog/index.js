document.addEventListener('DOMContentLoaded', function() {


  const walkListings = document.querySelectorAll('.walk-info');
  walkListings.forEach(walk => {
    walk.addEventListener('click', function() {

      // grab all info needed
      const walkID = this.getAttribute('data-walkID');

      // api call to fetch all walk details
      fetch(`/view_walk/${walkID}`)
      .then(response => response.json())
      .then(data => {
        // hide calendar view (body div)
        document.querySelector('#calendar-view').style.display = "none";

        // create HTML for detailed view of walk
        const listingView = document.getElementById('listing-view');
        listingView.innerHTML = `
          <div class="walk-details-container">
            <div class="back-button">
              <button id="back-button">Back to Calendar</button>
            </div>
            <div class="walk-details">
              <h2>Walk Details</h2>
              <div class="walk-info-item">
                <strong>Date:</strong><br>${data.date}
              </div>
              <div class="walk-info-item">
                <strong>Time:</strong><br>${data.time}
              </div>
              <div class="walk-info-item">
                <strong>Duration:</strong><br>${data.duration}
              </div>
              <div class="walk-info-item">
                <strong>Dog Walked:</strong><br>${data.dog_walked}
              </div>
              <div class="walk-info-item">
                <strong>Walked By:</strong><br>${data.walked_by}
              </div>
              <div class="walk-info-item">
                <strong>Completed:</strong><br>${data.completed ? 'Yes' : 'No'}
              </div>
            </div>
          </div>
          <div>
            <button id="delete-btn" class="btn-delete">Delete Walk</button>
          </div>
        `;

        // add eventlisteners to back button
        const backButton = document.getElementById('back-button');
        backButton.addEventListener('click', function() {
          // show calendar again and clear listing view
          document.querySelector('#calendar-view').style.display = 'block';
          listingView.innerHTML = ''; // Clear listing view content
        });

        // add eventListeners to delete button
        const deleteButton = document.getElementById('delete-btn');
        deleteButton.addEventListener('click', function () {
          // hide calendar and clear listing view
          document.querySelector('#calendar-view').style.display = 'none';
          listingView.innerHTML = ''; // Clear listing view content
          
          // add in delete view
          listingView.innerHTML = `
          <div id="delete-div">
            <h1>Are you sure you want to delete this walk?</h1>
            <button id="delete-confirm-btn" class="btn-delete">Confirm Delete</button>
          </div>
          `;

          // eventlistener for confirming delete
          const deleteConfirmButton = document.getElementById('delete-confirm-btn');
          deleteConfirmButton.addEventListener('click', function () {
            fetch(`/delete_walk/${walkID}`)
            .then(response => response.json())
            .then(data => {
              if (data.success) {
                // clear editDiv and show profile Div
                listingView.innerHTML = ''; // Clear listing view content
                document.querySelector('#calendar-view').style.display = 'block';
                // reload to index
                window.location.href = "";
              } else {
                console.log(data.success);
                console.log(data.error);
                alert('Cannot delete!');
              }
            })
          });

        });




      })
      .catch(error => {
        console.error('Error fetching walk details:', error);
      });
    });
  });
});