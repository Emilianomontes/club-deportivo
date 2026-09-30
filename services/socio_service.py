"""Servicio de negocio para la gestión de socios."""

import sqlite3
from models.socio import Socio
from repositories.socio_repository import SocioRepository


class SocioService:
    """Reglas de negocio y validaciones para socios del club."""

    def __init__(self):
        self.repo = SocioRepository()

    def listar_socios(self, solo_activos=True):
        """Lista socios, opcionalmente solo los activos."""
        return self.repo.listar(solo_activos)

    def buscar_socios(self, termino: str, solo_activos=True):
        """Busca socios por folio, nombre o correo."""
        return self.repo.buscar(termino, solo_activos)

    def obtener_socio(self, socio_id: int):
        """Obtiene un socio por ID."""
        return self.repo.obtener_por_id(socio_id)

    def crear_socio(self, folio: str, nombre: str, telefono: str,
                    correo: str):
        """
        Crea un nuevo socio con validaciones de negocio.
        Lanza ValueError si los datos son inválidos.
        Lanza sqlite3.IntegrityError si folio o correo ya existen.
        """
        # Validaciones
        if not folio or not folio.strip():
            raise ValueError("El folio es obligatorio.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio.")
        if not correo or not correo.strip():
            raise ValueError("El correo es obligatorio.")

        socio = Socio(
            folio=folio.strip(),
            nombre=nombre.strip(),
            telefono=telefono.strip() if telefono else '',
            correo=correo.strip(),
            activo=1
        )
        return self.repo.crear(socio)

    def actualizar_socio(self, socio_id: int, folio: str, nombre: str,
                         telefono: str, correo: str):
        """
        Actualiza los datos de un socio existente.
        Lanza ValueError si los datos son inválidos.
        """
        if not folio or not folio.strip():
            raise ValueError("El folio es obligatorio.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio.")
        if not correo or not correo.strip():
            raise ValueError("El correo es obligatorio.")

        socio = self.repo.obtener_por_id(socio_id)
        if socio is None:
            raise ValueError("Socio no encontrado.")

        socio.folio = folio.strip()
        socio.nombre = nombre.strip()
        socio.telefono = telefono.strip() if telefono else ''
        socio.correo = correo.strip()
        self.repo.actualizar(socio)
        return socio

    def desactivar_socio(self, socio_id: int):
        """
        Desactiva un socio lógicamente.
        Si tiene pagos asociados, se desactiva en vez de eliminar.
        """
        socio = self.repo.obtener_por_id(socio_id)
        if socio is None:
            raise ValueError("Socio no encontrado.")
        self.repo.desactivar(socio_id)

    def activar_socio(self, socio_id: int):
        """Reactiva un socio previamente desactivado."""
        socio = self.repo.obtener_por_id(socio_id)
        if socio is None:
            raise ValueError("Socio no encontrado.")
        self.repo.activar(socio_id)

    def generar_folio(self) -> str:
        """Genera automáticamente el siguiente folio disponible."""
        return self.repo.obtener_siguiente_folio()
