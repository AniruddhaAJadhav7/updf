document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const fileLabel = document.querySelector('.file-input label');

    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            fileLabel.textContent = e.target.files[0].name;
        } else {
            fileLabel.textContent = 'Choose a PDF file';
        }
    });
});