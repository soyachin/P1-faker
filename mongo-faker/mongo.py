import sys

from pymongo import MongoClient
from faker import Faker
from random import choice, randint
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field

fake = Faker()

class SeguroModel(BaseModel):
    tipo_seguro: str
    vencimiento: datetime

class PacienteModel(BaseModel):
    dni: str = Field(..., alias="_id")
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    seguro: Optional[SeguroModel] = None

    class Config:
        populate_by_name = True

def generar_dni() -> str:
    return str(randint(10000000, 99999999))

import os

host = os.getenv('HOST')  # Usa 'localhost' como valor por defecto
port = int(os.getenv('PORT', 27017))    # Usa 27017 como valor por defecto

try:
    client = MongoClient(f'mongodb://{host}:{port}/')
    client.server_info()  # Intentar obtener información del servidor
    print("Conectado a MongoDB!")
except Exception as e:
    print("Error al conectar a MongoDB:", e)
    sys.exit(1)


db = client.P1pacientes_test
collection = db.Pacientes
seguros = ["Salud", "Vida", "Dental"]

data = []

for _ in range(50):

    tiene_seguro = choice([True, False])
    fecha_nacimiento = fake.date_of_birth(maximum_age=99)
    paciente = PacienteModel(
        dni=generar_dni(),
        nombres=fake.first_name(),
        apellidos=fake.last_name(),
        fecha_nacimiento=fecha_nacimiento
    )

    if tiene_seguro:
        tipo_seguro = choice(seguros)
        vencimiento = fake.date_between(start_date='today', end_date='+2y')
        paciente.seguro = SeguroModel(tipo_seguro= tipo_seguro, vencimiento = vencimiento)

    paciente_dict = paciente.dict(by_alias=True)
    paciente_dict['fecha_nacimiento'] = datetime.combine(paciente_dict['fecha_nacimiento'], datetime.min.time())
    data.append(paciente_dict)


result = collection.insert_many(data)

print(f"Insertado a: {result.inserted_ids}")
