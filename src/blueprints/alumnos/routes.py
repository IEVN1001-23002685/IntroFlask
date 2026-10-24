from flask import Blueprint, jsonfy, request
from database import mysql

alumnos_bp = Blueprint ('alumnos', __name__, url_prefix = '/api/alumnos')

def fila_a_diccionario(curso, fila):
    columnas = [columna[0] for columna in curso.description]
    return dict(zip(columnas, fila))

@alumnos_bp.route('', methods = ['GET'])
def lista_alumnos():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos """)

        datos = cursor.fetchall()
        alumnos = [fila_a_diccionario(cursor, fila)
                   for fila in datos]
        return jsonfy({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        }), 200

    except Exception:
        return jsonfy({
            'mensaje': 'Error al consultar los alumnos',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()