"""Servicio de negocio para la gestión de planes de membresía."""

from models.plan import Plan
from repositories.plan_repository import PlanRepository


class PlanService:
    """Reglas de negocio y validaciones para planes del club."""

    def __init__(self):
        self.repo = PlanRepository()

    def listar_planes(self, solo_activos=True):
        """Lista planes, opcionalmente solo los activos."""
        return self.repo.listar(solo_activos)

    def buscar_planes(self, termino: str, solo_activos=True):
        """Busca planes por nombre."""
        return self.repo.buscar(termino, solo_activos)

    def obtener_plan(self, plan_id: int):
        """Obtiene un plan por ID."""
        return self.repo.obtener_por_id(plan_id)

    def crear_plan(self, nombre: str, duracion_dias: int, precio: float):
        """
        Crea un nuevo plan con validaciones de negocio.
        Lanza ValueError si los datos son inválidos.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del plan es obligatorio.")
        if not isinstance(duracion_dias, int) or duracion_dias <= 0:
            raise ValueError("La duración debe ser un número entero positivo.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        plan = Plan(
            nombre=nombre.strip(),
            duracion_dias=duracion_dias,
            precio=float(precio),
            activo=1
        )
        return self.repo.crear(plan)

    def actualizar_plan(self, plan_id: int, nombre: str,
                        duracion_dias: int, precio: float):
        """
        Actualiza los datos de un plan existente.
        Lanza ValueError si los datos son inválidos.
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del plan es obligatorio.")
        if not isinstance(duracion_dias, int) or duracion_dias <= 0:
            raise ValueError("La duración debe ser un número entero positivo.")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        plan = self.repo.obtener_por_id(plan_id)
        if plan is None:
            raise ValueError("Plan no encontrado.")

        plan.nombre = nombre.strip()
        plan.duracion_dias = duracion_dias
        plan.precio = float(precio)
        self.repo.actualizar(plan)
        return plan

    def desactivar_plan(self, plan_id: int):
        """
        Desactiva un plan lógicamente.
        Si tiene pagos asociados, se desactiva en vez de eliminar.
        """
        plan = self.repo.obtener_por_id(plan_id)
        if plan is None:
            raise ValueError("Plan no encontrado.")
        self.repo.desactivar(plan_id)

    def activar_plan(self, plan_id: int):
        """Reactiva un plan previamente desactivado."""
        plan = self.repo.obtener_por_id(plan_id)
        if plan is None:
            raise ValueError("Plan no encontrado.")
        self.repo.activar(plan_id)
