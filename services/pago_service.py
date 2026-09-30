"""Servicio de negocio para la gestión de pagos/inscripciones."""

import csv
from datetime import date, timedelta

from models.pago import Pago
from repositories.pago_repository import PagoRepository
from repositories.socio_repository import SocioRepository
from repositories.plan_repository import PlanRepository


class PagoService:
    """Reglas de negocio para pagos: cálculo de vigencia, validaciones, reportes."""

    def __init__(self):
        self.pago_repo = PagoRepository()
        self.socio_repo = SocioRepository()
        self.plan_repo = PlanRepository()

    def registrar_pago(self, socio_id: int, plan_id: int):
        """
        Registra un nuevo pago/inscripción con las siguientes reglas:
        1. El socio debe existir y estar activo.
        2. El plan debe existir y estar activo.
        3. Si el socio ya tiene un pago vigente, la nueva vigencia
           se calcula desde la fecha de vencimiento actual.
        Retorna el objeto Pago creado.
        Lanza ValueError si alguna validación falla.
        """
        # Validar socio
        socio = self.socio_repo.obtener_por_id(socio_id)
        if socio is None:
            raise ValueError("El socio seleccionado no existe.")
        if not socio.esta_activo():
            raise ValueError(
                "No se pueden registrar pagos para socios inactivos."
            )

        # Validar plan
        plan = self.plan_repo.obtener_por_id(plan_id)
        if plan is None:
            raise ValueError("El plan seleccionado no existe.")
        if not plan.esta_activo():
            raise ValueError(
                "No se pueden vender planes inactivos."
            )

        # Calcular fechas
        hoy = date.today()
        fecha_pago = hoy

        # Si tiene pago vigente, sumar días desde la vigencia actual
        pago_vigente = self.pago_repo.obtener_ultimo_pago_vigente(
            socio_id, hoy.isoformat()
        )
        if pago_vigente:
            fecha_inicio = date.fromisoformat(pago_vigente.vigencia_hasta)
        else:
            fecha_inicio = hoy

        vigencia_hasta = fecha_inicio + timedelta(days=plan.duracion_dias)

        pago = Pago(
            socio_id=socio_id,
            plan_id=plan_id,
            fecha_pago=fecha_pago.isoformat(),
            vigencia_hasta=vigencia_hasta.isoformat(),
            monto=plan.precio
        )
        return self.pago_repo.crear(pago)

    def listar_pagos(self):
        """Lista todos los pagos con datos de socio y plan (JOIN)."""
        return self.pago_repo.listar_con_detalle()

    def obtener_pagos_vencidos(self):
        """Obtiene pagos de socios con membresía vencida."""
        hoy = date.today().isoformat()
        return self.pago_repo.obtener_vencidos(hoy)

    def obtener_pagos_por_vencer(self, dias=7):
        """Obtiene pagos que vencen dentro de los próximos N días."""
        hoy = date.today()
        limite = hoy + timedelta(days=dias)
        return self.pago_repo.obtener_por_vencer(
            hoy.isoformat(), limite.isoformat()
        )

    @staticmethod
    def exportar_csv(datos: list, ruta: str):
        """
        Exporta una lista de diccionarios a un archivo CSV.
        Retorna True si la exportación fue exitosa.
        Lanza ValueError si no hay datos para exportar.
        """
        if not datos:
            raise ValueError("No hay datos para exportar.")

        encabezados = list(datos[0].keys())
        with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictWriter(archivo, fieldnames=encabezados)
            writer.writeheader()
            writer.writerows(datos)
        return True
