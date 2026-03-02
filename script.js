// =========================
// TOGGLE LOGIN / SIGNUP
// =========================

const loginToggle = document.getElementById("loginToggle");
const signupToggle = document.getElementById("signupToggle");
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");

if (loginToggle && signupToggle) {

    loginToggle.addEventListener("click", () => {
        loginToggle.classList.add("active");
        signupToggle.classList.remove("active");

        loginForm.classList.add("active-form");
        signupForm.classList.remove("active-form");
    });

    signupToggle.addEventListener("click", () => {
        signupToggle.classList.add("active");
        loginToggle.classList.remove("active");

        signupForm.classList.add("active-form");
        loginForm.classList.remove("active-form");
    });
}

// =========================
// BASIC FORM VALIDATION
// =========================

if (loginForm) {
    loginForm.addEventListener("submit", function(e) {
        e.preventDefault();

        const email = loginForm.querySelector("input[type='email']").value;
        const password = loginForm.querySelector("input[type='password']").value;

        if (email === "" || password === "") {
            alert("Please fill in all fields.");
            return;
        }

        alert("Login successful! (Backend integration required)");
    });
}

if (signupForm) {
    signupForm.addEventListener("submit", function(e) {
        e.preventDefault();

        const name = signupForm.querySelector("input[type='text']").value;
        const email = signupForm.querySelector("input[type='email']").value;
        const password = signupForm.querySelector("input[type='password']").value;

        if (name === "" || email === "" || password === "") {
            alert("Please fill in all fields.");
            return;
        }

        if (password.length < 6) {
            alert("Password must be at least 6 characters.");
            return;
        }

        alert("Account created successfully! (Backend integration required)");
    });
}
