(() => {
    const uploadBtn = document.querySelector('.js-upload');
    const backBtn = document.querySelector('.js-back');
    const uploadContainer = document.querySelector('.upload-container');
    const videoContainer = document.querySelector('.video-container');
    const errorContainer = document.querySelector('.error-container');
    const resultContainer = document.querySelector('.js-video-text');
    const videoPreview = document.querySelector('#video');
    const spinner = document.querySelector('.js-spinner-container');
    const errorText = document.querySelector('.error-message');

    uploadBtn.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();

        spinner.classList.remove('d-none');
        uploadContainer.classList.add('d-none');

        const fileInput = document.querySelector('.form-control-file[name="video"]');
        const file = fileInput.files[0];

        const formData = new FormData();
        formData.append('video', file);

        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        })
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((json) => Promise.reject(json));
                }

                return response.json();
            })
            .then((json) => {
                spinner.classList.add('d-none');
                videoContainer.classList.remove('d-none');
                backBtn.classList.remove('d-none');

                videoPreview.src = URL.createObjectURL(file);

                resultContainer.textContent = json;
            })
            .catch((message) => {
                spinner.classList.add('d-none');
                backBtn.classList.remove('d-none');
                errorContainer.classList.remove('d-none');

                errorText.textContent = message;
            });
    });

    backBtn.addEventListener('click', () => {
        uploadContainer.classList.remove('d-none');
        videoContainer.classList.add('d-none');
        errorContainer.classList.add('d-none');

        backBtn.classList.add('d-none');
    })
})();