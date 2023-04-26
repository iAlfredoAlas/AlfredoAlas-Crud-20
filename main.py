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