document.addEventListener("DOMContentLoaded", () => {

    const modal = document.getElementById("screenshot-modal");
    const openButton = document.getElementById("open-screenshot-modal");
    const closeButton = document.getElementById("close-screenshot-modal");
    const cancelButton = document.getElementById("cancel-screenshot-modal");

    const form = document.getElementById("screenshot-form");

    const imageInput = document.getElementById("id_image");

    const preview = document.getElementById("screenshot-preview");
    const previewImage = document.getElementById("screenshot-preview-image");

    const modalTitle = document.getElementById("screenshot-modal-title");
    const modalSubmit = document.getElementById("screenshot-modal-submit");

    const editButtons = document.querySelectorAll(".btn-edit-screenshot");

    const screenshotsList = document.querySelector(".screenshots-list");

    const gameId = screenshotsList?.dataset.gameId;


    if (!modal || !form) {
        return;
    }


    /* ========================================
       ABRIR MODAL
    ======================================== */

    const openModal = () => {

        console.log("Abriendo modal de screenshot...");

        form.reset();

        if (previewImage) {
            previewImage.src = "";
        }

        if (preview) {
            preview.classList.remove("show");
        }

        if (modalTitle) {
            modalTitle.textContent = "Agregar screenshot";
        }

        if (modalSubmit) {

            const submitText =
                modalSubmit.querySelector("span");

            if (submitText) {
                submitText.textContent =
                    "Guardar screenshot";
            }

        }

        modal.style.display = "flex";

        console.log("Modal abierto");

    };

    /* ========================================
    ABRIR MODAL - EDITAR
    ======================================== */

    const openEditModal = async (url) => {

        try {

            const response = await fetch(url);

            if (!response.ok) {

                throw new Error(
                    "No se pudo obtener el screenshot."
                );

            }


            const data = await response.json();


            /* ==============================
            CONFIGURAR MODAL
            ============================== */

            if (modalTitle) {

                modalTitle.textContent =
                    "Editar screenshot";

            }


            const submitText =
                modalSubmit?.querySelector("span");

            if (submitText) {

                submitText.textContent =
                    "Guardar cambios";

            }


            /* ==============================
            CARGAR TÍTULO
            ============================== */

            const titleInput =
                document.getElementById("id_title");

            if (titleInput) {

                titleInput.value =
                    data.title || "";

            }


            /* ==============================
            CARGAR IMAGEN ACTUAL
            ============================== */

            if (data.image && previewImage) {

                previewImage.src =
                    data.image;

                preview?.classList.add("show");

            }


            /* ==============================
            CONFIGURAR FORMULARIO
            ============================== */

            form.action = url;


            /* ==============================
            MOSTRAR MODAL
            ============================== */

            modal.style.display = "flex";


        } catch (error) {

            console.error(
                "Error al cargar screenshot:",
                error
            );

        }

    };


    /* ========================================
       CERRAR MODAL
    ======================================== */

    const closeModal = () => {

        modal.style.display = "none";

        form.reset();

        previewImage.src = "";

        preview.classList.remove("show");

    };


    /* ========================================
       BOTONES
    ======================================== */

    openButton?.addEventListener("click", () => {

        console.log("CLICK EN AGREGAR SCREENSHOT");

        openModal();

    });


    closeButton?.addEventListener(
        "click",
        closeModal
    );


    cancelButton?.addEventListener(
        "click",
        closeModal
    );


    /* ========================================
       CERRAR AL HACER CLICK FUERA
    ======================================== */

    modal.addEventListener("click", (event) => {

        if (event.target === modal) {

            closeModal();

        }

    });

    editButtons.forEach((button) => {

        button.addEventListener("click", async () => {

            const screenshotId =
                button.dataset.screenshotId;

            if (!screenshotId || !gameId) {
                return;
            }

            const url =
                `/moderator/games/${gameId}/screenshots/${screenshotId}/edit/`;

            await openEditModal(url);

        });

    });


    /* ========================================
       PREVISUALIZACIÓN DE IMAGEN
    ======================================== */

    imageInput?.addEventListener("change", () => {

        const file = imageInput.files[0];

        if (!file) {

            previewImage.src = "";

            preview.classList.remove("show");

            return;

        }


        if (!file.type.startsWith("image/")) {

            previewImage.src = "";

            preview.classList.remove("show");

            return;

        }


        const imageUrl = URL.createObjectURL(file);

        previewImage.src = imageUrl;

        preview.classList.add("show");

    });

});