document.addEventListener('DOMContentLoaded', function() {
  const header = document.querySelector('#todays-date');
  const dogs_grid = document.querySelector('.dogs-grid');
  const newDogButton = document.querySelector('#new-walk-button-div');
  const paginationDiv = document.querySelector('.pagination');
  const removeDiv = document.querySelector('.remove-dog-div');

  header.style.display = 'block';
  dogs_grid.style.display = 'block';
  newDogButton.style.display = 'block';
  paginationDiv.style.display = 'block';
  removeDiv.style.display = 'none';

  const removeButtons = document.querySelectorAll('.btn-remove-dog');
  removeButtons.forEach(button => {
    button.addEventListener('click', function() {
      const dogID = this.getAttribute('data-dogID');
      
      header.style.display = 'none';
      dogs_grid.style.display = 'none';
      newDogButton.style.display = 'none';
      paginationDiv.style.display = 'none';
      removeDiv.style.display = 'block';

      removeDiv.innerHTML = `
      <div id="delete-div">
        <h1>Are you sure you want to remove this dog?</h1>
        <button id="delete-confirm-btn" class="btn-delete">Confirm Delete</button>
        <button id="delete-back-btn" class="btn-primary">Back</button>
      </div>
      `;

      // eventlistener for confirming delete
      const deleteConfirmButton = document.getElementById('delete-confirm-btn');
      deleteConfirmButton.addEventListener('click', function () {
        fetch(`/remove_dog/${dogID}`)
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              // clear removeDiv
              removeDiv.innerHTML = '';
              // reload to view dogs
              window.location.href = 'view_dogs';
            } else {
              console.log(data.success);
              console.log(data.error);
              alert('Cannot delete!');
            }
          })
      });

      // eventlistener for back button
      const backBtn = document.getElementById('delete-back-btn');
      backBtn.addEventListener('click', function() {
        header.style.display = 'block';
        dogs_grid.style.display = 'block';
        newDogButton.style.display = 'block';
        paginationDiv.style.display = 'block';
        removeDiv.innerHTML = '';
        removeDiv.style.display = 'none';
      });


    });
  });

  



});