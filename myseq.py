import random
import sys, os
from dotenv import load_dotenv

import psycopg2
import mysql.connector
from pymongo import MongoClient
from faker import Faker

load_dotenv()

faker = Faker()

try:
    mongo_client = MongoClient(os.getenv('MONGO_CLIENT'))
    db = mongo_client['P1pacientes_test']
    collection = db['Pacientes']
    dnis_pacientes = [paciente['_id'] for paciente in collection.find({}, {'_id': 1})]
    print("Connection to MongoDB successful. Retrieved", len(dnis_pacientes), "patients.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    mongo_client = None
    sys.exit(1)


try:
    posgres_conn = psycopg2.connect(
        database=os.getenv('PG_DB'),
        user=os.getenv('PG_USER'),
        password=os.getenv('PG_PASSWORD'),
        host=os.getenv('PG_HOST'),
        port=os.getenv('PG_PORT')
    )
    posgres_cursor = posgres_conn.cursor()

    posgres_cursor.execute("SELECT dni, especialidad FROM doctores")
    doc_info = posgres_cursor.fetchall()
except Exception as e:
    print(f"Error connecting to PostgreSQL: {e}")
    posgres_conn = None
    sys.exit(1)

try:
    msql_conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        database=os.getenv('MYSQL_DB'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD')
    )

    if msql_conn.is_connected():
        db_Info = msql_conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = msql_conn.cursor()

        n_historias = 50

        for _ in range(n_historias):
            dni = random.choice(dnis_pacientes)
            fecha_creacion_historia = faker.date_time_this_year(before_now=True)

            cursor.execute("INSERT INTO historias_clinicas (dni, fecha_creacion_historia) VALUES (%s, %s)", (dni, fecha_creacion_historia))

            for _ in range(random.randint(1, 5)):
                dni_doctor, especialidad = random.choice(doc_info)
                fecha_consulta = faker.date_between(start_date=fecha_creacion_historia, end_date='now')
                hora_consulta = faker.date_time_between(pattern="%H:%M:%S", start_date="07:00:00", end_date="20:00:00")
                diagnostico = faker.text(max_nb_chars=100)
                tratamiento = faker.text(max_nb_chars=100)
                cursor.execute("INSERT INTO cita (dni_doctor, especialidad, fecha_consulta, hora_consulta, dni) VALUES (%s, %s, %s, %s, %s)", (dni_doctor, especialidad, fecha_consulta, hora_consulta, dni))
                print("Inserted consulta for dni", dni, "with doctor", dni_doctor)


except Exception as e:
    print("Error while connecting to MySQL", e)
finally:
    if msql_conn.is_connected():
        cursor.close()
        msql_conn.close()
        print("MySQL connection is closed")
