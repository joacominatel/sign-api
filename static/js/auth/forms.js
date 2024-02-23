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
        toastr.error(response.message); // Muestra mensaje de error
        return;
      } else {
        toastr.success("User logged in"); // Muestra mensaje de éxito
        window.location.href = "/"; // Redirect on successful login
      }
    })
    .catch((err) => {
      console.log(err);
      toastr.error("Error logging in"); // Muestra mensaje de error
    });
}
