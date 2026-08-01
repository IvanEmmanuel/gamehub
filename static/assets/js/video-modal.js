const videoModal = document.getElementById("videoModal");

if (videoModal) {

    const videoPlayer = document.getElementById("videoPlayer");
    const modalTitle = document.getElementById("videoModalLabel");

    videoModal.addEventListener("show.bs.modal", function (event) {

        const button = event.relatedTarget;

        if (!button) return;

        const video = button.dataset.video;
        const title = button.dataset.title;

        if (video) {
            videoPlayer.src = video;
        }

        if (title) {
            modalTitle.textContent = title;
        }

    });

    videoModal.addEventListener("hidden.bs.modal", function () {

        videoPlayer.src = "";

    });

}