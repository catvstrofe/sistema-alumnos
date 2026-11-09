"""!
@file app.py
@brief API de gestión de alumnos "Sistema Alumnos" (actividad OCY1102).
"""
import os
from flask import Flask, jsonify, request

## Aplicación Flask principal.
app = Flask(__name__)

## Base de datos en memoria (solo para fines de la actividad).
ALUMNOS = [
    {"id": 1, "nombre": "Ana Pérez", "carrera": "Ingeniería en Informática", "promedio": 6.1},
    {"id": 2, "nombre": "Benjamín Rojas", "carrera": "Ingeniería en Ciberseguridad", "promedio": 5.4},
    {"id": 3, "nombre": "Camila Soto", "carrera": "Analista Programador", "promedio": 6.8},
]

## La versión la inyecta el pipeline (ver Jenkinsfile). Sirve para la trazabilidad.
VERSION = os.environ.get("APP_VERSION", "dev")


@app.route('/hello')
def hello():
    """!
    @brief Endpoint para saludar al usuario.
    
    Toma el parámetro opcional 'name' desde los argumentos de la URL (query string).

    @return Mensaje de saludo en texto plano.
    """
    name = request.args.get('name')
    return f"Hello, {name}!"


@app.route('/health')
def health():
    """!
    @brief Endpoint para comprobar la salud de la aplicación.

    @return JSON con el estado de la aplicación.
    """
    return jsonify({"estado": "ok"})


@app.route('/version')
def version():
    """!
    @brief Endpoint para obtener la versión actual de la aplicación.

    @return JSON con el nombre de la aplicación y la versión inyectada por el pipeline.
    """
    return jsonify({"aplicacion": "Sistema Alumnos", "version": VERSION})


@app.route('/alumnos')
def listar_alumnos():
    """!
    @brief Obtiene la lista completa de alumnos.

    @return JSON con la lista de alumnos registrados.
    """
    return jsonify(ALUMNOS)


@app.route('/alumnos/<int:alumno_id>')
def obtener_alumno(alumno_id):
    """!
    @brief Obtiene un alumno por su identificador único.

    @param alumno_id Identificador numérico del alumno.
    @return JSON con la información del alumno, o mensaje de error 404 si no se encuentra.
    """
    for alumno in ALUMNOS:
        if alumno["id"] == alumno_id:
            return jsonify(alumno)
    return jsonify({"error": "Alumno no encontrado"}), 404


@app.route('/alumnos', methods=['POST'])
def crear_alumno():
    """!
    @brief Registra un nuevo alumno en la base de datos.

    Lee los campos 'nombre', 'promedio' y opcionalmente 'carrera' del cuerpo JSON de la solicitud.

    @return JSON con el alumno creado (código 201) o mensaje de error (código 400).
    """
    datos = request.get_json(silent=True) or {}
    nombre = str(datos.get("nombre", "")).strip()
    promedio = datos.get("promedio")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400
    if not isinstance(promedio, (int, float)) or not 1.0 <= promedio <= 7.0:
        return jsonify({"error": "El 'promedio' debe ser un número entre 1.0 y 7.0"}), 400

    nuevo = {
        "id": max(a["id"] for a in ALUMNOS) + 1,
        "nombre": nombre,
        "carrera": str(datos.get("carrera", "Sin carrera")),
        "promedio": promedio,
    }
    ALUMNOS.append(nuevo)
    return jsonify(nuevo), 201


def main():
    """!
    @brief Función principal de entrada para ejecutar el servidor de desarrollo Flask.
    """
    app.run(debug=True)


if __name__ == '__main__':
    main()