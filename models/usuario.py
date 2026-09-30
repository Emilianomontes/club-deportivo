"""Modelo de dominio para usuarios del sistema."""


class Usuario:
    """Representa un usuario del sistema (administrador u operador)."""

    def __init__(self, id=None, username='', password_hash='',
                 rol='operador', activo=1):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.rol = rol
        self.activo = activo

    def es_administrador(self):
        """Retorna True si el usuario tiene rol de administrador."""
        return self.rol == 'administrador'

    def esta_activo(self):
        """Retorna True si el usuario está activo."""
        return self.activo == 1

    def __repr__(self):
        return (f"Usuario(id={self.id}, username='{self.username}', "
                f"rol='{self.rol}', activo={self.activo})")
