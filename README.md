**TaskApp**

En esta aplicacion decidi poner en practica ciertos lenguajes y frameworks.
En este caso utilice Python con su framework de Flask, y PostgreSQL principalmente.

El proyecto se trataba de una simple "to-do list" pero completo. Es decir, sistema de usuarios, roles, administradores, grupos para compartir tareas, de esa forma practicaba la relacion entre los datos y las tablas.

*Como usar?*

📌 Primero se deben descargar las dependencias del `requirements.txt` con el comando:

*Windows:* `pip install -r ./requirements.txt`

*Linux/Mac*: `pip3 install -r ./requirements.txt`
En el caso de Mac/Linux, o al usar `pip3`, se debe instalar la libreria `psycopg2-binary`.

📌 Se debe crear un archivo `.env` en la raiz del proyecto. Este es el encargado de guardar ciertos datos "privados/vulnerables". Debe quedar algo asi:

.env:
```
SECRET_KEY='secretKey_of_flask'

SQLALCHEMY_DATABASE_URI='postgresql://USERNAME:PASSWORD@localhost/taskapp'

UPLOAD_FOLDER = 'static/img/uploads'
```

En esta version se utiliza SQLAlchemy para ordenar las tablas y automatizar algunos procesos. Por ejemplo,
la creacion de estas y la generacion de los dos roles principales (user, admin).

Esta en la carpeta /sql donde podemos encontrar el archivo db.py que establece la conexion. Y dentro de /sql/models 
estan todos los modelos de cada tabla, de esta forma se mantiene otro orden y se asegura que no haya errores al crear
la base de datos.

📌 Ejecutar el `app.py` estando dentro del entorno virtual.