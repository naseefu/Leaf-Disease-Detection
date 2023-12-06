function showResultSection() {
  
  const fileInput = document.getElementById('file-input');

  
  if (fileInput.files.length > 0) {
    
    document.getElementById('result-section').style.display = 'block';

    document.getElementById('intro-section').style.display = 'none';

    
    const uploadedImage = document.getElementById('uploaded-image');
    uploadedImage.src = URL.createObjectURL(fileInput.files[0]);

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/predict', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {

        document.getElementById('result').textContent = data.result;
      })
      .catch(error => {
        console.error('Error:', error);
      });
  } else {
    alert('Please choose a file.');
  }
}
