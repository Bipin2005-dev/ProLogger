// document.addEventListener("DOMContentLoaded", () => {
//     document.getElementById("form-upload").addEventListener('submit', (event) => {
//         event.preventDefault();
//         const formData = new FormData();
//         formData.append("raw-log", document.getElementById("file-upload").files[0]);

//         fetch('http://127.0.0.1:5000/fileProcess', {
//             method: "POST",
//             body: formData
//         })
//         .then(response => response.json())
//         .then(data => console.log(data))
//         .catch(error => console.error('Error:', error));
//     });
// });

