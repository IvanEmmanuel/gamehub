const imageModal = document.getElementById("imageModal");

if (imageModal) {

    const imageViewer = document.getElementById("imageViewer");
    const modalTitle = document.getElementById("imageModalLabel");

    imageModal.addEventListener("show.bs.modal", function (event) {

        const button = event.relatedTarget;

        if (!button) return;

        imageViewer.src = button.dataset.image;
        imageViewer.alt = button.dataset.title;
        modalTitle.textContent = button.dataset.title;

    });

}