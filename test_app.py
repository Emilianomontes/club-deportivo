"""Script de prueba para validar todas las capas del sistema."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from db.database import init_db
from services.auth_service import AuthService
from services.socio_service import SocioService
from services.plan_service import PlanService
from services.pago_service import PagoService


def test_all():
    # 1. Base de datos
    print("=" * 60)
    print("PRUEBA: Inicializacion de base de datos")
    init_db()
    print("  OK - Base de datos inicializada correctamente")

    # 2. Autenticacion
    print("\nPRUEBA: Autenticacion")
    auth = AuthService()

    u1 = auth.autenticar('admin', 'admin123')
    assert u1 is not None, "Fallo login admin"
    assert u1.rol == 'administrador'
    print(f"  OK - Login admin: {u1}")

    u2 = auth.autenticar('operador1', 'operador123')
    assert u2 is not None, "Fallo login operador"
    assert u2.rol == 'operador'
    print(f"  OK - Login operador: {u2}")

    u3 = auth.autenticar('admin', 'wrongpass')
    assert u3 is None
    print("  OK - Login con password incorrecta rechazado")

    u4 = auth.autenticar('noexiste', 'test')
    assert u4 is None
    print("  OK - Login con usuario inexistente rechazado")

    # 3. Socios
    print("\nPRUEBA: Servicio de Socios")
    ss = SocioService()

    socios_activos = ss.listar_socios(solo_activos=True)
    print(f"  OK - Socios activos: {len(socios_activos)}")
    assert len(socios_activos) == 7, f"Esperados 7, obtenidos {len(socios_activos)}"

    socios_todos = ss.listar_socios(solo_activos=False)
    print(f"  OK - Socios totales: {len(socios_todos)}")
    assert len(socios_todos) == 8, f"Esperados 8, obtenidos {len(socios_todos)}"

    busqueda = ss.buscar_socios("Juan", solo_activos=True)
    print(f"  OK - Busqueda 'Juan': {len(busqueda)} resultado(s)")
    assert len(busqueda) >= 1

    folio = ss.generar_folio()
    print(f"  OK - Siguiente folio generado: {folio}")

    # 4. Planes
    print("\nPRUEBA: Servicio de Planes")
    ps = PlanService()

    planes = ps.listar_planes(solo_activos=True)
    print(f"  OK - Planes activos: {len(planes)}")
    assert len(planes) == 5, f"Esperados 5, obtenidos {len(planes)}"

    for plan in planes:
        print(f"    - {plan.nombre}: {plan.duracion_dias}d, ${plan.precio:.2f}")

    # 5. Pagos
    print("\nPRUEBA: Servicio de Pagos")
    pago_svc = PagoService()

    pagos = pago_svc.listar_pagos()
    print(f"  OK - Pagos totales: {len(pagos)}")
    assert len(pagos) >= 3

    for p in pagos:
        print(f"    - Pago #{p['id']}: {p['socio_nombre']} | "
              f"{p['plan_nombre']} | Vigencia: {p['vigencia_hasta']}")

    vencidos = pago_svc.obtener_pagos_vencidos()
    print(f"  OK - Membresias vencidas: {len(vencidos)}")

    por_vencer = pago_svc.obtener_pagos_por_vencer(dias=7)
    print(f"  OK - Por vencer (7 dias): {len(por_vencer)}")

    # 6. Prueba de registro de pago
    print("\nPRUEBA: Registrar nuevo pago")
    nuevo_pago = pago_svc.registrar_pago(socio_id=4, plan_id=1)
    print(f"  OK - Pago registrado: #{nuevo_pago.id}, "
          f"vigencia hasta {nuevo_pago.vigencia_hasta}")

    # 7. Validaciones de negocio
    print("\nPRUEBA: Validaciones de negocio")
    try:
        pago_svc.registrar_pago(socio_id=7, plan_id=1)
        print("  FALLO - Debio lanzar excepcion por socio inactivo")
    except ValueError as e:
        print(f"  OK - Socio inactivo rechazado: {e}")

    try:
        ss.crear_socio('', 'Test', '123', 'test@test.com')
        print("  FALLO - Debio lanzar excepcion por folio vacio")
    except ValueError as e:
        print(f"  OK - Folio vacio rechazado: {e}")

    print("\n" + "=" * 60)
    print("TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
    print("=" * 60)


if __name__ == '__main__':
    test_all()
