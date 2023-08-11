// Debug 
console.log("This script was created by Mbonu Chinedum.")

// Getting all the dom elements 
let email = document.getElementById("email"); 
let password = document.getElementById("password"); 
let submitButton = document.getElementById("submit-btn"); 

// Adding event listener for the submit button 
submitButton.addEventListener("click", (event) => {
    // Preventing default submission 
    event.preventDefault(); 

    /* Execute the block of code below if the submit button 
    * was clicked
    * Getting the user's input email, and password value from the dom elements  
    */ 
   const emailValue = email.value; 
   const passwordValue = password.value; 

   /** 
    * Checking if the forms are valid for the email field 
    * and the password field 
    */
   if (emailValue === '') {
        // Using sweet Alert to display the info message 
        Swal.fire({
            title: 'Email required',
            text: 'Please fill in your email address',
            icon: 'info',
            confirmButtonText: 'Okay...'
        })

        // Stopping the process 
        return; 
   }

   // Checking for password 
   else if (passwordValue === '') {
        // Using sweet alert to display the info 
        Swal.fire({
            title: 'Password required', 
            text: 'Please fill in your password', 
            icon: 'info', 
            confirmButtonText: 'Okay...'
        })

        // Stopping the process 
        return; 
   }

   // Else if the form field had text values, execute the 
   // block of code below 
   let data = JSON.stringify({
        email: emailValue, 
        password: passwordValue, 
   })

   /** Setting the request headers, the http verb, 
    * and the URL for the backend connection.  
   */
   const headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST', 
        'Access-Control-Allow-Headers': 'Content-Type',
   }; 

   // Setting the url 
   const url = "/"; 

   // Making the fetch request to the backend server 
   fetch(url, {
        method: 'POST', 
        headers: headers, 
        body: data, 
   })
   .then(response => response.json())
   .then(data => {
        // Execute the block of code below if the server responded 
        if (data.status === "success") {
          // Execute the block of code below if the returned data status 
          // is a success 
          location.href = '/dashboard'; 
        }

        // Else if the status returned an error code 
        else if (data.status === "error" ) {
          // Execute the block of code below if the returned status code was 
          // an error 
          Swal.fire({
               title: 'Invalid Email, or Password', 
               text: 'Please fill in the correct email address, or password', 
               icon: 'error', 
               confirmButtonText: 'Okay...'
          })

          // Closing up 
          return; 

        }
   })

    

})