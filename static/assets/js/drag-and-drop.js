document.addEventListener("DOMContentLoaded", () => {

    const sortableLists = document.querySelectorAll(
        "[data-drag-drop]"
    );

    sortableLists.forEach((list) => {

        let draggedItem = null;


        /* ========================================
           DRAG START
        ======================================== */

        list.addEventListener("dragstart", (event) => {

            const item = event.target.closest(
                "[data-drag-item]"
            );

            if (!item) {
                return;
            }

            draggedItem = item;

            item.classList.add("dragging");

            event.dataTransfer.effectAllowed = "move";

        });


        /* ========================================
           DRAG END
        ======================================== */

        list.addEventListener("dragend", () => {

            if (!draggedItem) {
                return;
            }

            draggedItem.classList.remove("dragging");

            draggedItem = null;

            saveOrder(list);

        });


        /* ========================================
           DRAG OVER
        ======================================== */

        list.addEventListener("dragover", (event) => {

            event.preventDefault();

            if (!draggedItem) {
                return;
            }

            const target = event.target.closest(
                "[data-drag-item]"
            );

            if (!target || target === draggedItem) {
                return;
            }

            const rect =
                target.getBoundingClientRect();

            const middle =
                rect.top + rect.height / 2;


            if (event.clientY < middle) {

                list.insertBefore(
                    draggedItem,
                    target
                );

            } else {

                list.insertBefore(
                    draggedItem,
                    target.nextSibling
                );

            }

        });

    });


    /* ========================================
       SAVE ORDER
    ======================================== */

    async function saveOrder(list) {

        const items = list.querySelectorAll(
            "[data-drag-item]"
        );

        const ids = Array.from(items).map(
            (item) => item.dataset.dragId
        );

        const url = list.dataset.dragUrl;

        const parameter =
            list.dataset.dragParameter || "ids[]";


        if (!url) {

            console.error(
                "Drag & Drop: no se encontró la URL."
            );

            return;
        }


        if (!ids.length) {
            return;
        }


        const csrfToken =
            document.querySelector(
                "[name=csrfmiddlewaretoken]"
            )?.value;


        if (!csrfToken) {

            console.error(
                "Drag & Drop: no se encontró el token CSRF."
            );

            return;
        }


        const body = new URLSearchParams();


        ids.forEach((id) => {

            body.append(
                parameter,
                id
            );

        });


        try {

            const response = await fetch(url, {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/x-www-form-urlencoded",

                    "X-CSRFToken":
                        csrfToken,

                },

                body: body.toString(),

            });


            const data =
                await response.json();


            if (!response.ok || !data.success) {

                throw new Error(
                    data.error ||
                    "No se pudo guardar el orden."
                );

            }


            console.log(
                "Orden guardado correctamente."
            );


        } catch (error) {

            console.error(
                "Drag & Drop:",
                error
            );

        }

    }

});