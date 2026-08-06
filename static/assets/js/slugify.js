document.addEventListener("DOMContentLoaded", () => {

    const nameInput = document.getElementById("id_name");
    const slugInput = document.getElementById("id_slug");

    if (!nameInput || !slugInput) {
        return;
    }

    nameInput.addEventListener("input", () => {

        let slug = nameInput.value
            .toLowerCase()
            .trim()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .replace(/[^a-z0-9\s-]/g, "")
            .replace(/\s+/g, "-")
            .replace(/-+/g, "-");

        slugInput.value = slug;

    });

});