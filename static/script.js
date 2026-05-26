function showStrength(passwordId, strengthId) {
    if (!passwordId) passwordId = "password";
    if (!strengthId) strengthId = "strengthText";
    const password = document.getElementById(passwordId).value;
    const strengthText = document.getElementById(strengthId);
    if (!strengthText) return;
    const strength = checkStrength(password);
    strengthText.innerText = "Password Strength: " + strength;
    if (strength === "Weak") {
        strengthText.style.color = "red";
    } else if (strength === "Medium") {
        strengthText.style.color = "orange";
    } else {
        strengthText.style.color = "green";
    }
}

function checkStrength(password) {
    if (password.length < 6) return "Weak";
    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*]/.test(password);
    if (hasUpper && hasLower && hasNumber && hasSpecial && password.length >= 8) return "Strong";
    return "Medium";
}

function validateField(id) {
    const input = document.getElementById(id);
    const error = document.getElementById(id + "Error");
    if (!input || !error) return true;
    const value = input.value.trim();
    let msg = "";

    if (id === "fullName") {
        if (value === "") msg = "Full Name is required.";
        else if (!/^[a-zA-Z\s\.]+$/.test(value)) msg = "Only letters, spaces, and dots allowed.";
        else if (value.length < 2) msg = "Must be at least 2 characters.";
    } else if (id === "email" || id === "loginEmail") {
        if (value === "") msg = "Email is required.";
        else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) msg = "Enter a valid email address.";
    } else if (id === "phone") {
        if (value === "") msg = "Phone number is required.";
        else if (!/^[\d\s\+\-\(\)]{7,15}$/.test(value)) msg = "Enter a valid phone number (7-15 digits).";
    } else if (id === "password" || id === "loginPassword") {
        if (value === "") msg = "Password is required.";
        else if (value.length < 8) msg = "Must be at least 8 characters.";
        else if (!/[A-Z]/.test(value)) msg = "Must contain an uppercase letter.";
        else if (!/[a-z]/.test(value)) msg = "Must contain a lowercase letter.";
        else if (!/[0-9]/.test(value)) msg = "Must contain a number.";
        else if (!/[!@#$%^&*]/.test(value)) msg = "Must contain a special character (!@#$%^&*).";
    }

    error.innerText = msg;
    input.className = msg ? "invalid" : "valid";
    return msg === "";
}

function validateRegisterForm() {
    const fields = ["fullName", "email", "phone", "password"];
    let valid = true;
    fields.forEach(function (id) {
        if (!validateField(id)) valid = false;
    });
    if (!valid) alert("Please fix the errors before submitting.");
    return valid;
}

function validateLoginForm() {
    const fields = ["loginEmail", "loginPassword"];
    let valid = true;
    fields.forEach(function (id) {
        if (!validateField(id)) valid = false;
    });
    if (!valid) alert("Please fix the errors before submitting.");
    return valid;
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    const isDark = document.body.classList.contains("dark-mode");
    localStorage.setItem("darkMode", isDark);
    const btn = document.getElementById("darkModeToggle");
    if (btn) btn.innerText = isDark ? "\u2600\ufe0f" : "\u{1F319}";
}

function initDarkMode() {
    const btn = document.getElementById("darkModeToggle");
    if (!btn) return;
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
        btn.innerText = "\u2600\ufe0f";
    }
}
