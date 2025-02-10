// Select elements
const pdfUrlsInput = document.getElementById('pdf-urls');
const clearUrlsBtn = document.getElementById('clear-urls');
const fileContainer = document.getElementById('file-container');
const addFileBtn = document.getElementById('add-file-btn');
const urlWarning = document.getElementById('url-warning');
const fileWarning = document.getElementById('file-warning');

// Function to reset warnings
function resetWarnings() {
    urlWarning.classList.add('d-none');
    fileWarning.classList.add('d-none');
}

// Function to validate inputs dynamically
function validateInputs() {
    const hasUrls = pdfUrlsInput.value.trim().length > 0;
    const hasFiles = [...fileContainer.querySelectorAll('.file-input')].some(input => input.value);

    toggleFileInputs(!hasUrls); // Disable file inputs if URLs exist
    toggleUrlInput(!hasFiles); // Disable URL input if files exist

    urlWarning.classList.toggle('d-none', !hasFiles || !hasUrls);
    fileWarning.classList.toggle('d-none', !hasFiles || !hasUrls);
}

// Function to toggle file inputs
function toggleFileInputs(enable) {
    const fileInputs = fileContainer.querySelectorAll('.file-input');
    fileInputs.forEach(input => {
        input.disabled = !enable;
    });
    addFileBtn.disabled = !enable; // Disable add button if file inputs are disabled
}

// Function to toggle URL input
function toggleUrlInput(enable) {
    pdfUrlsInput.disabled = !enable;
    clearUrlsBtn.disabled = !enable;
}

// Add file input dynamically
addFileBtn.addEventListener('click', () => {
    const fileInputGroup = document.createElement('div');
    fileInputGroup.classList.add('file-input-group');

    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.classList.add('file-input', 'form-control');

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.classList.add('btn', 'btn-danger', 'remove-file-btn');
    removeBtn.textContent = 'Remove';

    fileInputGroup.appendChild(fileInput);
    fileInputGroup.appendChild(removeBtn);

    fileContainer.appendChild(fileInputGroup);

    validateInputs(); // Revalidate after adding file
});

// Clear URLs
clearUrlsBtn.addEventListener('click', () => {
    pdfUrlsInput.value = '';
    resetWarnings(); // Clear warnings when URLs are cleared
    validateInputs(); // Revalidate inputs
});

// Remove file input dynamically
fileContainer.addEventListener('click', (event) => {
    if (event.target.classList.contains('remove-file-btn')) {
        event.target.closest('.file-input-group').remove();
        resetWarnings(); // Clear warnings when files are removed
        validateInputs(); // Revalidate inputs
    }
});

// Input event listeners for validation
pdfUrlsInput.addEventListener('input', validateInputs);
fileContainer.addEventListener('change', validateInputs);

// Reset warnings initially
resetWarnings();
