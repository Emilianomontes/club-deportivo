"""Modelo de dominio para planes de membresía."""


class Plan:
    """Representa un plan/membresía del club deportivo."""

    def __init__(self, id=None, nombre='', duracion_dias=0,
                 precio=0.0, activo=1):
        self.id = id
        self.nombre = nombre
        self.duracion_dias = duracion_dias
        self.precio = precio
        self.activo = activo

    def esta_activo(self):
        """Retorna True si el plan está activo."""
        return self.activo == 1

    def __repr__(self):
        return (f"Plan(id={self.id}, nombre='{self.nombre}', "
                f"duracion={self.duracion_dias}d, precio=${self.precio:.2f})")
