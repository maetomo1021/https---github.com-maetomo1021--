document.getElementById('file-upload').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const uploadedImage = document.getElementById('uploaded-image');
            uploadedImage.src = e.target.result;
            uploadedImage.style.display = 'block';
            
            // Trigger OCR processing function (send the image to Flask backend)
            processOCR(file);
        };
        reader.readAsDataURL(file);
    }
});

function processOCR(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    // Send image to Flask backend for OCR processing
    fetch('/process_ocr', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('extracted-text').textContent = data.text;
    })
    .catch(error => {
        console.error('Error during OCR processing:', error);
    });
}
