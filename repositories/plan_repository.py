"""Repositorio de persistencia para planes de membresía."""

from db.database import get_connection
from models.plan import Plan


class PlanRepository:
    """Acceso a datos de la tabla planes."""

    def listar(self, solo_activos=True):
        """Retorna la lista de planes, opcionalmente solo los activos."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if solo_activos:
                cursor.execute(
                    "SELECT * FROM planes WHERE activo = 1 ORDER BY id"
                )
            else:
                cursor.execute("SELECT * FROM planes ORDER BY id")
            return [self._row_to_plan(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def buscar(self, termino: str, solo_activos=True):
        """Busca planes por nombre."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            like = f"%{termino}%"
            if solo_activos:
                cursor.execute(
                    "SELECT * FROM planes WHERE activo = 1 AND "
                    "nombre LIKE ? ORDER BY id",
                    (like,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM planes WHERE nombre LIKE ? ORDER BY id",
                    (like,)
                )
            return [self._row_to_plan(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def obtener_por_id(self, plan_id: int):
        """Obtiene un plan por su ID. Retorna Plan o None."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM planes WHERE id = ?", (plan_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_plan(row)
            return None
        finally:
            conn.close()

    def crear(self, plan: Plan):
        """Inserta un nuevo plan y retorna el objeto con id asignado."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO planes (nombre, duracion_dias, precio, activo) "
                "VALUES (?, ?, ?, ?)",
                (plan.nombre, plan.duracion_dias, plan.precio, plan.activo)
            )
            conn.commit()
            plan.id = cursor.lastrowid
            return plan
        finally:
            conn.close()

    def actualizar(self, plan: Plan):
        """Actualiza los datos de un plan existente."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE planes SET nombre=?, duracion_dias=?, precio=?, "
                "activo=? WHERE id=?",
                (plan.nombre, plan.duracion_dias, plan.precio,
                 plan.activo, plan.id)
            )
            conn.commit()
        finally:
            conn.close()

    def desactivar(self, plan_id: int):
        """Desactiva lógicamente un plan (activo = 0)."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE planes SET activo = 0 WHERE id = ?", (plan_id,)
            )
            conn.commit()
        finally:
            conn.close()

    def activar(self, plan_id: int):
        """Reactiva un plan (activo = 1)."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE planes SET activo = 1 WHERE id = ?", (plan_id,)
            )
            conn.commit()
        finally:
            conn.close()

    def tiene_pagos(self, plan_id: int) -> bool:
        """Verifica si un plan tiene pagos asociados."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM pagos WHERE plan_id = ?", (plan_id,)
            )
            return cursor.fetchone()[0] > 0
        finally:
            conn.close()

    @staticmethod
    def _row_to_plan(row) -> Plan:
        """Convierte una fila de sqlite3.Row a un objeto Plan."""
        return Plan(
            id=row['id'],
            nombre=row['nombre'],
            duracion_dias=row['duracion_dias'],
            precio=row['precio'],
            activo=row['activo']
        )
