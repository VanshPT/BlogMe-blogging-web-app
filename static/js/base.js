function typerr() {
    var txt = "BlogMe";
    var emp = "";
    var strin = document.getElementsByClassName('pacifico-regular')[0]; // Assuming there's only one element with this class
    var i = 0;

    var typingInterval = setInterval(function() {
        emp += txt[i];
        strin.textContent = emp;
        i++;
        if (i >= txt.length) {
            clearInterval(typingInterval); // Stop the typing effect once all characters are added
        }
    }, 100); // Adjust the interval to control typing speed
}

typerr(); // Call the function to start the typing effect


function typerr1() {
    var txt = "BlogMe";
    var emp = "";
    var strin = document.getElementById('logguser')[0]; // Assuming there's only one element with this class
    var i = 0;

    var typingInterval = setInterval(function() {
        emp += txt[i];
        strin.textContent = emp;
        i++;
        if (i >= txt.length) {
            clearInterval(typingInterval); // Stop the typing effect once all characters are added
        }
    }, 100); // Adjust the interval to control typing speed
}

typerr1(); // Call the function to start the typing effect
