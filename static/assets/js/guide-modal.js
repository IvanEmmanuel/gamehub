document.addEventListener("DOMContentLoaded", () => {

    /* ========================================
       ELEMENTOS DEL DOM
    ======================================== */

    const modal =
        document.getElementById("guide-modal");

    const openButton =
        document.getElementById("open-guide-modal");

    const openEmptyButton =
        document.getElementById("open-guide-modal-empty");

    const closeButton =
        document.getElementById("close-guide-modal");

    const cancelButton =
        document.getElementById("cancel-guide-modal");

    const form =
        document.getElementById("guide-form");

    const modalTitle =
        document.getElementById("guide-modal-title");

    const modalSubmit =
        document.getElementById("guide-modal-submit");


    /* ========================================
       CAMPOS
    ======================================== */

    const titleInput =
        document.getElementById("id_title");

    const descriptionInput =
        document.getElementById("id_description");

    const urlInput =
        document.getElementById("id_url");

    const sourceInput =
        document.getElementById("id_source");


    /* ========================================
       BOTONES EDITAR
    ======================================== */

    const editButtons =
        document.querySelectorAll(".btn-edit-guide");


    /* ========================================
       INFORMACIÓN DEL JUEGO
    ======================================== */

    const guidesList =
        document.querySelector(".guides-list");

    const gameId =
        guidesList?.dataset.gameId;


    /* ========================================
       VALIDACIÓN
    ======================================== */

    if (!modal) {

        console.error(
            "guide-modal.js: No se encontró #guide-modal"
        );

        return;

    }


    /* ========================================
       ABRIR MODAL - AGREGAR
    ======================================== */

    const openModal = () => {

        console.log(
            "Abriendo modal de guía..."
        );


        if (form) {

            form.reset();

        }


        if (modalTitle) {

            modalTitle.textContent =
                "Agregar guía";

        }


        if (modalSubmit) {

            const submitText =
                modalSubmit.querySelector("span");

            if (submitText) {

                submitText.textContent =
                    "Guardar guía";

            }

        }


        /* ------------------------------------
           ACTION CREAR
        ------------------------------------ */

        if (form && gameId) {

            form.action =
                `/moderator/games/${gameId}/guides/create/`;

        }


        modal.style.display = "flex";


        if (titleInput) {

            setTimeout(() => {

                titleInput.focus();

            }, 50);

        }


        console.log(
            "Modal de guía abierto"
        );

    };


    /* ========================================
       ABRIR MODAL - EDITAR
    ======================================== */

    const openEditModal = async (guideId) => {

        try {

            console.log(
                "Cargando guía para editar..."
            );


            if (!gameId) {

                throw new Error(
                    "No se encontró el ID del juego."
                );

            }


            const url =
                `/moderator/games/${gameId}/guides/${guideId}/edit/`;


            const response =
                await fetch(url);


            if (!response.ok) {

                throw new Error(
                    "No se pudo obtener la guía."
                );

            }


            const data =
                await response.json();


            /* ------------------------------------
               MODAL
            ------------------------------------ */

            if (modalTitle) {

                modalTitle.textContent =
                    "Editar guía";

            }


            if (modalSubmit) {

                const submitText =
                    modalSubmit.querySelector("span");

                if (submitText) {

                    submitText.textContent =
                        "Guardar cambios";

                }

            }


            /* ------------------------------------
               CAMPOS
            ------------------------------------ */

            if (titleInput) {

                titleInput.value =
                    data.title || "";

            }


            if (descriptionInput) {

                descriptionInput.value =
                    data.description || "";

            }


            if (urlInput) {

                urlInput.value =
                    data.url || "";

            }


            if (sourceInput) {

                sourceInput.value =
                    data.source || "OTHER";

            }


            /* ------------------------------------
               ACTION EDITAR
            ------------------------------------ */

            if (form) {

                form.action =
                    url;

            }


            /* ------------------------------------
               MOSTRAR MODAL
            ------------------------------------ */

            modal.style.display = "flex";


            if (titleInput) {

                setTimeout(() => {

                    titleInput.focus();

                }, 50);

            }


            console.log(
                "Guía cargada correctamente."
            );


        } catch (error) {

            console.error(
                "Error al cargar guía:",
                error
            );

        }

    };


    /* ========================================
       CERRAR MODAL
    ======================================== */

    const closeModal = () => {

        modal.style.display = "none";

    };


    /* ========================================
       BOTÓN AGREGAR
    ======================================== */

    if (openButton) {

        openButton.addEventListener(
            "click",
            openModal
        );

    }


    /* ========================================
       ESTADO VACÍO
    ======================================== */

    if (openEmptyButton) {

        openEmptyButton.addEventListener(
            "click",
            openModal
        );

    }


    /* ========================================
       BOTONES EDITAR
    ======================================== */

    editButtons.forEach((button) => {

        button.addEventListener(
            "click",
            async () => {

                const guideId =
                    button.dataset.guideId;


                if (!guideId) {

                    console.error(
                        "No se encontró data-guide-id."
                    );

                    return;

                }


                await openEditModal(
                    guideId
                );

            }
        );

    });


    /* ========================================
       CERRAR - X
    ======================================== */

    if (closeButton) {

        closeButton.addEventListener(
            "click",
            closeModal
        );

    }


    /* ========================================
       CERRAR - CANCELAR
    ======================================== */

    if (cancelButton) {

        cancelButton.addEventListener(
            "click",
            closeModal
        );

    }


    /* ========================================
       CERRAR AL HACER CLICK FUERA
    ======================================== */

    modal.addEventListener(
        "click",
        (event) => {

            if (event.target === modal) {

                closeModal();

            }

        }
    );


    /* ========================================
       ESC PARA CERRAR
    ======================================== */

    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Escape" &&
                modal.style.display === "flex"
            ) {

                closeModal();

            }

        }
    );


    /* ========================================
       EVITAR DOBLE SUBMIT
    ======================================== */

    if (form) {

        form.addEventListener(
            "submit",
            () => {

                if (modalSubmit) {

                    modalSubmit.disabled = true;

                    const submitText =
                        modalSubmit.querySelector("span");

                    if (submitText) {

                        submitText.textContent =
                            "Guardando...";

                    }

                }

            }
        );

    }

});