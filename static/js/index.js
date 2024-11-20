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

function mostraMessaggio() {
    alert("Ti ho hackerato il computer :)")
}

function passwordSbagliata() {
    alert("Username o password sbagliati")
}

window.addEventListener("load", mostraMessaggio)

