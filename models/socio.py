"""Modelo de dominio para socios del club deportivo."""


class Socio:
    """Representa un socio/miembro del club deportivo."""

    def __init__(self, id=None, folio='', nombre='', telefono='',
                 correo='', activo=1):
        self.id = id
        self.folio = folio
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.activo = activo

    def esta_activo(self):
        """Retorna True si el socio está activo."""
        return self.activo == 1

    def __repr__(self):
        return (f"Socio(id={self.id}, folio='{self.folio}', "
                f"nombre='{self.nombre}', activo={self.activo})")
