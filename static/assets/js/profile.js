const avatarInput = document.getElementById('id_avatar');
const avatarButton = document.getElementById('avatar-edit-button');
const avatarPreview = document.getElementById('avatar-preview');

avatarButton.addEventListener('click', () => {
    avatarInput.click();
});

avatarInput.addEventListener('change', () => {

    const file = avatarInput.files[0];

    if (file) {
        avatarPreview.src = URL.createObjectURL(file);
    }

});

const bannerInput = document.getElementById('id_banner');
const bannerButton = document.getElementById('banner-edit-button');
const bannerPreview = document.getElementById('banner-preview');

bannerButton.addEventListener('click', () => {
    bannerInput.click();
});

bannerInput.addEventListener('change', () => {

    const file = bannerInput.files[0];

    if (file) {
        bannerPreview.src = URL.createObjectURL(file);
    }

});