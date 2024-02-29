document.getElementById('userSearchInput').addEventListener('input', function(e) {
    axios.get('/search_users', { params: { username: e.target.value } })
         .then(function (response) {
                var users = response.data;
                var usersList = document.getElementById('userSearchResults');

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

// when click on user search result, location.href to /profile/username
document.getElementById('userSearchResults').addEventListener('click', function(e) {
    if (e.target.className === 'user-search-result') {
        var username = e.target.textContent;
        location.href = '/profile/' + username;
    }
});