"""Modelo de dominio para pagos/inscripciones."""


class Pago:
    """Representa un pago o inscripción de un socio a un plan."""

    def __init__(self, id=None, socio_id=None, plan_id=None,
                 fecha_pago='', vigencia_hasta='', monto=0.0):
        self.id = id
        self.socio_id = socio_id
        self.plan_id = plan_id
        self.fecha_pago = fecha_pago
        self.vigencia_hasta = vigencia_hasta
        self.monto = monto

    def __repr__(self):
        return (f"Pago(id={self.id}, socio_id={self.socio_id}, "
                f"plan_id={self.plan_id}, vigencia_hasta='{self.vigencia_hasta}')")
