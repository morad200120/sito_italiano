const hamMenu = document.querySelector(".ham-menu");
const offScreenMenu = document.querySelector(".off-screen-menu");

hamMenu.addEventListener("click", () => {
    hamMenu.classList.toggle("active");
    offScreenMenu.classList.toggle("active");
    console.log("Menu toggled");
});


const addArticleButton = document.querySelector("#aggiungi-articolo");
const inputBoxContainer = document.querySelector(".input-box-container");
const blur = document.querySelector(".blur-container");

addArticleButton.addEventListener("click", () => {
    inputBoxContainer.classList.toggle("active");
    blur.classList.toggle("active");
});


document.addEventListener("click", (event) => {
    if (!inputBoxContainer.contains(event.target) && !addArticleButton.contains(event.target)) {
        inputBoxContainer.classList.remove("active");
        blur.classList.remove("active");
    }
});


const mainForm = document.getElementById("login-form");

mainForm.onsubmit = function(event) {
    event.preventDefault();

    const username = "admin";
    const password = "admin";

    const usernameInserito = document.getElementsByName("username")[0].value;
    const passwordInserita = document.getElementsByName("password")[0].value;

    const errorMessage = document.getElementById("error-message");

    if (usernameInserito !== username || passwordInserita !== password) {
        errorMessage.classList.add("active"); // Aggiunge la classe "active" per mostrare l'errore
        return false; 
    }

    errorMessage.classList.remove("active"); // Rimuove l'errore se le credenziali sono corrette
    mainForm.submit(); // Procede con l'invio del form
};

