// Debug 
console.log('This script was created by Mbonu Chinedu'); 

// Getting all the dom elements 
let firstnameDisplay = document.getElementById("firstname-display"); 
let lastnameDisplay = document.getElementById("lastname-display"); 
let uploadImageBtn = document.getElementById("uploadImageBtn"); 
let performAnalysisBtn = document.getElementById("perform-analysis"); 
let fileInput = document.getElementById("imageInput"); 
let uploadImage = document.getElementById("upload-image"); 

// Making connections to the server to get the user's details 
window.onload = () => {
   // Setting the request headers 
   const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST', 
    'Access-Control-Allow-Headers': 'Content-Type',
   }; 

   // Setting the url 
   const url = '/dashboard/get-users-details'; 

   // Making the fetch request to the backend server 
   fetch(url, {
        method: 'POST', 
        headers: headers, 
        body: null, 
   })
   .then((response) => response.json())
   .then(data => {
        // Execute the block of code below if the server returned with 
        // a json object file. 
        // make changes to the firstname, and lastname html-tag 
        firstnameDisplay.innerText = data['firstname']; 
        lastnameDisplay.innerText = data['lastname']; 
   })
}

// Adding event listener for the upload image button 
uploadImageBtn.addEventListener("click", (event) => {
    // Execute the block of code below if the upload image button was clicked 
    const file = fileInput.files[0]; 
    let formData = new FormData(); 

    // Appending the file, into the form data before sending it 
    // to the backend server 
    formData.append('image', file); 

    // Using fetch request 
    fetch('/dashboard/upload', {
        method: 'POST', 
        body: formData
    })
    .then(response => response.text())
    .then(result => {
        // Convert the data into a json object 
        result = JSON.parse(result); 
        console.log(result); 

        // Changing the apperance of the image, and showing the user the 
        // image he/she uploaded 
        uploadImage.src = result["imageUrl"]

        /**
         * Storing the uploaded image name into the localstorage memeory 
         * on the browser 
         * of the image file. This name would then be sent back 
         * to the server for specifically identifying the image to perform 
         * machine learning classification on. 
         */
        localStorage.setItem('uploaded-image-name', result['imageName']); 
    })
})

// Adding an event listener for the perform analysis button 
performAnalysisBtn.addEventListener("click", (event) => {
    // Get the image name from the localstorage client-side web storage object 
    const imageName = localStorage.getItem('uploaded-image-name'); 
    
    // And send the image name back to the server to perform machine learning analysis 
    // on the specified image file 
    const data = JSON.stringify({
        imageName: imageName, 
    })
    
    /**
     * Setting the request headers, and the URL for the 
     * backend connection. 
     */
    const headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST', 
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    // Setting the url 
    const url = '/dashboard/perform-analysis'; 

    // then clear the 'localStorage' storage 
    fetch(url, {
        method: 'POST', 
        headers: headers, 
        body: data, 
        keepalive: true, 
    })
    .then((response) => response.json())
    .then(data => {
        // If the status is "success", execute the 
        // block of code below 
        if (data.status === "success") {
            // Using sweet alert to display the success message 
            Swal.fire({
                title: "Car Tyre Thread Results", 
                icon: "success", 
                html: `
                    <head> 
                        <style> 
                            .container {
                                margin: auto; 
                                diplay: flex; 
                                margin-top: 0px; 
                                height: 149px; 
                                width: 370px; 
                            }
                        </style> 
                    </head> 
                    <div class="container"> 
                       <ul> 
                          <li style="list-style: none; font-size: 27px; padding-bottom: 19px; color: #712424;"> Thread Analysis: ${data['ModelAccuracy']} </li> 
                          <li style="list-style: none; font-size: 18px; padding-bottom: 19px;"> Tyre Type: <b> ${data["ThreadType"]} </b> </li> 
                          <li style="list-style: none;"> Status: ${data['status']} </li> 
                        </ul> 
                    </div> 
                `
            })

            // Clearing the localstorage memory 
            localStorage.removeItem("uploaded-image-name"); 

        }
    })
    

})