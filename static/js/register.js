window.onload = () => {

	let timer = 10;
	// Event Listener for Login Button
	document.getElementById('register').onclick = () => {
		// Reset Response Messages
		document.getElementById('error-email').innerText = null;
		document.getElementById('error-password').innerText = null;
		document.getElementById('success').innerText = null;
		document.getElementById('redirect-message').innerText = null;

		// Create Request
		const xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4) {
				if (this.status == 200){ // Success
					const message = JSON.parse(this.responseText);
					document.getElementById('success').innerText = message['success'] || null;
					
					document.getElementById('redirect-message').innerText = `You will be redirected to the login page in ${timer} second(s)`;

					//Redirect to Login
					setInterval(() => {
						timer--;
						document.getElementById('redirect-message').innerText = `You will be redirected to the login page in ${timer} second(s)`;
					}, 1000);
					setTimeout(() => {
						window.location.href='./';
					}, 9000);
				}
				else{ //Failure
					const errors = JSON.parse(this.responseText);
					document.getElementById('error-email').innerText = errors['email-error'] || null;
					document.getElementById('error-password').innerText = errors['password-error'] || null;
				}
			}

		};
		xhttp.open("POST", "./register", true);
		xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
		xhttp.send(JSON.stringify({ "email": document.getElementById('email').value, "password": document.getElementById('password').value }));
	}
}