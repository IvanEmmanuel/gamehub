document.addEventListener("DOMContentLoaded", () => {

    /* ========================================
       ELEMENTOS DEL DOM
    ======================================== */

    const modal =
        document.getElementById("patch-note-modal");

    const openButton =
        document.getElementById("open-patch-note-modal");

    const openEmptyButton =
        document.getElementById("open-patch-note-modal-empty");

    const closeButton =
        document.getElementById("close-patch-note-modal");

    const cancelButton =
        document.getElementById("cancel-patch-note-modal");

    const form =
        document.getElementById("patch-note-form");

    const modalTitle =
        document.getElementById("patch-note-modal-title");

    const modalSubmit =
        document.getElementById("patch-note-modal-submit");


    /* ========================================
       CAMPOS
    ======================================== */

    const versionInput =
        document.getElementById("id_version");

    const titleInput =
        document.getElementById("id_title");

    const descriptionInput =
        document.getElementById("id_description");

    const releaseDateInput =
        document.getElementById("id_release_date");

    const officialUrlInput =
        document.getElementById("id_official_url");


    /* ========================================
       BOTONES EDITAR
    ======================================== */

    const editButtons =
        document.querySelectorAll(".btn-edit-patch-note");


    /* ========================================
       LISTA
    ======================================== */

    const patchNotesList =
        document.querySelector(".patch-notes-list");

    const gameId =
        patchNotesList?.dataset.gameId;


    /* ========================================
       VALIDACIÓN
    ======================================== */

    if (!modal) {

        console.error(
            "patch-note-modal.js: No se encontró #patch-note-modal"
        );

        return;

    }


    /* ========================================
       ABRIR MODAL - AGREGAR
    ======================================== */

    const openModal = () => {

        console.log(
            "Abriendo modal de Patch Note..."
        );


        if (form) {

            form.reset();

        }


        if (modalTitle) {

            modalTitle.textContent =
                "Agregar Patch Note";

        }


        if (modalSubmit) {

            const submitText =
                modalSubmit.querySelector("span");

            if (submitText) {

                submitText.textContent =
                    "Guardar Patch Note";

            }

        }


        if (form && gameId) {

            form.action =
                `/moderator/games/${gameId}/patch-notes/create/`;

        }


        modal.style.display = "flex";


        if (versionInput) {

            setTimeout(() => {

                versionInput.focus();

            }, 50);

        }

    };


    /* ========================================
       ABRIR MODAL - EDITAR
    ======================================== */

    const openEditModal = async (patchNoteId) => {

        try {

            console.log(
                "Cargando Patch Note para editar..."
            );


            if (!gameId) {

                throw new Error(
                    "No se encontró el ID del juego."
                );

            }


            const url =
                `/moderator/games/${gameId}/patch-notes/${patchNoteId}/edit/`;


            const response =
                await fetch(url);


            if (!response.ok) {

                throw new Error(
                    "No se pudo obtener el Patch Note."
                );

            }


            const data =
                await response.json();


            /* ==================================
               MODAL
            ================================== */

            if (modalTitle) {

                modalTitle.textContent =
                    "Editar Patch Note";

            }


            if (modalSubmit) {

                const submitText =
                    modalSubmit.querySelector("span");

                if (submitText) {

                    submitText.textContent =
                        "Guardar cambios";

                }

            }


            /* ==================================
               CAMPOS
            ================================== */

            if (versionInput) {

                versionInput.value =
                    data.version || "";

            }


            if (titleInput) {

                titleInput.value =
                    data.title || "";

            }


            if (descriptionInput) {

                descriptionInput.value =
                    data.description || "";

            }


            if (releaseDateInput) {

                releaseDateInput.value =
                    data.release_date || "";

            }


            if (officialUrlInput) {

                officialUrlInput.value =
                    data.official_url || "";

            }


            /* ==================================
               ACTION
            ================================== */

            if (form) {

                form.action =
                    url;

            }


            /* ==================================
               MOSTRAR MODAL
            ================================== */

            modal.style.display = "flex";


            if (versionInput) {

                setTimeout(() => {

                    versionInput.focus();

                }, 50);

            }


            console.log(
                "Patch Note cargado correctamente."
            );


        } catch (error) {

            console.error(
                "Error al cargar Patch Note:",
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

                const patchNoteId =
                    button.dataset.patchNoteId;


                if (!patchNoteId) {

                    console.error(
                        "No se encontró data-patch-note-id."
                    );

                    return;

                }


                await openEditModal(
                    patchNoteId
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