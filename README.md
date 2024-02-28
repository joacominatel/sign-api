**TaskApp**

En esta aplicacion decidi poner en practica ciertos lenguajes y frameworks.
En este caso utilice Python con su framework de Flask, y PostgreSQL principalmente.

El proyecto se trataba de una simple "to-do list" pero completo. Es decir, sistema de usuarios, roles, administradores, grupos para compartir tareas, de esa forma practicaba la relacion entre los datos y las tablas.

*Como usar?*

📌 Primero se deben descargar las dependencias del `requirements.txt` con el comando:

*Windows:* `pip install -r ./requirements.txt`

*Linux/Mac*: `pip3 install -r ./requirements.txt`

📌 Se debe crear un archivo `.env` en la raiz del proyecto. Este es el encargado de guardar ciertos datos "privados/vulnerables". Debe quedar algo asi:

.env:
```
DB_NAME='taskapp'
DB_USER='x'
DB_PASS='x'
DB_HOST='localhost'
DB_PORT='5432'

SECRET_KEY='secretKey_of_flask'

UPLOAD_FOLDER = 'static/img/uploads'
```

📌 Ahora queda crear las tablas SQL. Estas estan guardadas en el archivo  `./tables.sql`.

📌 Una vez creadas ya se puede iniciar la aplicacion el archivo `app.py`

