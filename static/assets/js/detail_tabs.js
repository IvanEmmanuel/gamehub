document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll(".tab-btn");

    const contents = document.querySelectorAll(".tab-content");

    buttons.forEach(button => {

        button.addEventListener("click", () => {

            const target = button.dataset.tab;

            // Botones
            buttons.forEach(btn => btn.classList.remove("active"));
            button.classList.add("active");

            // Contenido
            contents.forEach(content => {

                content.classList.remove("active");

            });

            document
                .getElementById(target)
                .classList.add("active");

        });

    });

});