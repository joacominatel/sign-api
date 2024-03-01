function registerUser(e) {
  e.preventDefault();

  let username = document.getElementById("username").value;
  let name = document.getElementById("name").value;
  let password = document.getElementById("password").value;
  let confirmPassword = document.getElementById("confirmPassword").value;
  let email = document.getElementById("email").value;

  if (password !== confirmPassword) {
    alert("Passwords do not match");
    return;
  }

  let data = {
    username: username,
    password: password,
    name: name,
    email: email,
  };

  // post data to server
  axios
    .post("/register", data)
    .then((res) => {
      alert("User registered");
      window.location.href = "/";
    })
    .catch((err) => {
      console.log(err);
      alert("Error registering user");
    });
}

function loginUser(e) {
  e.preventDefault();

  // check if in input #username is an email or username
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  let data = {
    username: username,
    password: password,
  };

  // post data to server
  axios
    .post("/login", data)
    .then((res) => {
      const response = res.data;
      if (response.status === "error") {
        alert(response.message);
        return;
      } else {
        alert("User logged in");
        setTimeout(() => {
          window.location.href = "/";
        }, 1000);
      }
    })
    .catch((err) => {
      console.log(err);
      alert("Error logging in user");
    });
}
