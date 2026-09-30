"""Repositorio de persistencia para pagos/inscripciones."""

from db.database import get_connection
from models.pago import Pago


class PagoRepository:
    """Acceso a datos de la tabla pagos, con JOINs para reportes."""

    def crear(self, pago: Pago):
        """Inserta un nuevo pago y retorna el objeto con id asignado."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO pagos (socio_id, plan_id, fecha_pago, "
                "vigencia_hasta, monto) VALUES (?, ?, ?, ?, ?)",
                (pago.socio_id, pago.plan_id, pago.fecha_pago,
                 pago.vigencia_hasta, pago.monto)
            )
            conn.commit()
            pago.id = cursor.lastrowid
            return pago
        finally:
            conn.close()

    def listar_con_detalle(self):
        """
        Lista todos los pagos con JOIN a socios y planes.
        Retorna lista de diccionarios con datos completos.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, s.folio, s.nombre AS socio_nombre,
                       pl.nombre AS plan_nombre, p.fecha_pago,
                       p.vigencia_hasta, p.monto
                FROM pagos p
                INNER JOIN socios s ON p.socio_id = s.id
                INNER JOIN planes pl ON p.plan_id = pl.id
                ORDER BY p.id DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def obtener_ultimo_pago_vigente(self, socio_id: int, fecha_hoy: str):
        """
        Obtiene el último pago vigente de un socio (vigencia_hasta >= hoy).
        Retorna Pago o None.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM pagos WHERE socio_id = ? AND "
                "vigencia_hasta >= ? ORDER BY vigencia_hasta DESC LIMIT 1",
                (socio_id, fecha_hoy)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_pago(row)
            return None
        finally:
            conn.close()

    def obtener_vencidos(self, fecha_hoy: str):
        """
        Obtiene pagos vencidos (vigencia_hasta < hoy) con JOIN.
        Solo retorna el último pago de cada socio si ya venció.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, s.folio, s.nombre AS socio_nombre,
                       pl.nombre AS plan_nombre, p.fecha_pago,
                       p.vigencia_hasta, p.monto
                FROM pagos p
                INNER JOIN socios s ON p.socio_id = s.id
                INNER JOIN planes pl ON p.plan_id = pl.id
                WHERE p.vigencia_hasta < ?
                  AND s.activo = 1
                  AND NOT EXISTS (
                      SELECT 1 FROM pagos p2
                      WHERE p2.socio_id = p.socio_id
                        AND p2.vigencia_hasta >= ?
                  )
                ORDER BY p.vigencia_hasta ASC
            """, (fecha_hoy, fecha_hoy))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def obtener_por_vencer(self, fecha_hoy: str, fecha_limite: str):
        """
        Obtiene pagos cuya vigencia termina entre hoy y fecha_limite (inclusive).
        Usa JOIN para obtener datos completos.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, s.folio, s.nombre AS socio_nombre,
                       pl.nombre AS plan_nombre, p.fecha_pago,
                       p.vigencia_hasta, p.monto
                FROM pagos p
                INNER JOIN socios s ON p.socio_id = s.id
                INNER JOIN planes pl ON p.plan_id = pl.id
                WHERE p.vigencia_hasta >= ?
                  AND p.vigencia_hasta <= ?
                  AND s.activo = 1
                ORDER BY p.vigencia_hasta ASC
            """, (fecha_hoy, fecha_limite))
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def _row_to_pago(row) -> Pago:
        """Convierte una fila de sqlite3.Row a un objeto Pago."""
        return Pago(
            id=row['id'],
            socio_id=row['socio_id'],
            plan_id=row['plan_id'],
            fecha_pago=row['fecha_pago'],
            vigencia_hasta=row['vigencia_hasta'],
            monto=row['monto']
        )
