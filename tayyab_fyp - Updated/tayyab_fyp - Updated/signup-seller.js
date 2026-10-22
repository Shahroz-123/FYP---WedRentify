'use strict';

// --- JAVASCRIPT PATCH 2: Setup and Verification Logic ---
let pendingFormData = {};
const verificationModal = document.getElementById("verification-modal"); 

// --- Modal Button Handlers ---
document.getElementById("verifyButton").addEventListener("click", verifyAndFinalizeSignup);
document.getElementById("cancelVerify").addEventListener("click", () => {
    verificationModal.style.display = 'none';
    document.getElementById("modalMessage").textContent = '';
});


// -----------------------------------------------------------------
// FINAL SIGNUP LOGIC: Checks code, then creates Seller account
// -----------------------------------------------------------------
async function verifyAndFinalizeSignup() {
    const submittedCode = document.getElementById("verificationCode").value.trim();
    const modalMessage = document.getElementById("modalMessage");
    const verifyButton = document.getElementById("verifyButton");

    if (submittedCode.length !== 6) {
        modalMessage.textContent = "Please enter the 6-digit code.";
        return;
    }

    verifyButton.disabled = true;
    modalMessage.textContent = 'Verifying code...';

    try {
        // 1. Verify Code API Call (Backend API: /api/accounts/verify-code/)
        const checkCodeResponse = await fetch("http://127.0.0.1:8000/api/accounts/verify-code/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: pendingFormData.email, code: submittedCode }),
        });
        
        if (!checkCodeResponse.ok) {
             const errorData = await checkCodeResponse.json();
             throw new Error(errorData.error || "Invalid or expired code.");
        }
        
        // 2. If verified, proceed to final Seller account creation (CRITICAL DIFFERENCE)
        const finalSignupResponse = await fetch("http://127.0.0.1:8000/api/accounts/seller/signup/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(pendingFormData),
        });

        const data = await finalSignupResponse.json();

        if (finalSignupResponse.ok) {
            alert("✅ Seller account created and email verified successfully!");
            window.location.href = "seller-login.html"; // Redirect to seller login
        } else {
            alert("Error during final signup: " + (data.error || "Please check inputs."));
        }

    } catch (error) {
        console.error("Verification/Signup Error:", error);
        modalMessage.textContent = "Verification Failed: " + error.message;
    } finally {
        verifyButton.disabled = false;
        verifyButton.textContent = 'Verify Account';
    }
}


// -------------------------------------------------------------------------
// MAIN FORM LISTENER: Pauses original flow and initiates code send
// -------------------------------------------------------------------------
document.getElementById("signupForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    // 1. Gather all data
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const cnic = document.getElementById("cnic").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const email = document.getElementById("email").value.trim();
    
    if (!username || !password || !cnic || !phone || !email) {
       alert("Please fill all fields.");
       return;
    }
    
    // 2. Store data globally (for verification/final signup)
    pendingFormData = { username, password, cnic, phone, email };

    // 3. Trigger API to send verification code (Backend API: /api/accounts/send-verification-code/)
    try {
        const sendCodeResponse = await fetch("http://127.0.0.1:8000/api/accounts/send-verification-code/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, username: username }),
        });

        const data = await sendCodeResponse.json();

        if (sendCodeResponse.ok) {
            // Code sent successfully, show the verification modal
            document.getElementById("verification-modal").style.display = 'flex';
            document.getElementById("verificationCode").value = ''; 
            document.getElementById("modalMessage").textContent = "Code sent! Check your inbox.";
            alert("Verification code sent! Please check your email.");

            // Optional: Clear form fields after data is stored
            document.getElementById("signupForm").reset();

        } else {
            // Error: If email is already registered (unique constraint violation), the backend returns error here.
            alert("Error sending code: " + (data.error || "Account might already exist or inputs are invalid."));
        }

    } catch (error) {
        console.error("Error sending verification code:", error);
        alert("Network error. Could not connect to verification service.");
    }
});