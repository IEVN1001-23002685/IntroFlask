from flask import Blueprint, jsonfy, request
from database import mysql

maestros_bp = Blueprint ('maestros', __name__, url_prefix = '/api/maestros')

def fila_a_diccionario(curso, fila):
    columnas = [columna[0] for columna in curso.description]
    return dict(zip(columnas, fila))

@maestros_bp.route('', methods = ['GET'])
def lista_maestros():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT idmaestro, nombre, apaterno, amaterno, correo FROM maestros """)

        datos = cursor.fetchall()
        maestros = [fila_a_diccionario(cursor, fila)
                   for fila in datos]
        return jsonfy({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception:
        return jsonfy({
            'mensaje': 'Error al consultar los maestros',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()