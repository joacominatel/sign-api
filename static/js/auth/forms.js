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

async function loginUser(e) {
  const button = document.getElementById("register");
  
  button.disabled = true;
  button.textContent = "Logging in...";
  button.classList.add("loading");
  
  e.preventDefault();

  // check if in input #username is an email or username
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  let data = {
    username: username,
    password: password,
  };


  try {
    const response = await axios.post("/login", data);
    alert(
      `Logueado con el usuario ${response.data.username}!`
    );
  } catch (error) {
    console.error(error);
  } finally {
    button.textContent = "Login";
    button.disabled = false;
    button.classList.remove("loading");
  }
}
