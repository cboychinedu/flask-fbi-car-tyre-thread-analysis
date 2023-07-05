// Debug 
console.dir("This script was created by Mbonu Chinedum"); 

// Getting all the dom elements 
let firstname = document.getElementById("firstname"); 
let lastname = document.getElementById("lastname"); 
let email = document.getElementById("email"); 
let password = document.getElementById("password"); 
let registerBtn = document.getElementById("register-button"); 

// Adding event listener for the register button 
registerBtn.addEventListener("click", (event) => {
    // Preventing default submission 
    event.preventDefault(); 

    /**
     * Execute the block of code below if the submit button was clicked 
     * And get the user's input values for the firstname, lastname, email, and 
     * password value. 
     */
    const firstnameValue = firstname.value; 
    const lastnameValue = lastname.value; 
    const emailValue = email.value; 
    const passwordValue = password.value; 

    /**
     * Checking if the forms are valid for the firstname, lastname, email 
     * And password 
     */
    if (firstnameValue === '') {
        // Using sweet Alert to display the info message 
        Swal.fire({
            title: 'Firstname required',
            text: 'Please fill in your firstname',
            icon: 'info',
            confirmButtonText: 'Okay...'
        })
    }

    // Lastname name 
    else if (lastnameValue === '') {
        // Using sweet Alert to display the info message 
        Swal.fire({
            title: 'Lastname required',
            text: 'Please fill in your lastname',
            icon: 'info',
            confirmButtonText: 'Okay...'
        })
    }

    // Email address 
    else if (emailValue === '') {
        // Using sweet Alert to display the info message 
        Swal.fire({
            title: 'Email address required',
            text: 'Please fill in your email address',
            icon: 'info',
            confirmButtonText: 'Okay...'
        })
    }

    // Password check 
    else if (passwordValue === '') {
        // Using sweet Alert to display the info message 
        Swal.fire({
            titl: 'Password required', 
            text: 'Please fill in your password', 
            icon: 'info', 
            confirmButtonText: 'Okay...'
        })
    }

    // Using else statement 
    else {
        // Getting the user's registration data 
        let data = JSON.stringify({
            firstname: firstnameValue, 
            lastname: lastnameValue, 
            email: emailValue, 
            password: passwordValue, 
        })

        /**
         * Setting the requuest header, the http verbs, 
         * and the URL for the register route server. 
         */
        const headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST', 
            'Access-Control-Allow-Headers': 'Content-Type',
        }; 

        // Setting the url 
        const url = "http://localhost:5001/register"

        // Making the fetch request to the backend server 
        fetch(url, {
            method: 'POST', 
            headers: headers, 
            body: data, 
        })
        .then(response => response.json())
        .then(data => {
            // Checking if the user is saved on the database 
            if (data.status === "success") {
                // Execute the block of code below for a successful message 
                Swal.fire({
                    titl: 'User registered...', 
                    text: 'Successfully registered', 
                    icon: 'success', 
                    confirmButtonText: 'Okay...'
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Redirect the user to the login page 
                        location.href = "/"
                    }
                })

            }

            // Else if the data was an error 
            else if (data.status === "error" ) {
                // Execute the block of code below for an error message 
                Swal.fire({
                    titl: 'Error registering user...', 
                    text: 'Error in registration...', 
                    icon: 'error', 
                    confirmButtonText: 'Okay...'
                })

                // Closing 
                return; 
            }

          
        })
    }

})
