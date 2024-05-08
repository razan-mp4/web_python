document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('signup-form');
    const messageDiv = document.getElementById('message');

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const username = form.elements['username'].value;
        const email = form.elements['email'].value;
        const password = form.elements['password'].value;

        const response = await fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const responseData = await response.json();

        if (response.ok) {
            messageDiv.textContent = 'Signup successful!'; // Customize success message if needed
            form.reset();
        } else {
            messageDiv.textContent = responseData.detail; // Display error message returned from server
        }
    });
});
