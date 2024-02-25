function createGroup() {
    const name = document.getElementById('groupName').value;
    const description = document.getElementById('groupDescription').value;
    
    axios.post('/groups/create', {
        name: name,
        description: description
    })
    .then(function (response) {
        console.log(response);
        alert("Grupo creado exitosamente!");
    })
    .catch(function (error) {
        console.log(error);
        alert("Hubo un error al crear el grupo.");
    });
}