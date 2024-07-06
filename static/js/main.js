document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('convertForm');
    const loadingDiv = document.getElementById('loading');
    const convertBtn = document.getElementById('convertBtn');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        loadingDiv.classList.remove('hidden');
        convertBtn.disabled = true;

        const formData = new FormData(form);
        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = formData.get('file').name.replace('.pdf', '.epub');
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            } else {
                throw new Error('Conversion failed');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during conversion. Please try again.');
        } finally {
            loadingDiv.classList.add('hidden');
            convertBtn.disabled = false;
        }
    });
});
