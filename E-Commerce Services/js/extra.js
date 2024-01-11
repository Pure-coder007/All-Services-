// SIGN UP FORM

const cont = document.querySelector(".cont");
const signUpLink = document.querySelector(".signup-link");
const signInLink = document.querySelector(".signin-link");

signUpLink.addEventListener("click", () => {
    cont.classList.add("navigate");
});

signInLink.addEventListener("click", () => {
    cont.classList.remove("navigate");
});