document.addEventListener("DOMContentLoaded", () => {

    const screenshotsContainer = document.querySelector(".screenshots");
    const screenshots = document.querySelectorAll(".screenshot");

    const prevButton = document.querySelector(".screenshot-arrow.left");
    const nextButton = document.querySelector(".screenshot-arrow.right");

    const pagination = document.querySelector(".screenshots-pagination");

    const screenshotsPerPage = 6;

    let currentPage = 0;

    // Si no existen capturas, no hacemos nada
    if (!screenshotsContainer || screenshots.length === 0) {
        return;
    }

    const totalPages = Math.ceil(
        screenshots.length / screenshotsPerPage
    );

    // Crear indicadores
    for (let i = 0; i < totalPages; i++) {

        const indicator = document.createElement("span");

        if (i === 0) {
            indicator.classList.add("active");
        }

        pagination.appendChild(indicator);
    }

    const indicators = pagination.querySelectorAll("span");


    function showPage(page) {

        currentPage = page;

        const start = currentPage * screenshotsPerPage;
        const end = start + screenshotsPerPage;

        screenshots.forEach((screenshot, index) => {

            if (index >= start && index < end) {
                screenshot.style.display = "";
            } else {
                screenshot.style.display = "none";
            }

        });


        // Actualizar indicador
        indicators.forEach((indicator, index) => {

            indicator.classList.toggle(
                "active",
                index === currentPage
            );

        });


        // Controlar flechas
        prevButton.disabled = currentPage === 0;
        nextButton.disabled = currentPage === totalPages - 1;

    }


    // Flecha izquierda
    prevButton.addEventListener("click", () => {

        if (currentPage > 0) {
            showPage(currentPage - 1);
        }

    });


    // Flecha derecha
    nextButton.addEventListener("click", () => {

        if (currentPage < totalPages - 1) {
            showPage(currentPage + 1);
        }

    });


    // Estado inicial
    showPage(0);

});