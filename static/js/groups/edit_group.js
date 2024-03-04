const formEditGroup = document.getElementById('edit-group-form');

formEditGroup.addEventListener('submit', async (e) => {
    e.preventDefault();

    const button = document.getElementById('edit-group-submit');

    // get group id from url
    const url = window.location.href;
    const urlArray = url.split('/');
    const groupId = urlArray[urlArray.length - 2];

    const groupName = document.getElementById('group-name').value;
    const groupDescription = document.getElementById('group-description').value;

    // button config
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';

    try { 
        const response = axios.post(`/groups/${groupId}/edit_group`, {
            groupName,
            groupDescription
            });

            alert('Group updated successfully');
    } catch (error) {
        console.error(error);
    } finally {
        button.disabled = false;
        button.innerHTML = 'Save';
    }
});