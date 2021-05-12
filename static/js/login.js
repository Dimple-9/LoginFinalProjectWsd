window.onload = () => {

	// Event Listener for Login Button
	document.getElementById('login').onclick = () => {
		// Reset Error Messages
		document.getElementById('error-account').innerText = null;
		document.getElementById('error-email').innerText = null;
		document.getElementById('error-password').innerText = null;

		// Create Request
		const xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4) {
				if (this.status == 200){ // Success
					// TODO: Redirect to Rest of Application here
					window.location.href='/application'
					
				}
				else{ //Failure
					const errors = JSON.parse(this.responseText);
					document.getElementById('error-account').innerText = errors['account-error'] || null;
					document.getElementById('error-email').innerText = errors['email-error'] || null;
					document.getElementById('error-password').innerText = errors['password-error'] || null;
				}
			}

		};
		xhttp.open("POST", "./", true);
		xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
		xhttp.send(JSON.stringify({ "email": document.getElementById('email').value, "password": document.getElementById('password').value }));
	}
}