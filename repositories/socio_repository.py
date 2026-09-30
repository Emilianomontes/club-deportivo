"""Repositorio de persistencia para socios del club."""

from db.database import get_connection
from models.socio import Socio


class SocioRepository:
    """Acceso a datos de la tabla socios."""

    def listar(self, solo_activos=True):
        """Retorna la lista de socios, opcionalmente solo los activos."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if solo_activos:
                cursor.execute(
                    "SELECT * FROM socios WHERE activo = 1 ORDER BY id"
                )
            else:
                cursor.execute("SELECT * FROM socios ORDER BY id")
            return [self._row_to_socio(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def buscar(self, termino: str, solo_activos=True):
        """Busca socios por folio, nombre o correo."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            like = f"%{termino}%"
            if solo_activos:
                cursor.execute(
                    "SELECT * FROM socios WHERE activo = 1 AND "
                    "(folio LIKE ? OR nombre LIKE ? OR correo LIKE ?) ORDER BY id",
                    (like, like, like)
                )
            else:
                cursor.execute(
                    "SELECT * FROM socios WHERE "
                    "(folio LIKE ? OR nombre LIKE ? OR correo LIKE ?) ORDER BY id",
                    (like, like, like)
                )
            return [self._row_to_socio(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def obtener_por_id(self, socio_id: int):
        """Obtiene un socio por su ID. Retorna Socio o None."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM socios WHERE id = ?", (socio_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_socio(row)
            return None
        finally:
            conn.close()

    def obtener_por_folio(self, folio: str):
        """Obtiene un socio por su folio. Retorna Socio o None."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM socios WHERE folio = ?", (folio,))
            row = cursor.fetchone()
            if row:
                return self._row_to_socio(row)
            return None
        finally:
            conn.close()

    def crear(self, socio: Socio):
        """Inserta un nuevo socio y retorna el objeto con id asignado."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO socios (folio, nombre, telefono, correo, activo) "
                "VALUES (?, ?, ?, ?, ?)",
                (socio.folio, socio.nombre, socio.telefono, socio.correo,
                 socio.activo)
            )
            conn.commit()
            socio.id = cursor.lastrowid
            return socio
        finally:
            conn.close()

    def actualizar(self, socio: Socio):
        """Actualiza los datos de un socio existente."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE socios SET folio=?, nombre=?, telefono=?, "
                "correo=?, activo=? WHERE id=?",
                (socio.folio, socio.nombre, socio.telefono, socio.correo,
                 socio.activo, socio.id)
            )
            conn.commit()
        finally:
            conn.close()

    def desactivar(self, socio_id: int):
        """Desactiva lógicamente un socio (activo = 0)."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE socios SET activo = 0 WHERE id = ?", (socio_id,)
            )
            conn.commit()
        finally:
            conn.close()

    def activar(self, socio_id: int):
        """Reactiva un socio (activo = 1)."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE socios SET activo = 1 WHERE id = ?", (socio_id,)
            )
            conn.commit()
        finally:
            conn.close()

    def tiene_pagos(self, socio_id: int) -> bool:
        """Verifica si un socio tiene pagos asociados."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM pagos WHERE socio_id = ?", (socio_id,)
            )
            return cursor.fetchone()[0] > 0
        finally:
            conn.close()

    def obtener_siguiente_folio(self) -> str:
        """Genera el siguiente folio secuencial (S001, S002, ...)."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT folio FROM socios ORDER BY id DESC LIMIT 1"
            )
            row = cursor.fetchone()
            if row:
                ultimo_num = int(row['folio'][1:])
                return f"S{ultimo_num + 1:03d}"
            return "S001"
        finally:
            conn.close()

    @staticmethod
    def _row_to_socio(row) -> Socio:
        """Convierte una fila de sqlite3.Row a un objeto Socio."""
        return Socio(
            id=row['id'],
            folio=row['folio'],
            nombre=row['nombre'],
            telefono=row['telefono'],
            correo=row['correo'],
            activo=row['activo']
        )
