# Tarea: Base de Datos en FastAPI con MediaPipe

## Datos del alumno:
- Nombre: Marcos Andrés Simon Ágreda
- Código: 56728

## Descripción:

La presente tarea, contiene tres métodos HTML para acceso a la base de datos, basada en SQLite; los cuales son:
- GET "/esqueletocompleto": Devuelva todos los esqueletos almacenados en la base de datos
- GET "/esqueletocompleto/{id}": Devuelva el esqueleto con el id indicado
- DELETE "/esqueletocompleto/{id}": Elimina el esqueleto con el id indicado
- POST "/esqueleto": Crea un nuevo esqueleto en la base de datos

Los requisitos se encuentran en el archivo requirements.txt; son los mismos que se vieron en clase, a excepción de la inclusión del ORM "SQLAlchemy" para facilitar la creación de la base de datos. Además, se necesita tener instalado "SQLite" para poder crear la base de datos.

Las fotos para realizar las pruebas se encuentran en la carpeta "test_pictures".

De la misma manera que se vio en clase, se puede ejecutar el programa con el comando "uvicorn selfie_server:app --port 8000" en la terminal.