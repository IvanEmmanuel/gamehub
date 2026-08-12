document.addEventListener("DOMContentLoaded", () => {

    /* ========================================
       ELEMENTOS DEL DOM
    ======================================== */

    const modal =
        document.getElementById("soundtrack-modal");

    const openButton =
        document.getElementById("open-soundtrack-modal");

    const openEmptyButton =
        document.getElementById("open-soundtrack-modal-empty");

    const closeButton =
        document.getElementById("close-soundtrack-modal");

    const cancelButton =
        document.getElementById("cancel-soundtrack-modal");

    const form =
        document.getElementById("soundtrack-form");

    const modalTitle =
        document.getElementById("soundtrack-modal-title");

    const modalSubmit =
        document.getElementById("soundtrack-modal-submit");

    const editButtons =
        document.querySelectorAll(".btn-edit-soundtrack");

    const soundtracksList =
        document.querySelector(".soundtracks-list");

    const gameId =
        soundtracksList?.dataset.gameId;


    /* ========================================
       CAMPOS
    ======================================== */

    const titleInput =
        document.getElementById("id_title");

    const artistInput =
        document.getElementById("id_artist");

    const spotifyInput =
        document.getElementById("id_spotify_url");

    const youtubeInput =
        document.getElementById("id_youtube_url");


    /* ========================================
       VALIDACIÓN
    ======================================== */

    if (!modal) {

        console.error(
            "soundtrack-modal.js: No se encontró #soundtrack-modal"
        );

        return;

    }


    /* ========================================
       ABRIR MODAL - AGREGAR
    ======================================== */

    const openModal = () => {

        console.log(
            "Abriendo modal de soundtrack..."
        );


        if (form) {

            form.reset();

        }


        if (modalTitle) {

            modalTitle.textContent =
                "Agregar canción";

        }


        if (modalSubmit) {

            const submitText =
                modalSubmit.querySelector("span");

            if (submitText) {

                submitText.textContent =
                    "Guardar canción";

            }

        }


        /*
         * IMPORTANTE:
         * Restauramos el action de creación.
         */

        if (form && gameId) {

            form.action =
                `/moderator/games/${gameId}/soundtrack/create/`;

        }


        modal.style.display = "flex";


        if (titleInput) {

            setTimeout(() => {

                titleInput.focus();

            }, 50);

        }


        console.log(
            "Modal de soundtrack abierto"
        );

    };


    /* ========================================
       ABRIR MODAL - EDITAR
    ======================================== */

    const openEditModal = async (soundtrackId) => {

        try {

            console.log(
                "Cargando soundtrack para editar..."
            );


            if (!gameId) {

                throw new Error(
                    "No se encontró el ID del juego."
                );

            }


            const url =
                `/moderator/games/${gameId}/soundtrack/${soundtrackId}/edit/`;


            const response =
                await fetch(url);


            if (!response.ok) {

                throw new Error(
                    "No se pudo obtener el soundtrack."
                );

            }


            const data =
                await response.json();


            /* ==============================
               CONFIGURAR MODAL
            ============================== */

            if (modalTitle) {

                modalTitle.textContent =
                    "Editar canción";

            }


            if (modalSubmit) {

                const submitText =
                    modalSubmit.querySelector("span");

                if (submitText) {

                    submitText.textContent =
                        "Guardar cambios";

                }

            }


            /* ==============================
               CARGAR DATOS
            ============================== */

            if (titleInput) {

                titleInput.value =
                    data.title || "";

            }


            if (artistInput) {

                artistInput.value =
                    data.artist || "";

            }


            if (spotifyInput) {

                spotifyInput.value =
                    data.spotify_url || "";

            }


            if (youtubeInput) {

                youtubeInput.value =
                    data.youtube_url || "";

            }


            /* ==============================
               ACTION DE EDICIÓN
            ============================== */

            if (form) {

                form.action = url;

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
                "Soundtrack cargado correctamente."
            );

        } catch (error) {

            console.error(
                "Error al cargar soundtrack:",
                error
            );

        }

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

                const soundtrackId =
                    button.dataset.soundtrackId;


                if (!soundtrackId) {

                    console.error(
                        "No se encontró data-soundtrack-id."
                    );

                    return;

                }


                await openEditModal(
                    soundtrackId
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


    /* ========================================
       CERRAR MODAL
    ======================================== */

    function closeModal() {

        modal.style.display = "none";

    }

});