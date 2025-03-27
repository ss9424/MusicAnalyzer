let uploadedFilePath = "";  // Global variable to store file path

document.getElementById("file-selector").addEventListener("click", function() {
    document.getElementById("file-input").click();
});

document.getElementById("file-input").addEventListener("change", function(event) {
    let file = event.target.files[0];
    if (file) uploadFile(file);
});

function uploadFile(file) {
    let formData = new FormData();
    formData.append("file", file);

    fetch("/upload", { method: "POST", body: formData })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert("File uploaded successfully!");
            uploadedFilePath = data.file_path;
        }
    })
    .catch(error => console.error(error));
}

function getAnalysis(type) {
    if (!uploadedFilePath) {
        alert("Please upload a file first!");
        return;
    }

    let formData = new FormData();
    formData.append("file_path", uploadedFilePath);

    fetch(`/analyze/${type}`, { method: "POST", body: formData })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerHTML = `<strong>${type}:</strong> ${data[type]}`;
    })
    .catch(error => console.error(error));
}

// Function to switch tabs
function showTab(tabName) {
    document.querySelectorAll(".tab-content").forEach(tab => {
        tab.style.display = "none";
    });
    document.getElementById(tabName).style.display = "block";
}
