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

                    // if user[1] is not null, then it means that the user have image
                    if (user[1] != null) {
                        userDiv.innerHTML = '<img src="/static/img/uploads/' + user[1] + '" width="50" height="50" style="border-radius: 50%;">' + user[0];
                    } else {
                        userDiv.innerHTML = '<img src="/static/img/default-user.webp" width="50" height="50" style="border-radius: 50%;">' + user[0];
                    }
                    
                    userDiv.onclick = function() {
                        addMemberToGroup(user[0]);
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
        }
    )
    .catch(function (error) {
        console.log(error);
    });
}