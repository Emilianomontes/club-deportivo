"""Servicio de autenticación de usuarios."""

import hashlib
from repositories.usuario_repository import UsuarioRepository


class AuthService:
    """Lógica de negocio para autenticación y gestión de contraseñas."""

    def __init__(self):
        self.repo = UsuarioRepository()

    @staticmethod
    def hash_password(password: str) -> str:
        """Genera el hash SHA-256 de una contraseña."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def autenticar(self, username: str, password: str):
        """
        Autentica un usuario por username y contraseña.
        Retorna el objeto Usuario si las credenciales son válidas
        y el usuario está activo. Retorna None en caso contrario.
        """
        if not username or not password:
            return None

        usuario = self.repo.buscar_por_username(username.strip())
        if usuario is None:
            return None

        if not usuario.esta_activo():
            return None

        password_hash = self.hash_password(password)
        if usuario.password_hash != password_hash:
            return None

        return usuario
