"""Repositorio de persistencia para usuarios del sistema."""

from db.database import get_connection
from models.usuario import Usuario


class UsuarioRepository:
    """Acceso a datos de la tabla usuarios_sistema."""

    def buscar_por_username(self, username: str):
        """Busca un usuario por su nombre de usuario. Retorna Usuario o None."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM usuarios_sistema WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            if row:
                return self._row_to_usuario(row)
            return None
        finally:
            conn.close()

    def listar_todos(self):
        """Retorna todos los usuarios del sistema."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios_sistema ORDER BY id")
            return [self._row_to_usuario(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def crear(self, usuario: Usuario):
        """Inserta un nuevo usuario y retorna el objeto con id asignado."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios_sistema (username, password_hash, rol, activo) "
                "VALUES (?, ?, ?, ?)",
                (usuario.username, usuario.password_hash, usuario.rol, usuario.activo)
            )
            conn.commit()
            usuario.id = cursor.lastrowid
            return usuario
        finally:
            conn.close()

    def actualizar(self, usuario: Usuario):
        """Actualiza los datos de un usuario existente."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuarios_sistema SET username=?, password_hash=?, "
                "rol=?, activo=? WHERE id=?",
                (usuario.username, usuario.password_hash, usuario.rol,
                 usuario.activo, usuario.id)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _row_to_usuario(row) -> Usuario:
        """Convierte una fila de sqlite3.Row a un objeto Usuario."""
        return Usuario(
            id=row['id'],
            username=row['username'],
            password_hash=row['password_hash'],
            rol=row['rol'],
            activo=row['activo']
        )
