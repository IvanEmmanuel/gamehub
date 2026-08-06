document.addEventListener("DOMContentLoaded", () => {

    /**
     * Muestra la vista previa de una imagen
     */
    function showPreview(file, uploadArea, preview, clearInput){

        if(!file){
            return;
        }

        if (clearInput) {
            clearInput.value = "0";
        }

        if(!file.type.startsWith("image/")){
            return;
        }

        const objectURL = URL.createObjectURL(file);

        preview.src = objectURL;

        uploadArea.classList.add("has-image");

        preview.onload = () => {

            URL.revokeObjectURL(objectURL);

        };

    }

    /**
     * Inicializa todas las zonas de carga
     */
    document.querySelectorAll(".upload-area").forEach(uploadArea => {

        const input = uploadArea.querySelector('input[type="file"]');
        const preview = uploadArea.querySelector(".image-preview");
        const removeButton = uploadArea.querySelector(".remove-image");
        const clearInput = uploadArea.querySelector(".clear-image-input");

        if(!input || !preview){
            return;
        }

        /*==========================
            Click (Seleccionar)
        ==========================*/

        input.addEventListener("change", function(){

            const file = this.files[0];

            showPreview(file, uploadArea, preview);

        });

        /*==========================
            Drag Enter
        ==========================*/

        uploadArea.addEventListener("dragenter", e => {

            e.preventDefault();

            uploadArea.classList.add("dragover");

        });

        /*==========================
            Drag Over
        ==========================*/

        uploadArea.addEventListener("dragover", e => {

            e.preventDefault();

        });

        /*==========================
            Drag Leave
        ==========================*/

        uploadArea.addEventListener("dragleave", () => {

            uploadArea.classList.remove("dragover");

        });

        /*==========================
            Drop
        ==========================*/

        uploadArea.addEventListener("drop", e => {

            e.preventDefault();

            uploadArea.classList.remove("dragover");

            const files = e.dataTransfer.files;

            if(!files.length){
                return;
            }

            input.files = files;

            showPreview(files[0], uploadArea, preview);

        });

        /*==========================
            Remove Image
        ==========================*/

        if(removeButton){

            removeButton.addEventListener("click", function(e){

                e.preventDefault();

                e.stopPropagation();

                input.value = "";

                preview.removeAttribute("src");

                uploadArea.classList.remove("has-image");

                if (clearInput) {
                    clearInput.value = "1";
                }

            });

        }

    });

});