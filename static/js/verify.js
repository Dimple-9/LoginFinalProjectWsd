window.onload = () => {
	// Create Request
	const xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4) {
			if (this.status == 200){ // Success
				const message = JSON.parse(this.responseText);
				document.getElementById('verify-status').innerText = message['success'] || null;
				document.getElementById('link').innerHTML = "<p>Please <a href='/'>login here.</a></p>"

			}
			else if (this.status == 500){
				document.getElementById('verify-status').innerText = 'There was an error verifying your account. Please ensure you have typed in the correct link.' || null;
			}
			else{ //Failure
				const message = JSON.parse(this.responseText);

				if (message['isVerified']){
					document.getElementById('link').innerHTML = "<p>Please <a href='/'>login here.</a></p>"
				}
				else{
					document.getElementById('link').innerHTML = "<p>Please <a href='/register'>register here.</a></p>"
				}
				document.getElementById('verify-status').innerText = message['error'] || null;
			}
		}

	};
	xhttp.open("POST", window.location.href, true);
	xhttp.setRequestHeader("Content-type", "application/json;charset=UTF-8");
	xhttp.send();
	
}