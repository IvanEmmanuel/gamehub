console.log("Delete modal cargado");
document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("deleteModal");

    const gameName = document.getElementById("deleteGameName");

    const deleteForm = document.getElementById("deleteForm");

    document.querySelectorAll(".open-delete-modal").forEach(button => {

        button.addEventListener("click", e => {

            e.preventDefault();

            console.log("Click en eliminar");

            gameName.textContent = button.dataset.gameName;

            deleteForm.action = button.dataset.deleteUrl;

            modal.classList.add("show");

        });

    });

    document.getElementById("cancelDelete").addEventListener("click", () => {

        modal.classList.remove("show");

    });

});