"""Frame para el módulo de reportes y exportación CSV."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from services.pago_service import PagoService


class ReportesFrame(ttk.Frame):
    """Módulo de reportes: vencidos, por vencer y exportación CSV."""

    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.pago_service = PagoService()
        self.datos_actuales = []

        self._crear_widgets()

    def _crear_widgets(self):
        """Construye la interfaz del módulo de reportes."""
        # ── Panel superior: Filtros ──────────────────────────────────────
        frame_filtros = ttk.LabelFrame(self, text="Filtros de Reporte",
                                       padding=10)
        frame_filtros.pack(fill='x', padx=10, pady=(10, 5))

        ttk.Button(
            frame_filtros,
            text="📋 Todos los pagos",
            command=self._mostrar_todos
        ).pack(side='left', padx=5, ipadx=5, ipady=3)

        ttk.Button(
            frame_filtros,
            text="❌ Socios con membresía vencida",
            command=self._mostrar_vencidos
        ).pack(side='left', padx=5, ipadx=5, ipady=3)

        ttk.Button(
            frame_filtros,
            text="⚠️ Socios por vencer (7 días)",
            command=self._mostrar_por_vencer
        ).pack(side='left', padx=5, ipadx=5, ipady=3)

        ttk.Button(
            frame_filtros,
            text="📥 Exportar a CSV",
            command=self._exportar_csv
        ).pack(side='right', padx=5, ipadx=10, ipady=3)

        # ── Etiqueta informativa ─────────────────────────────────────────
        self.lbl_info = ttk.Label(
            self, text="Seleccione un filtro para generar el reporte.",
            font=('Segoe UI', 10, 'italic')
        )
        self.lbl_info.pack(padx=10, pady=5, anchor='w')

        # ── Panel central: Treeview ──────────────────────────────────────
        frame_tabla = ttk.Frame(self)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        columnas = ('id', 'folio', 'socio', 'plan', 'fecha_pago',
                    'vigencia', 'monto')
        self.tree = ttk.Treeview(frame_tabla, columns=columnas,
                                 show='headings', height=18)

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
        """Limpia el reporte actual al cambiar de pestaña."""
        pass  # No recarga automáticamente; el usuario elige filtro

    def _cargar_datos_en_tabla(self, datos):
        """Carga una lista de diccionarios en el Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.datos_actuales = datos

        for pago in datos:
            self.tree.insert('', 'end', values=(
                pago['id'],
                pago['folio'],
                pago['socio_nombre'],
                pago['plan_nombre'],
                pago['fecha_pago'],
                pago['vigencia_hasta'],
                f"{pago['monto']:.2f}"
            ))

    def _mostrar_todos(self):
        """Muestra todos los pagos registrados."""
        datos = self.pago_service.listar_pagos()
        self._cargar_datos_en_tabla(datos)
        self.lbl_info.config(
            text=f"📋 Todos los pagos — {len(datos)} registro(s)"
        )

    def _mostrar_vencidos(self):
        """Muestra socios con membresía vencida."""
        datos = self.pago_service.obtener_pagos_vencidos()
        self._cargar_datos_en_tabla(datos)
        self.lbl_info.config(
            text=f"❌ Socios con membresía vencida — "
                 f"{len(datos)} registro(s)"
        )

    def _mostrar_por_vencer(self):
        """Muestra socios cuya membresía vence en los próximos 7 días."""
        datos = self.pago_service.obtener_pagos_por_vencer(dias=7)
        self._cargar_datos_en_tabla(datos)
        self.lbl_info.config(
            text=f"⚠️ Socios por vencer en 7 días — "
                 f"{len(datos)} registro(s)"
        )

    def _exportar_csv(self):
        """Exporta los datos actuales del reporte a un archivo CSV."""
        if not self.datos_actuales:
            messagebox.showwarning(
                "Sin datos",
                "No hay datos para exportar. Aplique un filtro primero."
            )
            return

        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos", "*.*")],
            title="Guardar reporte como CSV"
        )

        if not ruta:
            return

        try:
            self.pago_service.exportar_csv(self.datos_actuales, ruta)
            messagebox.showinfo(
                "Exportación exitosa",
                f"Reporte exportado correctamente a:\n{ruta}"
            )
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
