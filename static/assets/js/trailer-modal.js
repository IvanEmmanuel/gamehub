document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("trailer-modal");
    const openButton = document.getElementById("open-trailer-modal");
    const closeButton = document.getElementById("close-trailer-modal");
    const cancelButton = document.getElementById("cancel-trailer-modal");
    const editButtons = document.querySelectorAll(".open-edit-trailer-modal");
    const modalTitle = document.getElementById("trailer-modal-title");
    const modalSubmit = document.getElementById("trailer-modal-submit")
    const modalForm = document.getElementById("trailer-form")
    const titleInput = document.getElementById("id_title");
    const youtubeInput = document.getElementById("id_youtube_url");
    const officialInput = document.getElementById("id_is_official");
    
    editButtons.forEach((button) => {

    button.addEventListener("click", () => {

            const title = button.dataset.trailerTitle;
            const url = button.dataset.trailerUrl;
            const official = button.dataset.trailerOfficial;
            const updateUrl = button.dataset.updateUrl;

            titleInput.value = title;
            youtubeInput.value = url;

            officialInput.checked = official === "True";

            modalTitle.textContent = "Editar tráiler";

            modalSubmit.querySelector("span").textContent =
                "Guardar cambios";

            modalForm.action = updateUrl;

            modal.style.display = "flex";

        });

    });

    if (!modal || !openButton) {
        return;
    }

    const openModal = () => {

        modalForm.reset();

        modalTitle.textContent = "Agregar tráiler";

        modalSubmit.querySelector("span").textContent =
            "Guardar tráiler";

        modalForm.action =
            modalForm.dataset.createUrl;

        modal.style.display = "flex";

    };

    const closeModal = () => {

        modal.style.display = "none";

    };

    openButton.addEventListener("click", openModal);

    closeButton?.addEventListener("click", closeModal);

    cancelButton?.addEventListener("click", closeModal);

    modal.addEventListener("click", (event) => {

        if (event.target === modal) {

            closeModal();

        }

    });

});