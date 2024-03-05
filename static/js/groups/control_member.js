// Obtén el modal
var modal = document.getElementById('addMemberModal');

// Obtén el botón que abre el modal
var btn = document.getElementById("add-member-btn");

// Obtén el elemento <span> que cierra el modal
var span = document.getElementById("closeMemberModal");

// Cuando el usuario haga clic en el botón, abre el modal 
btn.onclick = function() {
    modal.style.display = "block";
}

// obtener GROUP ID
var currentPath = window.location.pathname;

// divide la ruta
var pathSegments = currentPath.split('/');
var GROUP_ID = pathSegments[pathSegments.length - 1];

GROUP_ID = parseInt(GROUP_ID);

// Cuando el usuario haga clic en <span> (x), cierra el modal
span.onclick = function() {
    modal.style.display = "none";
}

// Cuando el usuario haga clic en cualquier lugar fuera del modal, ciérralo
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Evento para buscar usuarios
document.getElementById('userSearchInput').addEventListener('input', function(e) {
    axios.get('/search_users', { params: { username: e.target.value, group_id: GROUP_ID } })
         .then(function (response) {
                var users = response.data;
                var usersList = document.getElementById('userSearchResults');
                
                console.log(users);

                usersList.innerHTML = '';
                users.forEach(function(user) {
                    var userDiv = document.createElement('div');
                    userDiv.className = 'user-search-result';

                    console.log(user.username);

                    // if user[1] is not null, then it means that the user have image
                    if (user.profile_image_url != null) {
                        userDiv.innerHTML = '<img src="/static/img/uploads/' + user.profile_image_url + '" width="50" height="50" style="border-radius: 50%;">' + user.username;
                    } else {
                        userDiv.innerHTML = '<img src="/static/img/default-user.webp" width="50" height="50" style="border-radius: 50%;">' + user.username;
                    }
                    
                    userDiv.onclick = function() {
                        addMemberToGroup(user.username);
                    }
                    usersList.appendChild(userDiv);
                });
        })
         .catch(function (error) {
             console.log(error);
         });
});

// Función para agregar miembro al grupo
function addMemberToGroup(username) {
    axios.post('/groups/' + GROUP_ID + '/add_member', { username: username })
        .then(function (response) {
            console.log(response);
            modal.style.display = "none";
            window.location.reload();
        }
    )
    .catch(function (error) {
        console.log(error);
    });
}


const btnOpenModalTask = document.getElementById('add-task-btn');
const modalTask = document.getElementById('addTaskModal');
const closeModalTask = document.getElementById('closeTaskModal');

btnOpenModalTask.onclick = function() {
    modalTask.style.display = "block";
}

closeModalTask.onclick = function() {
    modalTask.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modalTask) {
        modalTask.style.display = "none";
    }
}

function addTaskToGroup(taskId) {
    axios.post('/groups/' + GROUP_ID + '/add_task', { taskId: taskId })
        .then(function (response) {
            console.log(response);
            modalTask.style.display = "none";
            window.location.reload();
        }
    )
}

function deleteMemberFromGroup(userId) {
    if (!confirm('Estas seguro que quieres eliminar al miembro del grupo?')) {
        return;
    }

    axios.post('/groups/' + GROUP_ID + '/delete_member', { userId: userId })
        .then(function (response) {
            alert(response.data.message);
            window.location.reload();
        })
        .catch(function (error) {
            alert(error.response.data.message);
        });
}

const formGroupPosts = document.getElementById('create-post-form');

formGroupPosts.addEventListener('submit', function(e) {
    e.preventDefault();
    axios.post('/groups/' + GROUP_ID + '/posts', {
        title: document.getElementById('post-title').value,
        content: document.getElementById('post-content').value
        })
        .then(function (response) {
            console.log(response);
            window.location.reload();
        })
        .catch(function (error) {
            console.log(error);
        });
})

function upVotePost(postId) {
    axios.post('/groups/posts/' + postId + '/upvote')
        .then(function (response) {
            console.log(response);
            window.location.reload();
        })
        .catch(function (error) {
            console.log(error);
        });
}

function leaveGroup(group_id) {
    if (!confirm('Estas seguro que quieres abandonar el grupo?')) {
        return;
    }

    axios.post('/groups/' + group_id + '/leave')
        .then(function (response) {
            alert(response.data.message);
            window.location.href = '/groups';
        })
        .catch(function (error) {
            alert(error.response.data.message);
        });
}

function deleteGroup(group_id) {
    if (!confirm('Estas seguro que quieres eliminar el grupo?')) {
        console.log(group_id);
        return;
    }

    axios.post('/groups/' + group_id + '/delete')
        .then(function (response) {
            alert(response.data.message);
            window.location.href = '/groups';
        })
        .catch(function (error) {
            alert(error.response.data.message);
        });
}

async function removeTaskFromGroup(taskId) {
    if (!confirm('Estas seguro que quieres eliminar la tarea?')) {
        return;
    }

    try {
        const response = await axios.post('/groups/' + GROUP_ID + '/delete_task', { taskId: taskId });
        alert(response.data.message);
        window.location.reload();
    } catch (error) {
        alert(error.response.data.message);
    }
}