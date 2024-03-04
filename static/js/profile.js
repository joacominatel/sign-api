async function giveAdmin(username) {
    // are you sure?
    if (!confirm("Are you sure you want to give admin to " + username + "?")) {
        return;
    }

    try {
        // send request to server /profile/username/giveAdmin
        const response = await axios.post('/profile/' + username + '/give_admin');
        // if success
        if (response.status === 200) {
            location.reload();
        }
    }
    catch (error) {
        alert("Error: " + error.response.data);
    }
    
}