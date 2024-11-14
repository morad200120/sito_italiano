const hamMenu = document.querySelector(".ham-menu");
const offScreenMenu = document.querySelector(".off-screen-menu");

hamMenu.addEventListener("click", () => {
    hamMenu.classList.toggle("active");
    offScreenMenu.classList.toggle("active");
    console.log("Menu toggled"); // Per vedere se funziona
});


const addArticleButton = document.querySelector("#aggiungi-articolo")
const inputBoxContainer = document.querySelector(".input-box-container")


addArticleButton.addEventListener("click", () => {
    inputBoxContainer.classList.toggle("active")
})

