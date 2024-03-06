let changeThemeButton = document.getElementById("change-theme");

changeThemeButton.addEventListener("click", function (event) {
  let body = document.getElementsByTagName("body")[0];
  body.classList.toggle("dark");

  let theme = body.classList.contains("dark") ? "dark" : "light";
  localStorage.setItem("theme", theme);
});

let logoutButton = document.getElementById("logout");

logoutButton.addEventListener("click", function () {
  window.location.href = "/logout";
});

function updateTaskCompletion(task, taskId) {
  const completed = task.checked;

  axios
    .post("/complete_task", {
      taskId: taskId,
      completed: completed,
    })
    .then(function (response) {
      console.log("Task updated");
    })
    .catch(function (error) {
      console.log(error);
    });
}

function deleteTask(task) {
  const taskId = task.getAttribute("data-id");

  // are you sure taskparentelement.remove
  const confirmation = confirm("Are you sure you want to delete this task?");
  if (!confirmation) {
    return;
  }

  axios
    .post("/delete_task", {
      taskId: taskId,
    })
    .then(function (response) {
      console.log("Task deleted");
      task.parentElement.parentElement.parentElement.remove();
    })
    .catch(function (error) {
      console.log(error);
    });
}

function createTask() {
  // open modal for creating a task
  const modal = document.getElementById("createTaskModal");
  modal.style.display = "block";
}

function closeModal() {
  const modal = document.getElementById("createTaskModal");
  modal.style.display = "none";
}

function createTaskForm(event) {
  event.preventDefault();

  const title = document.getElementById("task-name").value;
  const description = document.getElementById("task-description").value;
  const dueDate = document.getElementById("task-date").value;
  const priority = document.getElementById("task-priority").value;

  axios
    .post("/add_task", {
      title: title,
      description: description,
      dueDate: dueDate,
      priority: priority,
    })
    .then(function (response) {
      console.log("Task created");
      closeModal();
      window.location.reload();
    })
    .catch(function (error) {
      console.log(error);
    });
}

function redirectTasks() {
  window.location.href = "/tasks";
}

function showCompletedTasks() {
  const completedTasks = document.querySelectorAll(".completed");

  // toggle class completed-filter
  completedTasks.forEach((task) => {
    task.classList.toggle("completed-filter");
  });
}

let lastScrollTop = 0;
const navbar = document.getElementById("navbar");

window.addEventListener("scroll", function() {
  let scrollTop = window.scrollY || document.documentElement.scrollTop;
  if (scrollTop > lastScrollTop) {
      // Scroll hacia abajo
      navbar.style.top = "-100px"; // Ocultar el navbar
  } else {
      // Scroll hacia arriba
      navbar.style.top = "0"; // Mostrar el navbar
  }
  lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

function showNotifications() {
  const notifications = document.getElementById("notification-list");
  notifications.classList.toggle("show");
} 

function readNotification(notificationId) {
  axios
    .post("/read_notification", {
      notificationId: notificationId,
    })
    .then(function (response) {
      console.log("Notification read");
      // remove notification from list
      const notification = document.getElementById(`notification-${notificationId}`);
      notification.remove();

      // check if there are no more notifications
      const notifications = document.getElementById("notification-list"); // div
      // get ul inside div
      const ul = notifications.querySelector("ul");
      if (ul.children.length === 0) {
        const noNotifications = document.createElement("li");
        // create <a>
        const a = document.createElement("a");
        a.href = "#";
        // create <p>
        const p = document.createElement("p");
        p.textContent = "No notifications";
        a.appendChild(p);
        noNotifications.appendChild(a);
        ul.appendChild(noNotifications);
      }

      // update notifications count
      const notificationsCount = document.getElementById("notification-count");
      notificationsCount.textContent = ul.children.length;
      
    })
    .catch(function (error) {
      console.log(error);
    });

}