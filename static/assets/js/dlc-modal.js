document.addEventListener("DOMContentLoaded", () => {

    /* ========================================
       ELEMENTOS DEL DOM
    ======================================== */

    const modal =
        document.getElementById("dlc-modal");

    const openButton =
        document.getElementById("open-dlc-modal");

    const openEmptyButton =
        document.getElementById("open-dlc-modal-empty");

    const closeButton =
        document.getElementById("close-dlc-modal");

    const cancelButton =
        document.getElementById("cancel-dlc-modal");

    const form =
        document.getElementById("dlc-form");

    const modalTitle =
        document.getElementById("dlc-modal-title");

    const modalSubmit =
        document.getElementById("dlc-modal-submit");


    /* ========================================
       CAMPOS
    ======================================== */

    const titleInput =
        document.getElementById("id_title");

    const descriptionInput =
        document.getElementById("id_description");

    const typeInput =
        document.getElementById("id_type");

    const coverInput =
        document.getElementById("id_cover");

    const releaseDateInput =
        document.getElementById("id_release_date");

    const purchaseUrlInput =
        document.getElementById("id_purchase_url");


    /* ========================================
       PREVIEW
    ======================================== */

    const preview =
        document.getElementById("dlc-cover-preview");

    const previewImage =
        document.getElementById("dlc-preview-image");


    /* ========================================
       BOTONES EDITAR
    ======================================== */

    const editButtons =
        document.querySelectorAll(".btn-edit-dlc");


    /* ========================================
       LISTA
    ======================================== */

    const dlcsList =
        document.querySelector(".dlcs-list");

    const gameId =
        dlcsList?.dataset.gameId;


    /* ========================================
       VALIDACIÓN
    ======================================== */

    if (!modal) {

        console.error(
            "dlc-modal.js: No se encontró #dlc-modal"
        );

        return;

    }


    /* ========================================
       ABRIR MODAL - AGREGAR
    ======================================== */

    const openModal = () => {

        console.log(
            "Abriendo modal de DLC..."
        );


        if (form) {

            form.reset();

        }


        /* -------------------------------
           LIMPIAR PREVIEW
        -------------------------------- */

        if (previewImage) {

            previewImage.src = "";

        }

        if (preview) {

            preview.classList.remove("show");

        }


        /* -------------------------------
           CONFIGURAR TÍTULO
        -------------------------------- */

        if (modalTitle) {

            modalTitle.textContent =
                "Agregar DLC";

        }


        /* -------------------------------
           CONFIGURAR BOTÓN
        -------------------------------- */

        if (modalSubmit) {

            const submitText =
                modalSubmit.querySelector("span");

            if (submitText) {

                submitText.textContent =
                    "Guardar DLC";

            }

        }


        /* -------------------------------
           PORTADA OBLIGATORIA
        -------------------------------- */

        if (coverInput) {

            coverInput.required = true;

        }


        /* -------------------------------
           ACTION CREACIÓN
        -------------------------------- */

        if (form && gameId) {

            form.action =
                `/moderator/games/${gameId}/dlcs/create/`;

        }


        /* -------------------------------
           MOSTRAR MODAL
        -------------------------------- */

        modal.style.display = "flex";


        if (titleInput) {

            setTimeout(() => {

                titleInput.focus();

            }, 50);

        }


        console.log(
            "Modal de DLC abierto"
        );

    };


    /* ========================================
       ABRIR MODAL - EDITAR
    ======================================== */

    const openEditModal = async (dlcId) => {

        try {

            console.log(
                "Cargando DLC para editar..."
            );


            if (!gameId) {

                throw new Error(
                    "No se encontró el ID del juego."
                );

            }


            const url =
                `/moderator/games/${gameId}/dlcs/${dlcId}/edit/`;


            const response =
                await fetch(url);


            if (!response.ok) {

                throw new Error(
                    "No se pudo obtener el DLC."
                );

            }


            const data =
                await response.json();


            /* ==============================
               TÍTULO DEL MODAL
            ============================== */

            if (modalTitle) {

                modalTitle.textContent =
                    "Editar DLC";

            }


            /* ==============================
               BOTÓN
            ============================== */

            if (modalSubmit) {

                const submitText =
                    modalSubmit.querySelector("span");

                if (submitText) {

                    submitText.textContent =
                        "Guardar cambios";

                }

            }


            /* ==============================
               TÍTULO
            ============================== */

            if (titleInput) {

                titleInput.value =
                    data.title || "";

            }


            /* ==============================
               DESCRIPCIÓN
            ============================== */

            if (descriptionInput) {

                descriptionInput.value =
                    data.description || "";

            }


            /* ==============================
               TIPO
            ============================== */

            if (typeInput) {

                typeInput.value =
                    data.type || "EXPANSION";

            }


            /* ==============================
               FECHA
            ============================== */

            if (releaseDateInput) {

                releaseDateInput.value =
                    data.release_date || "";

            }


            /* ==============================
               URL DE COMPRA
            ============================== */

            if (purchaseUrlInput) {

                purchaseUrlInput.value =
                    data.purchase_url || "";

            }


            /* ==============================
               PORTADA ACTUAL
            ============================== */

            if (data.cover && previewImage) {

                previewImage.src =
                    data.cover;

                preview?.classList.add("show");

            } else {

                if (previewImage) {

                    previewImage.src = "";

                }

                preview?.classList.remove("show");

            }


            /*
             * En edición NO obligamos
             * a seleccionar una nueva portada.
             */

            if (coverInput) {

                coverInput.required = false;

            }


            /* ==============================
               ACTION EDICIÓN
            ============================== */

            if (form) {

                form.action =
                    url;

            }


            /* ==============================
               MOSTRAR MODAL
            ============================== */

            modal.style.display = "flex";


            if (titleInput) {

                setTimeout(() => {

                    titleInput.focus();

                }, 50);

            }


            console.log(
                "DLC cargado correctamente."
            );


        } catch (error) {

            console.error(
                "Error al cargar DLC:",
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
       BOTÓN AGREGAR - ESTADO VACÍO
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

                const dlcId =
                    button.dataset.dlcId;


                if (!dlcId) {

                    console.error(
                        "No se encontró data-dlc-id."
                    );

                    return;

                }


                await openEditModal(
                    dlcId
                );

            }
        );

    });


    /* ========================================
       BOTÓN CERRAR
    ======================================== */

    if (closeButton) {

        closeButton.addEventListener(
            "click",
            closeModal
        );

    }


    /* ========================================
       BOTÓN CANCELAR
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
       PREVIEW DE PORTADA
    ======================================== */

    if (coverInput) {

        coverInput.addEventListener(
            "change",
            () => {

                const file =
                    coverInput.files?.[0];


                if (!file) {

                    return;

                }


                if (!file.type.startsWith("image/")) {

                    console.warn(
                        "El archivo seleccionado no es una imagen."
                    );

                    coverInput.value = "";

                    return;

                }


                const reader =
                    new FileReader();


                reader.onload = (event) => {

                    if (previewImage) {

                        previewImage.src =
                            event.target.result;

                    }

                    if (preview) {

                        preview.classList.add(
                            "show"
                        );

                    }

                };


                reader.readAsDataURL(file);

            }
        );

    }


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