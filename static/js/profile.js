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

async function blockUser(username) {
    // are you sure?
    if (!confirm("Are you sure you want to block " + username + "?")) {
        return;
    }

    try {
        // send request to server /profile/username/block
        const response = await axios.post('/profile/' + username + '/block');
        // if success
        if (response.status === 200) {
            location.reload();
        }
    }
    catch (error) {
        alert("Error: " + error.response.data);
    }
}

async function unblockUser(username) {
    // are you sure?
    if (!confirm("Are you sure you want to unblock " + username + "?")) {
        return;
    }

    try {
        // send request to server /profile/username/unblock
        const response = await axios.post('/profile/' + username + '/unblock');
        // if success
        if (response.status === 200) {
            location.reload();
        }
    }
    catch (error) {
        alert("Error: " + error.response.data);
    }
}

async function removeAdmin(username) {
    // are you sure?
    if (!confirm("Are you sure you want to remove admin from " + username + "?")) {
        return;
    }

    try {
        // send request to server /profile/username/removeAdmin
        const response = await axios.post('/profile/' + username + '/remove_admin');
        // if success
        if (response.status === 200) {
            location.reload();
        }
    }
    catch (error) {
        alert("Error: " + error.response.data);
    }
}