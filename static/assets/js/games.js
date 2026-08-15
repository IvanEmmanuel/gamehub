document.addEventListener("DOMContentLoaded", () => {

    const filterSections = document.querySelectorAll(
        ".filter-section"
    );

    filterSections.forEach(section => {

        const header = section.querySelector(
            ".filter-section-header"
        );

        if (!header) {
            return;
        }

        header.addEventListener("click", () => {

            const isActive = section.classList.contains("active");


            /*
             * Cerramos todas las secciones.
             */

            filterSections.forEach(item => {

                item.classList.remove("active");

            });


            /*
             * Si la sección que pulsamos
             * estaba cerrada, la abrimos.
             *
             * Si estaba abierta, permanece cerrada.
             */

            if (!isActive) {

                section.classList.add("active");

            }

        });

    });

});