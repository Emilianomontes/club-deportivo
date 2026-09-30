"""
Módulo de base de datos SQLite para el Club Deportivo.
Gestiona la conexión, creación de tablas (DDL) y datos semilla (seeders).
"""

import sqlite3
import hashlib
import os
from datetime import date, timedelta


# Ruta absoluta de la base de datos junto al directorio raíz del proyecto
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'club_deportivo.db')


def get_connection():
    """Crea y retorna una conexión a la base de datos SQLite con FK activadas."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def _hash_password(password: str) -> str:
    """Genera el hash SHA-256 de una contraseña."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def init_db():
    """Inicializa la base de datos: crea tablas y carga datos semilla."""
    conn = get_connection()
    cursor = conn.cursor()

    # ── DDL: Creación de tablas ──────────────────────────────────────────
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios_sistema (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            rol           TEXT    CHECK(rol IN ('administrador', 'operador')) NOT NULL,
            activo        INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS socios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            folio    TEXT    UNIQUE NOT NULL,
            nombre   TEXT    NOT NULL,
            telefono TEXT,
            correo   TEXT    UNIQUE NOT NULL,
            activo   INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS planes (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre        TEXT    UNIQUE NOT NULL,
            duracion_dias INTEGER NOT NULL CHECK(duracion_dias > 0),
            precio        REAL    NOT NULL CHECK(precio >= 0),
            activo        INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS pagos (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            socio_id       INTEGER NOT NULL,
            plan_id        INTEGER NOT NULL,
            fecha_pago     TEXT    NOT NULL,
            vigencia_hasta TEXT    NOT NULL,
            monto          REAL   NOT NULL,
            FOREIGN KEY (socio_id) REFERENCES socios(id),
            FOREIGN KEY (plan_id)  REFERENCES planes(id)
        );
    """)

    # ── Seeders: solo si las tablas están vacías ─────────────────────────
    cursor.execute("SELECT COUNT(*) FROM usuarios_sistema")
    if cursor.fetchone()[0] == 0:
        _seed_usuarios(cursor)

    cursor.execute("SELECT COUNT(*) FROM socios")
    if cursor.fetchone()[0] == 0:
        _seed_socios(cursor)

    cursor.execute("SELECT COUNT(*) FROM planes")
    if cursor.fetchone()[0] == 0:
        _seed_planes(cursor)

    cursor.execute("SELECT COUNT(*) FROM pagos")
    if cursor.fetchone()[0] == 0:
        _seed_pagos(cursor)

    conn.commit()
    conn.close()


# ── Funciones de seeding ─────────────────────────────────────────────────

def _seed_usuarios(cursor):
    """Inserta los usuarios de prueba del sistema."""
    usuarios = [
        ('admin',     _hash_password('admin123'),     'administrador'),
        ('operador1', _hash_password('operador123'),  'operador'),
    ]
    cursor.executemany(
        "INSERT INTO usuarios_sistema (username, password_hash, rol) VALUES (?, ?, ?)",
        usuarios
    )


def _seed_socios(cursor):
    """Inserta 8 socios de prueba (1 inactivo)."""
    socios = [
        ('S001', 'Juan Pérez',         '5551234567', 'juan.perez@email.com',      1),
        ('S002', 'María López',        '5552345678', 'maria.lopez@email.com',     1),
        ('S003', 'Carlos García',      '5553456789', 'carlos.garcia@email.com',   1),
        ('S004', 'Ana Martínez',       '5554567890', 'ana.martinez@email.com',    1),
        ('S005', 'Roberto Hernández',  '5555678901', 'roberto.hdz@email.com',     1),
        ('S006', 'Laura Sánchez',      '5556789012', 'laura.sanchez@email.com',   1),
        ('S007', 'Diego Torres',       '5557890123', 'diego.torres@email.com',    0),
        ('S008', 'Patricia Flores',    '5558901234', 'patricia.flores@email.com', 1),
    ]
    cursor.executemany(
        "INSERT INTO socios (folio, nombre, telefono, correo, activo) "
        "VALUES (?, ?, ?, ?, ?)",
        socios
    )


def _seed_planes(cursor):
    """Inserta 5 planes de membresía de prueba."""
    planes = [
        ('Pase Diario', 1,   50.00,   1),
        ('Mensual',      30,  500.00,  1),
        ('Trimestral',   90,  1200.00, 1),
        ('Anual',        365, 4000.00, 1),
        ('VIP',          365, 6000.00, 1),
    ]
    cursor.executemany(
        "INSERT INTO planes (nombre, duracion_dias, precio, activo) "
        "VALUES (?, ?, ?, ?)",
        planes
    )


def _seed_pagos(cursor):
    """Inserta 3 pagos de prueba: vigente, vencido y por vencer."""
    hoy = date.today()

    # 1) Pago vigente – Socio 1 (Juan), Plan Mensual (id=2)
    fp_vigente = hoy - timedelta(days=5)
    vh_vigente = fp_vigente + timedelta(days=30)

    # 2) Pago vencido – Socio 3 (Carlos), Plan Mensual (id=2)
    fp_vencido = hoy - timedelta(days=60)
    vh_vencido = fp_vencido + timedelta(days=30)

    # 3) Pago por vencer en ~3 días – Socio 2 (María), Plan Mensual (id=2)
    fp_por_vencer = hoy - timedelta(days=27)
    vh_por_vencer = fp_por_vencer + timedelta(days=30)

    pagos = [
        (1, 2, fp_vigente.isoformat(),    vh_vigente.isoformat(),    500.00),
        (3, 2, fp_vencido.isoformat(),    vh_vencido.isoformat(),    500.00),
        (2, 2, fp_por_vencer.isoformat(), vh_por_vencer.isoformat(), 500.00),
    ]
    cursor.executemany(
        "INSERT INTO pagos (socio_id, plan_id, fecha_pago, vigencia_hasta, monto) "
        "VALUES (?, ?, ?, ?, ?)",
        pagos
    )
