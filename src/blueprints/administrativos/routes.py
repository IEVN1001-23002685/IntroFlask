from flask import Blueprint, current_app, jsonify, request
from database import mysql

administrativos_bp = Blueprint(
    'administrativos',
    __name__,
    url_prefix='/api/administrativos'
)


def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


def leer_administrativo_bd(numempleado):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        sql = """
            SELECT numempleado, nombre, apellidos,
                   telefono, correo, departamento
            FROM administrativos
            WHERE numempleado = %s
        """

        cursor.execute(sql, (numempleado,))
        datos = cursor.fetchone()

        if datos is None:
            return None

        return fila_a_diccionario(cursor, datos)

    finally:
        if cursor is not None:
            cursor.close()


@administrativos_bp.route('', methods=['GET'], strict_slashes=False)
def lista_administrativos():
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT numempleado, nombre, apellidos,
                   telefono, correo, departamento
            FROM administrativos
        """)

        datos = cursor.fetchall()

        administrativos = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'administrativos': administrativos,
            'mensaje': 'Lista de administrativos',
            'exito': True
        }), 200

    except Exception:
        current_app.logger.exception('Error al consultar los administrativos')

        return jsonify({
            'mensaje': 'Error al consultar los administrativos',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@administrativos_bp.route('', methods=['POST'], strict_slashes=False)
def registrar_administrativo():
    cursor = None

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                'mensaje': 'Se requiere un objeto JSON válido',
                'exito': False
            }), 400

        campos = [
            'numempleado', 'nombre', 'apellidos',
            'telefono', 'correo', 'departamento'
        ]

        faltantes = [
            campo for campo in campos
            if campo not in datos or datos[campo] is None
        ]

        if faltantes:
            return jsonify({
                'mensaje': 'Faltan campos obligatorios',
                'campos': faltantes,
                'exito': False
            }), 400

        if leer_administrativo_bd(datos['numempleado']) is not None:
            return jsonify({
                'mensaje': 'El número de empleado ya existe',
                'exito': False
            }), 409

        cursor = mysql.connection.cursor()

        sql = """
            INSERT INTO administrativos
            (numempleado, nombre, apellidos,
             telefono, correo, departamento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = tuple(datos[campo] for campo in campos)

        cursor.execute(sql, valores)
        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Administrativo registrado',
            'exito': True
        }), 201

    except Exception:
        current_app.logger.exception('Error al registrar el administrativo')
        mysql.connection.rollback()

        return jsonify({
            'mensaje': 'Error al registrar el administrativo',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@administrativos_bp.route('/<numempleado>', methods=['PUT'])
def actualizar_administrativo(numempleado):
    cursor = None

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                'mensaje': 'Se requiere un objeto JSON válido',
                'exito': False
            }), 400

        campos = [
            'nombre', 'apellidos', 'telefono',
            'correo', 'departamento'
        ]

        faltantes = [
            campo for campo in campos
            if campo not in datos or datos[campo] is None
        ]

        if faltantes:
            return jsonify({
                'mensaje': 'Faltan campos obligatorios',
                'campos': faltantes,
                'exito': False
            }), 400

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            UPDATE administrativos
            SET nombre = %s,
                apellidos = %s,
                telefono = %s,
                correo = %s,
                departamento = %s
            WHERE numempleado = %s
            """,
            (
                datos['nombre'],
                datos['apellidos'],
                datos['telefono'],
                datos['correo'],
                datos['departamento'],
                numempleado
            )
        )

        if cursor.rowcount == 0:
            mysql.connection.rollback()

            return jsonify({
                'mensaje': 'Empleado no encontrado o sin cambios',
                'exito': False
            }), 404

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Administrativo actualizado',
            'exito': True
        }), 200

    except Exception:
        current_app.logger.exception('Error al actualizar el administrativo')
        mysql.connection.rollback()

        return jsonify({
            'mensaje': 'Error al actualizar el administrativo',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@administrativos_bp.route('/<numempleado>', methods=['DELETE'])
def eliminar_administrativo(numempleado):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            DELETE FROM administrativos
            WHERE numempleado = %s
            """,
            (numempleado,)
        )

        if cursor.rowcount == 0:
            return jsonify({
                'mensaje': 'Administrativo no encontrado',
                'exito': False
            }), 404

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Administrativo eliminado',
            'exito': True
        }), 200

    except Exception:
        current_app.logger.exception('Error al eliminar el administrativo')
        mysql.connection.rollback()

        return jsonify({
            'mensaje': 'Error al eliminar el administrativo',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
