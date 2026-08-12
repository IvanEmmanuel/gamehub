console.log("Delete modal cargado");

document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("deleteModal");

    const itemName = document.getElementById("deleteItemName");

    const deleteForm = document.getElementById("deleteForm");


    document.querySelectorAll(".open-delete-modal").forEach(button => {

        button.addEventListener("click", e => {

            e.preventDefault();

            console.log("Click en eliminar");

            itemName.textContent = button.dataset.itemName;

            deleteForm.action = button.dataset.deleteUrl;

            modal.classList.add("show");

        });

    });


    document.getElementById("cancelDelete").addEventListener("click", () => {

        modal.classList.remove("show");

    });

});