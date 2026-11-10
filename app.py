
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import date, datetime

app = Flask(__name__)

# CONEXIÓN A LA BASE DE DATOS
def conectar_db():
    conexion = sqlite3.connect("database.db")
    conexion.row_factory = sqlite3.Row
    return conexion


# CREAR TABLA DE COTIZACIONES
def crear_tabla():

    conexion = conectar_db()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            paquete TEXT NOT NULL,
            personas INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            comentarios TEXT,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexion.commit()
    conexion.close()


# PÁGINA PRINCIPAL
@app.route("/")
def inicio():
    return render_template("index.html")


# RECIBIR COTIZACIONES
@app.route("/api/cotizaciones", methods=["POST"])
def registrar_cotizacion():

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Solicitud inválida."}), 400

    nombre = datos.get("nombre", "").strip()
    correo = datos.get("correo", "").strip()
    paquete = datos.get("paquete", "")
    personas = datos.get("personas")
    fecha = datos.get("fecha", "")
    comentarios = datos.get("comentarios", "").strip()

    # VALIDAR DATOS
    if not nombre or len(nombre) > 100:
        return jsonify({"error": "Escribe un nombre válido."}), 400

    if not correo or len(correo) > 150 or "@" not in correo:
        return jsonify({"error": "Escribe un correo válido."}), 400

    if paquete not in ["1 día", "2 días"]:
        return jsonify({"error": "Selecciona un paquete válido."}), 400

    if isinstance(personas, bool) or not isinstance(personas, int):
        return jsonify({"error": "Número de viajeros inválido."}), 400

    if personas < 1 or personas > 30:
        return jsonify({"error": "El número de viajeros debe estar entre 1 y 30."}), 400

    try:
        fecha_viaje = date.fromisoformat(fecha)

        if fecha_viaje < date.today():
            return jsonify({"error": "La fecha debe ser hoy o posterior."}), 400

    except (ValueError, TypeError):
        return jsonify({"error": "Selecciona una fecha válida."}), 400

    if len(comentarios) > 1000:
        return jsonify({"error": "Los comentarios son demasiado largos."}), 400

    # GUARDAR EN SQLITE
    conexion = conectar_db()

    try:

        cursor = conexion.execute("""
            INSERT INTO cotizaciones
            (nombre, correo, paquete, personas, fecha, comentarios)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nombre,
            correo,
            paquete,
            personas,
            fecha,
            comentarios
        ))

        conexion.commit()

        nuevo_id = cursor.lastrowid

    except sqlite3.Error:
        conexion.rollback()
        return jsonify({"error": "Error al guardar la cotización."}), 500

    finally:
        conexion.close()

    return jsonify({
        "mensaje": "Cotización registrada correctamente.",
        "id": nuevo_id
    }), 201


# INICIAR SERVIDOR
if __name__ == "__main__":

    crear_tabla()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
