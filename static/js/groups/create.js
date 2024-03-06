async function createGroup() {
    const name = document.getElementById('groupName').value;
    const description = document.getElementById('groupDescription').value;
    
    const button = document.getElementById('createGroupButton');
    button.disabled = true;
    button.textContent = 'Creando grupo...';
    button.classList.add('loading');
    
    try {
        const response = await axios.post('/groups/create', {
            name,
            description
        });
        alert(
            `Grupo ${response.data.group_name} creado correctamente con id ${response.data.group_id}!`
        );
        window.location.href = `/groups/${response.data.group_id}`;
    } catch (error) {
        console.error(error);
    } finally {
        button.disabled = false;
        button.textContent = 'Crear grupo';
        button.classList.remove('loading');
    }
}