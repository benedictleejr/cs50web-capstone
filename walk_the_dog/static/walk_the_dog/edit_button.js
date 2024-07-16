document.addEventListener('DOMContentLoaded', function() {

  // code for edit profile buttons
  const editButton = document.querySelector('#edit-profile');
  editButton.addEventListener('click', function() {

    // grab user's ID and the div to append to
    const userID = this.getAttribute('data-userID');
    const viewProfileDiv = document.querySelector('#view-profile');
    const editDiv = document.querySelector('#edit-profile-div');
    console.log(editDiv)

    // api call to fetch user details
    fetch(`/profile/${userID}/get_details`)
    .then(response => response.json())
    .then(data => {
      // hide profile info, show editDIv
      viewProfileDiv.style.display = 'none';
      editDiv.style.display = 'block';

      editDiv.innerHTML = ''; // Clear existing content

      // create HTML for editing picture
      const title = document.createElement('h1');
      title.innerHTML = `${data.username}`;
      editDiv.appendChild(title);

      const subtitle = document.createElement('h2');
      subtitle.innerHTML = `${data.email}`;
      editDiv.appendChild(subtitle);

      const numwalks = document.createElement('h3');
      numwalks.innerHTML = `Number of walks: ${data.walks}`;
      editDiv.appendChild(numwalks);

      const profilePic = document.createElement('img');
      profilePic.setAttribute('src', `${data.picture_url}`);
      profilePic.setAttribute('alt', `${data.username}'s Profile Picture`);
      profilePic.setAttribute('width', '200');
      editDiv.appendChild(profilePic);

      const text = document.createElement('h4');
      text.innerHTML = 'Enter new image URL below:';
      editDiv.appendChild(text);

      // making the form for them to change their picture
      const editForm = document.createElement('form');
      editForm.setAttribute('id', 'edit-profile-form');
      editForm.setAttribute('data-userID', userID);
      editForm.setAttribute('action', '');
      editForm.setAttribute('method', 'post');

      const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
      const csrfTokenInput = document.createElement('input');
      csrfTokenInput.setAttribute('type', 'hidden');
      csrfTokenInput.setAttribute('name', 'csrfmiddlewaretoken');

      if (csrfTokenElement) {
        csrfTokenInput.value = csrfTokenElement.value;
      } else {
        console.error('CSRF token not found'); // Debugging log
      }
      editForm.appendChild(csrfTokenInput);

      // create textarea element for url
      const textarea = document.createElement('input');
      textarea.setAttribute('type', 'text');
      textarea.setAttribute('name', 'edited_picture_url');
      textarea.setAttribute('class', 'form-control');
      textarea.textContent = data.picture_url; // Set initial content from dataset
      editForm.appendChild(textarea);

      // create save button & append to form
      const saveButton = document.createElement('button');
      saveButton.setAttribute('type', 'submit');
      saveButton.setAttribute('class', 'btn btn-primary mt-2');
      saveButton.textContent = 'Save';
      editForm.appendChild(saveButton);

      // lastly, append form to editDiv
      editDiv.appendChild(editForm);

      console.log(editDiv)

      // Use requestAnimationFrame to force re-render
      requestAnimationFrame(() => {
        editDiv.style.display = 'block'; // Ensure display is set to block
      });

      // add eventlisteners to save button
      editForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const new_url = textarea.value;

        fetch(`/profile/${userID}/set_image`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfTokenInput.value
          },
          body: JSON.stringify({
            new_url: new_url
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // clear editDiv and show profile Div
            editDiv.innerHTML = '';
            viewProfileDiv.style.display = 'block';

            // reload the profile page
            window.location.href = `/profile/${userID}`;
          } else {
            console.log(data.success);
            console.log(data.error);
            alert('Invalid picture URL!');
          }
        });
      });
    });
  });
});