async function registerUser(e) {
  e.preventDefault();

  const button = document.getElementById("register");

  button.disabled = true;
  button.textContent = "Registering...";
  button.classList.add("loading");

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

  try {
    const response = await axios.post("/register", data);
    alert(
      `Usuario ${response.data.username} registrado con éxito!`
    );
    window.location.href = "/";
  }
  catch (error) {
    console.error(error);
  }
  finally {
    button.textContent = "Register";
    button.disabled = false;
    button.classList.remove("loading");
  }
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
    window.location.href = "/";
  } catch (error) {
    alert("Error: " + error.response.data.message);
  } finally {
    button.textContent = "Login";
    button.disabled = false;
    button.classList.remove("loading");
  }
}
