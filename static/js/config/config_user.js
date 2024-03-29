// script.js
(function () {
  let dropArea = document.getElementById("drop-area");

  // Previene el comportamiento predeterminado de arrastrar archivos
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  // Resalta el área de drop cuando el archivo está sobre ella
  ["dragenter", "dragover"].forEach((eventName) => {
    dropArea.addEventListener(eventName, highlight, false);
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropArea.addEventListener(eventName, unhighlight, false);
  });

  function highlight(e) {
    dropArea.classList.add("highlight");
  }

  function unhighlight(e) {
    dropArea.classList.remove("highlight");
  }

  // Maneja el archivo soltado
  dropArea.addEventListener("drop", handleDrop, false);

  function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;

    handleFiles(files);
  }

  // Actualiza esta función según cómo quieras procesar los archivos
  function handleFiles(files) {
    [...files].forEach(uploadFile);
  }

  function uploadFile(file) {
    let url = "/upload";
    let formData = new FormData();

    formData.append("file", file);

    axios
      .post(url, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("Success:", response);
        window.location.reload();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  // Permite también hacer clic para seleccionar archivos
  dropArea.addEventListener("click", () => {
    fileElem.click();
  });

  let fileElem = document.getElementById("fileElem");
  fileElem.addEventListener("change", function () {
    let files = this.files;
    handleFiles(files);
  });
})();

window.onload = function() {
  document.getElementById('modifyProfileButton').addEventListener('click', function(event) {
      event.preventDefault();
      
      // obtiene los valores del formulario
      var username = document.getElementById('username').value;
      var email = document.getElementById('email').value;
      var name = document.getElementById('name').value;
      
      // Axios para enviar los datos
      axios.post('/user/update', {
          username: username, // aunque username está deshabilitado, lo incluimos por completitud
          email: email,
          name: name
      })
      .then(function(response) {
          // if status text is OK, then the profile was updated
          if (response.statusText == "OK") {
              alert('Perfil modificado');
              setTimeout(function() {
                  window.location.reload();
              }, 1000);
          } else {
              alert('Error al modificar el perfil');
          }
      })
      .catch(function(error) {
          console.log(error);
          alert('Error al modificar el perfil');
      });
  });
};

// logica de imagen modal
const image = document.getElementById("profile-img");
const overlay = document.getElementById("overlay");
const imageModal = document.getElementsByClassName("profile-img-menu")[0]; // Seleccionado una vez para evitar repetición
const closeImageModal = document.getElementById("close-profile-img-menu");

// Función para mostrar u ocultar el modal de imagen
function toggleImageModal(displayStyle) {
  imageModal.style.display = displayStyle;
  overlay.style.display = displayStyle;
}

// Mostrar el modal al hacer clic en la imagen
image.addEventListener("click", () => toggleImageModal("flex"));

// Ocultar el modal al hacer clic en el botón de cerrar o en el overlay
closeImageModal.addEventListener("click", () => toggleImageModal("none"));
overlay.addEventListener("click", () => toggleImageModal("none"));
