#Importar librerias a utilizar.
import mysql.connector
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

#Modelo de tabla Student
class Student(BaseModel):
    idStudent: int
    name: str
    lastName: str
    email: str
    dateCreation: str
    phone: str
    status: str

#Guardar la conexión a la base de datos en una variable
mySqlConex = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="exercisecrud20%"
)

#Esta es una instancia de FastAPI, la cual levanta la api en local 
app = FastAPI()

#Recomiendo siempre dejar un endpoint para la ruta "/" dado que será el primer endpoind en visualizar
@app.get("/")
async def root():
    return {"message": "Hello World"}

#Endpoint GET todos los usuarios (PUNTO 7)
@app.get("/student")
def getStudent():

#Crear un cursor para ejecutar consultas SQL
    cursor = mySqlConex.cursor()

    #Ejecutar una consulta SQL para seleccionar todos los usuarios
    query = "SELECT * FROM student"
    cursor.execute(query)

    #Obtener los resultados de la consulta
    resultados = cursor.fetchall()

    #Cerrar el cursor y la conexión a la base de datos
    cursor.close()

 #Convertir los objetos datetime.date en cadenas de texto, esto se hace ya que en caso de
    #no hacer esta conversión obtendremos una excepción del siguiente tipo
    #TypeError: Object of type date is not JSON serializable
    student = [
        {
            "idStudent": student[0],
            "name": student[1],
            "lastName": student[2],
            "email": student[3],
            "dateCreation": str(student[4]),
            "phone": student[5],
            "status": student[6]
        }
        for student in resultados
    ]

    #Devolver los usuarios como una respuesta JSON
    return JSONResponse(content=student)

#Endpoint GET un usuario por id (PUNTO 10)
@app.get("/student/{idStudent}")
def getStudentById(idStudent: int):

    #Crear un cursor para ejecutar consultas SQL
    cursor = mySqlConex.cursor()

    #Ejecutar una consulta SQL para seleccionar el usuario con el id especificado
    query = "SELECT * FROM student WHERE idStudent = %s"
    cursor.execute(query, (idStudent,))

    #Obtener el resultado de la consulta
    resultado = cursor.fetchone()

    #Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    if resultado is None:
        #Si no se encontró ningún estudiante con el id especificado, devolver un error 404
        return JSONResponse(status_code=404, content={"mensaje": "Estudiante no encontrado"})
    else:
        #Si se encontró el usuario, devolver la información como una respuesta JSON
        student = {
            "idStudent": resultado[0],
            "name": resultado[1],
            "lastName": resultado[2],
            "email": resultado[3],
            "dateCreation": str(resultado[4]),
            "phone": resultado[5],
            "status": resultado[6]
        }
        return JSONResponse(content = student)
    
#Endpoint para editar Estudiantes
@app.put("/student/{idStudent}")
def updateStudent(idStudent: int, student: Student):
    
    try:
      #Crear un cursor para ejecutar consultas SQL
      cursor = mySqlConex.cursor()

      #Extraer los datos del objeto Estudiante
      nameStudent = student.name
      lastNameStudent = student.lastName
      email = student.email
      dateCreation = student.dateCreation
      phone = student.phone
      status = student.status

      # Ejecutar una consulta SQL para actualizar la información del usuario
      query = "UPDATE Student SET name=%s, lastName=%s, email=%s, dateCreation=%s, phone=%s, status=%s WHERE idStudent=%s"
      values = (nameStudent, lastNameStudent, email, dateCreation, phone, status, idStudent)
      cursor.execute(query, values)
     
      # Guardar los cambios en la base de datos
      mySqlConex.commit()

      # Cerrar el cursor y la conexión a la base de datos
      cursor.close()

    # Devolver una respuesta JSON indicando que el usuario ha sido actualizado
      return JSONResponse(content={"mensaje": f"El estudiante con id {idStudent} ha sido actualizado"})
    except:
      return JSONResponse(status_code=404, content={"error": f"El estudiante no pudo ser actualizado"})
    
#Endpoint para agregar estudiante
@app.post("/student")
def addStudent(student: Student):
    try:
      #Crear un cursor para ejecutar consultas SQL
      cursor = mySqlConex.cursor()

      #Extraer los datos del objeto Estudiante
      idStudent = student.idStudent
      nameStudent = student.name
      lastNameStudent = student.lastName
      email = student.email
      dateCreation = student.dateCreation
      phone = student.phone
      status = student.status

      #Ejecutar el query para agregar estudiantes a la tabla Student
      query = "INSERT INTO student (name, lastName, email, dateCreation, phone, status) VALUES (%s, %s, %s, %s, %s, %s)"
      values = (nameStudent, lastNameStudent, email, dateCreation, phone, status)
      cursor.execute(query, values)

      # Guardar los cambios en la base de datos
      mySqlConex.commit()

      # Cerrar el cursor y la conexión a la base de datos
      cursor.close()

      # Devolver una respuesta JSON indicando que el usuario ha sido actualizado
      return JSONResponse(content={"mensaje": f"El estudiante con id {idStudent} ha sido actualizado"})
    except:
      return JSONResponse(status_code=404, content={"error": f"El estudiante no pudo ser actualizado"})
    
#Endpoint para eliminar estudiante de forma lógica
@app.delete("/student/{idStudent}")
def deleteStudent(idStudent: int):
   try:
      # Crear un cursor para ejecutar consultas SQL
      cursor = mySqlConex.cursor()

      #Extraer los datos del objeto Estudiante
      status = idStudent.status

      # Ejecutar una consulta SQL para eliminar el usuario con el id especificado
      query = "UPDATE Student SET status = %s WHERE idStudent=%s"
      values = (status)
      cursor.execute(query, values)

      # Guardar los cambios en la base de datos
      mySqlConex.commit()

      # Cerrar el cursor y la conexión a la base de datos
      cursor.close()

      # Devolver una respuesta JSON indicando que el usuario ha sido eliminado
      return JSONResponse(content={"mensaje": f"El Estudiante con id {idStudent} ha sido eliminado"})
   except:
      return JSONResponse(status_code=400, content={"Error": f"El estudiante con el id {idStudent} no pudo ser eliminado"})