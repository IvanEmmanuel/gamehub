document.addEventListener("DOMContentLoaded", () => {

    /* ========================================
       ELEMENTOS DEL DOM
    ======================================== */

    const modal = document.getElementById("achievement-modal");

    const openButton = document.getElementById("open-achievement-modal");

    const closeButton = document.getElementById("close-achievement-modal");

    const cancelButton = document.getElementById("cancel-achievement-modal");

    const form = document.getElementById("achievement-form");

    const modalTitle = document.getElementById("achievement-modal-title");

    const modalSubmit = document.getElementById("achievement-modal-submit");

    const titleInput = document.getElementById("id_title");

    const descriptionInput = document.getElementById("id_description");

    const iconInput = document.getElementById("id_icon");

    const hiddenInput = document.getElementById("id_is_hidden");

    const preview = document.getElementById("achievement-icon-preview");

    const previewImage = document.getElementById("achievement-preview-image");

    const editButtons = document.querySelectorAll(".btn-edit-achievement");

    const achievementsList = document.querySelector(".achievements-list");

    const gameId = achievementsList?.dataset.gameId;


    /* ========================================
       VALIDACIÓN BÁSICA
    ======================================== */

    if (!modal) {

        console.error(
            "achievement-modal.js: No se encontró #achievement-modal"
        );

        return;

    }


    /* ========================================
       ABRIR MODAL - AGREGAR
    ======================================== */

    const openModal = () => {

        console.log(
            "Abriendo modal de achievement..."
        );


        /* -------------------------------
           LIMPIAR FORMULARIO
        -------------------------------- */

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
           CONFIGURAR TEXTOS
        -------------------------------- */

        if (modalTitle) {

            modalTitle.textContent =
                "Agregar logro";

        }


        if (modalSubmit) {

            const submitText =
                modalSubmit.querySelector("span");

            if (submitText) {

                submitText.textContent =
                    "Guardar logro";

            }

        }


        /* -------------------------------
           MOSTRAR MODAL
        -------------------------------- */

        modal.style.display = "flex";


        console.log(
            "Modal de achievement abierto"
        );

    };

    /* ========================================
    ABRIR MODAL - EDITAR
    ======================================== */

    const openEditModal = async (url) => {

        try {

            console.log(
                "Cargando achievement para editar..."
            );


            const response =
                await fetch(url);


            if (!response.ok) {

                throw new Error(
                    "No se pudo obtener el achievement."
                );

            }


            const data =
                await response.json();


            /* ==============================
            CONFIGURAR MODAL
            ============================== */

            if (modalTitle) {

                modalTitle.textContent =
                    "Editar logro";

            }


            const submitText =
                modalSubmit?.querySelector("span");


            if (submitText) {

                submitText.textContent =
                    "Guardar cambios";

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
            LOGRO OCULTO
            ============================== */

            if (hiddenInput) {

                hiddenInput.checked =
                    Boolean(data.is_hidden);

            }


            /* ==============================
            ICONO ACTUAL
            ============================== */

            if (data.icon && previewImage) {

                previewImage.src =
                    data.icon;

                preview?.classList.add("show");

            } else {

                if (previewImage) {

                    previewImage.src = "";

                }

                preview?.classList.remove("show");

            }


            /* ==============================
            CAMBIAR ACTION DEL FORM
            ============================== */

            if (form) {

                form.action = url;

            }


            /* ==============================
            MOSTRAR MODAL
            ============================== */

            modal.style.display = "flex";


            console.log(
                "Achievement cargado correctamente."
            );


        } catch (error) {

            console.error(
                "Error al cargar achievement:",
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
    BOTONES EDITAR
    ======================================== */

    editButtons.forEach((button) => {

        button.addEventListener("click", async () => {

            const achievementId =
                button.dataset.achievementId;


            if (!achievementId || !gameId) {

                console.error(
                    "Falta achievementId o gameId."
                );

                return;

            }


            const url =
                `/moderator/games/${gameId}/achievements/${achievementId}/edit/`;


            await openEditModal(url);

        });

    });


    /* ========================================
       BOTÓN CERRAR (X)
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
       CERRAR AL HACER CLICK EN EL FONDO
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
       PREVIEW DEL ICONO
    ======================================== */

    if (iconInput) {

        iconInput.addEventListener(
            "change",
            () => {

                const file =
                    iconInput.files?.[0];

                if (!file) {

                    if (previewImage) {

                        previewImage.src = "";

                    }

                    if (preview) {

                        preview.classList.remove(
                            "show"
                        );

                    }

                    return;

                }


                /* -------------------------------
                   VALIDAR TIPO
                -------------------------------- */

                if (!file.type.startsWith("image/")) {

                    console.warn(
                        "El archivo seleccionado no es una imagen."
                    );

                    iconInput.value = "";

                    if (preview) {

                        preview.classList.remove(
                            "show"
                        );

                    }

                    return;

                }


                /* -------------------------------
                   CREAR PREVIEW
                -------------------------------- */

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