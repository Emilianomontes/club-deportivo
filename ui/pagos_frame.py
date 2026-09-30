"""Frame para el módulo de pagos/inscripciones."""

import tkinter as tk
from tkinter import ttk, messagebox

from services.pago_service import PagoService
from services.socio_service import SocioService
from services.plan_service import PlanService


class PagosFrame(ttk.Frame):
    """Módulo de pagos: formulario de cobro y Treeview con JOIN."""

    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.pago_service = PagoService()
        self.socio_service = SocioService()
        self.plan_service = PlanService()

        # Mapas para los Combobox (nombre -> id)
        self.socios_map = {}
        self.planes_map = {}

        self._crear_widgets()
        self.refrescar()

    def _crear_widgets(self):
        """Construye la interfaz del módulo de pagos."""
        # ── Panel superior: Formulario de pago ───────────────────────────
        frame_form = ttk.LabelFrame(self, text="Registrar Nuevo Pago",
                                    padding=10)
        frame_form.pack(fill='x', padx=10, pady=(10, 5))

        row1 = ttk.Frame(frame_form)
        row1.pack(fill='x', pady=5)

        ttk.Label(row1, text="Socio:").pack(side='left')
        self.combo_socio = ttk.Combobox(row1, width=40, state='readonly')
        self.combo_socio.pack(side='left', padx=(5, 20))

        ttk.Label(row1, text="Plan:").pack(side='left')
        self.combo_plan = ttk.Combobox(row1, width=30, state='readonly')
        self.combo_plan.pack(side='left', padx=5)

        row2 = ttk.Frame(frame_form)
        row2.pack(fill='x', pady=5)

        ttk.Button(
            row2, text="💳 Registrar Pago", command=self._registrar_pago
        ).pack(side='left', padx=2, ipadx=10, ipady=3)

        ttk.Button(
            row2, text="🔄 Refrescar Listas", command=self._cargar_combos
        ).pack(side='left', padx=10)

        # ── Panel central: Treeview de pagos ─────────────────────────────
        frame_tabla = ttk.LabelFrame(self, text="Historial de Pagos",
                                     padding=5)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=(5, 10))

        columnas = ('id', 'folio', 'socio', 'plan', 'fecha_pago',
                    'vigencia', 'monto')
        self.tree = ttk.Treeview(frame_tabla, columns=columnas,
                                 show='headings', height=15)

        self.tree.heading('id', text='ID Pago')
        self.tree.heading('folio', text='Folio Socio')
        self.tree.heading('socio', text='Nombre Socio')
        self.tree.heading('plan', text='Plan')
        self.tree.heading('fecha_pago', text='Fecha Pago')
        self.tree.heading('vigencia', text='Vigencia Hasta')
        self.tree.heading('monto', text='Monto ($)')

        self.tree.column('id', width=60, anchor='center')
        self.tree.column('folio', width=80, anchor='center')
        self.tree.column('socio', width=180)
        self.tree.column('plan', width=120)
        self.tree.column('fecha_pago', width=110, anchor='center')
        self.tree.column('vigencia', width=110, anchor='center')
        self.tree.column('monto', width=90, anchor='e')

        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical',
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def refrescar(self):
        """Recarga combos y tabla de pagos."""
        self._cargar_combos()
        self._cargar_pagos()

    def _cargar_combos(self):
        """Carga las listas de socios activos y planes activos."""
        # Socios activos
        socios = self.socio_service.listar_socios(solo_activos=True)
        self.socios_map = {}
        valores_socios = []
        for s in socios:
            texto = f"{s.folio} - {s.nombre}"
            self.socios_map[texto] = s.id
            valores_socios.append(texto)
        self.combo_socio['values'] = valores_socios
        if valores_socios:
            self.combo_socio.current(0)

        # Planes activos
        planes = self.plan_service.listar_planes(solo_activos=True)
        self.planes_map = {}
        valores_planes = []
        for p in planes:
            texto = f"{p.nombre} ({p.duracion_dias}d - ${p.precio:.2f})"
            self.planes_map[texto] = p.id
            valores_planes.append(texto)
        self.combo_plan['values'] = valores_planes
        if valores_planes:
            self.combo_plan.current(0)

    def _cargar_pagos(self):
        """Carga el historial de pagos en el Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        pagos = self.pago_service.listar_pagos()
        for pago in pagos:
            self.tree.insert('', 'end', values=(
                pago['id'],
                pago['folio'],
                pago['socio_nombre'],
                pago['plan_nombre'],
                pago['fecha_pago'],
                pago['vigencia_hasta'],
                f"{pago['monto']:.2f}"
            ))

    def _registrar_pago(self):
        """Registra un nuevo pago con validaciones de negocio."""
        socio_texto = self.combo_socio.get()
        plan_texto = self.combo_plan.get()

        if not socio_texto or not plan_texto:
            messagebox.showwarning(
                "Campos vacíos",
                "Seleccione un socio y un plan."
            )
            return

        socio_id = self.socios_map.get(socio_texto)
        plan_id = self.planes_map.get(plan_texto)

        if socio_id is None or plan_id is None:
            messagebox.showerror(
                "Error", "Selección inválida. Refresque las listas."
            )
            return

        if not messagebox.askyesno(
            "Confirmar pago",
            f"¿Registrar pago?\n\n"
            f"Socio: {socio_texto}\n"
            f"Plan: {plan_texto}"
        ):
            return

        try:
            pago = self.pago_service.registrar_pago(socio_id, plan_id)
            messagebox.showinfo(
                "Pago registrado",
                f"Pago #{pago.id} registrado exitosamente.\n\n"
                f"Vigencia hasta: {pago.vigencia_hasta}\n"
                f"Monto: ${pago.monto:.2f}"
            )
            self._cargar_pagos()
        except ValueError as e:
            messagebox.showerror("Error de negocio", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))
