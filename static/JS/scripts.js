document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/login/', {
        method: 'POST',
        body: formData,
        headers: {'X-CSRFToken': '{{ csrf_token }}'}
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirect or perform any necessary action on successful login
            } else {
                // Display error message to the user
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

document.addEventListener('DOMContentLoaded', function () {
    var loginButton = document.getElementById('loginButton');
    var loginForm = document.getElementById('loginForm');

    loginButton.addEventListener('click', function () {
        loginForm.style.display = 'block';
    });
});

 // JavaScript code for handling the logout button and modal
    const logoutButton = document.getElementById('logoutButton');
    const logoutModal = document.getElementById('logoutModal');
    const confirmLogoutButton = document.getElementById('confirmLogoutButton');
    const cancelLogoutButton = document.getElementById('cancelLogoutButton');

    // Show the logout modal when the logout button is clicked
    logoutButton.addEventListener('click', function() {
        logoutModal.style.display = 'block';
    });

    // Hide the logout modal and perform logout when confirmed
    confirmLogoutButton.addEventListener('click', function() {
        // Perform the logout action here
        // ...

        logoutModal.style.display = 'none';
    });

