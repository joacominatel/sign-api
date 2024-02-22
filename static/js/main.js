let changeThemeButton = document.getElementById('change-theme');

changeThemeButton.addEventListener('click', function( event ) {
    let body = document.getElementsByTagName('body')[0];
    body.classList.toggle('dark');
    
    let theme = body.classList.contains('dark') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
});

let logoutButton = document.getElementById('logout');

logoutButton.addEventListener('click', function () {
    window.location.href = '/logout';
});

function updateTaskCompletion(task) {
    const taskId = task.getAttribute('data-id');
    const completed = task.checked;

    axios.post('/complete_task', {
        taskId: taskId,
        completed: completed
    })
    .then(function (response) {
        console.log('Task updated');
    })
    .catch(function (error) {
        console.log(error);
    });
}

function deleteTask(task) {
    const taskId = task.getAttribute('data-id');

    // are you sure taskparentelement.remove
    const confirmation = confirm('Are you sure you want to delete this task?');
    if (!confirmation) {
        return;
    }

    axios.post('/delete_task', {
        taskId: taskId
    })
    .then(function (response) {
        console.log('Task deleted');
        task.parentElement.parentElement.parentElement.remove();
    })
    .catch(function (error) {
        console.log(error);
    });
}

function createTask() {
    // open modal for creating a task
    const modal = document.getElementById('createTaskModal');
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('createTaskModal');
    modal.style.display = 'none';
}

function createTaskForm( event ) {
    event.preventDefault();

    const title = document.getElementById('task-name').value;
    const description = document.getElementById('task-description').value;
    const dueDate = document.getElementById('task-date').value;

    axios.post('/add_task', {
        title: title,
        description: description,
        dueDate: dueDate
    })
    .then(function (response) {
        console.log('Task created');
        closeModal();
        window.location.reload();
    })
    .catch(function (error) {
        console.log(error);
    });
}