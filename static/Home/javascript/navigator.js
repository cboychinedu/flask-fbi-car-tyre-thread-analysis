// Debug 
console.log("Working Navbar"); 

// Getting all the necessary dom elements 
let menuBtn = document.getElementById("menuButton"); 
let menuContainer = document.getElementById("menuContainer"); 

// Adding event listener 
menuBtn.addEventListener("click", (event) => {
    // Adding class list 
    menuContainer.classList.add("open"); 

    // Remove the menu after it is shown 
    setTimeout(() => {
        menuContainer.classList.remove('open'); 
    }, 4000)
})