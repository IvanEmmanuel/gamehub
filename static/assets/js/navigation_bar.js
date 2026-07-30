document.addEventListener("DOMContentLoaded", () => {

    const sections = document.querySelectorAll("section[id]");
    const navLinks = document.querySelectorAll(".content-navigation .nav-item");

    const observer = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                navLinks.forEach(link => {

                    link.classList.remove("active");

                    if (link.getAttribute("href") === "#" + entry.target.id) {

                        link.classList.add("active");

                    }

                });

            }

        });

    }, {

        threshold: 0.35

    });

    sections.forEach(section => observer.observe(section));

});