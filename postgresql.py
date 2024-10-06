from random import choice

from faker import Faker
import psycopg2, os
from faker.generator import random
from dotenv import load_dotenv

load_dotenv()

try:
    print("Datos de conexión a la base de datos:")
    print(f"DB: {os.getenv('PG_DB')}")
    print(f"USER: {os.getenv('PG_USER')}")

    connection = psycopg2.connect(

        database=os.getenv('PG_DB'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASSWORD'),
        host=os.getenv('PG_HOST'),
        port=os.getenv('PG_PORT')
    )
except psycopg2.Error as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit(1)

faker = Faker()

especialidades = [
    'Cardiología',
    'Pediatría',
    'Oftalmología',
    'Neurología',
    'Dermatología',
    'Ginecología/Obstericia',
    'Traumatología',
    'Oncología',
    'Urología',
    'Psiquiatría',
    'Endocrinología',
    'Reumatología',
    'Hematología',
    'Nefrología',
    'Neumonología',
    'Nutriología',
    'Odontología',
    'Otorrinolaringología',
    'Proctología',
    'Radiología',
    'Toxicología',
    'Anestesiología',
    'Epidemiología',
    'Geriatría',
    'Medicina general',
    'Medicina interna',
    'Psicología',
    'Terapia física'
]

def generar_doctores(num):
    doctors = []
    for _ in range(num):
        dni =  faker.unique.random_number(digits=8),
        nombres =  faker.first_name(),
        apellidos =  faker.last_name(),
        especialidad =  random.choice(especialidades),
        totalcitas = random.randint(0, 100),

        doctors.append((dni, nombres, apellidos, especialidad, totalcitas))
    return doctors

def generar_disponibilidades(doctores):
    disponibilidades = []
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    for doctor in doctores:
        dni_doctor = doctor[0]
        num_dispos = random.randint(1, 5)
        for _ in range(num_dispos):
            dia = choice(dias)
            hora = faker.time()
            disponibilidades.append((dia, hora, dni_doctor))

    return disponibilidades

print("Cuantos numeros de doctores quieres generar?")
n = int(input())

doctor_data = generar_doctores(n)
with connection.cursor() as cursor:
    cursor.executemany("""
        INSERT INTO Doctor (dni, nombres, apellidos, especialidad, totalcitas) 
        VALUES (%s, %s, %s, %s, %s);
    """, doctor_data)

with connection.cursor() as cursor:
    disponibilidades = generar_disponibilidades(doctor_data)
    cursor.executemany("""
        INSERT INTO Disponibilidad (dia, hora, dni_doctor) 
        VALUES (%s, %s, %s);
    """, disponibilidades)

connection.commit()
connection.close()

print("Datos generados y almacenados exitosamente!")



