"""Frame CRUD para la gestión de planes de membresía."""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from services.plan_service import PlanService


class PlanesFrame(ttk.Frame):
    """Módulo de gestión de planes con Treeview, búsqueda y formulario."""

    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.service = PlanService()
        self.plan_seleccionado_id = None

        self._crear_widgets()
        self.refrescar()

    def _crear_widgets(self):
        """Construye la interfaz del módulo de planes."""
        # ── Panel superior: Búsqueda ─────────────────────────────────────
        frame_busqueda = ttk.LabelFrame(self, text="Buscar Planes",
                                        padding=10)
        frame_busqueda.pack(fill='x', padx=10, pady=(10, 5))

        ttk.Label(frame_busqueda, text="Buscar:").pack(side='left')
        self.entry_busqueda = ttk.Entry(frame_busqueda, width=40)
        self.entry_busqueda.pack(side='left', padx=5)
        self.entry_busqueda.bind('<KeyRelease>', lambda e: self._buscar())

        self.var_mostrar_inactivos = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame_busqueda, text="Mostrar inactivos",
            variable=self.var_mostrar_inactivos,
            command=self.refrescar
        ).pack(side='left', padx=10)

        ttk.Button(
            frame_busqueda, text="🔄 Refrescar", command=self.refrescar
        ).pack(side='right')

        # ── Panel central: Treeview ──────────────────────────────────────
        frame_tabla = ttk.Frame(self)
        frame_tabla.pack(fill='both', expand=True, padx=10, pady=5)

        columnas = ('id', 'nombre', 'duracion', 'precio', 'estado')
        self.tree = ttk.Treeview(frame_tabla, columns=columnas,
                                 show='headings', height=12)

        self.tree.heading('id', text='ID')
        self.tree.heading('nombre', text='Nombre del Plan')
        self.tree.heading('duracion', text='Duración (días)')
        self.tree.heading('precio', text='Precio ($)')
        self.tree.heading('estado', text='Estado')

        self.tree.column('id', width=40, anchor='center')
        self.tree.column('nombre', width=250)
        self.tree.column('duracion', width=120, anchor='center')
        self.tree.column('precio', width=120, anchor='e')
        self.tree.column('estado', width=80, anchor='center')

        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical',
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_seleccionar)

        # ── Panel inferior: Formulario ───────────────────────────────────
        frame_form = ttk.LabelFrame(self, text="Datos del Plan", padding=10)
        frame_form.pack(fill='x', padx=10, pady=(5, 10))

        row1 = ttk.Frame(frame_form)
        row1.pack(fill='x', pady=2)

        ttk.Label(row1, text="Nombre:").pack(side='left')
        self.entry_nombre = ttk.Entry(row1, width=30)
        self.entry_nombre.pack(side='left', padx=(5, 20))

        ttk.Label(row1, text="Duración (días):").pack(side='left')
        self.entry_duracion = ttk.Entry(row1, width=10)
        self.entry_duracion.pack(side='left', padx=(5, 20))

        ttk.Label(row1, text="Precio ($):").pack(side='left')
        self.entry_precio = ttk.Entry(row1, width=12)
        self.entry_precio.pack(side='left', padx=5)

        # Botones
        frame_botones = ttk.Frame(frame_form)
        frame_botones.pack(fill='x', pady=(10, 0))

        ttk.Button(
            frame_botones, text="➕ Agregar", command=self._agregar
        ).pack(side='left', padx=2)

        ttk.Button(
            frame_botones, text="✏️ Actualizar", command=self._actualizar
        ).pack(side='left', padx=2)

        self.btn_desactivar = ttk.Button(
            frame_botones, text="🚫 Desactivar", command=self._desactivar
        )
        self.btn_desactivar.pack(side='left', padx=2)

        self.btn_activar = ttk.Button(
            frame_botones, text="✅ Activar", command=self._activar
        )
        self.btn_activar.pack(side='left', padx=2)

        ttk.Button(
            frame_botones, text="🧹 Limpiar", command=self._limpiar_formulario
        ).pack(side='left', padx=2)

    def refrescar(self):
        """Recarga los datos del Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        solo_activos = not self.var_mostrar_inactivos.get()
        planes = self.service.listar_planes(solo_activos)

        for plan in planes:
            estado = "Activo" if plan.activo else "Inactivo"
            self.tree.insert('', 'end', values=(
                plan.id, plan.nombre, plan.duracion_dias,
                f"{plan.precio:.2f}", estado
            ))

    def _buscar(self):
        """Filtra planes según el término de búsqueda."""
        termino = self.entry_busqueda.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)

        solo_activos = not self.var_mostrar_inactivos.get()
        if termino:
            planes = self.service.buscar_planes(termino, solo_activos)
        else:
            planes = self.service.listar_planes(solo_activos)

        for plan in planes:
            estado = "Activo" if plan.activo else "Inactivo"
            self.tree.insert('', 'end', values=(
                plan.id, plan.nombre, plan.duracion_dias,
                f"{plan.precio:.2f}", estado
            ))

    def _on_seleccionar(self, event):
        """Carga los datos del plan seleccionado en el formulario."""
        seleccion = self.tree.selection()
        if not seleccion:
            return
        valores = self.tree.item(seleccion[0], 'values')
        self.plan_seleccionado_id = int(valores[0])

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[1])
        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, valores[2])
        self.entry_precio.delete(0, tk.END)
        self.entry_precio.insert(0, valores[3])

    def _agregar(self):
        """Agrega un nuevo plan."""
        try:
            duracion = int(self.entry_duracion.get())
            precio = float(self.entry_precio.get())
            self.service.crear_plan(
                nombre=self.entry_nombre.get(),
                duracion_dias=duracion,
                precio=precio
            )
            messagebox.showinfo("Éxito", "Plan creado correctamente.")
            self._limpiar_formulario()
            self.refrescar()
        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error de integridad",
                "Ya existe un plan con ese nombre."
            )

    def _actualizar(self):
        """Actualiza los datos del plan seleccionado."""
        if self.plan_seleccionado_id is None:
            messagebox.showwarning(
                "Selección", "Seleccione un plan de la tabla."
            )
            return
        try:
            duracion = int(self.entry_duracion.get())
            precio = float(self.entry_precio.get())
            self.service.actualizar_plan(
                plan_id=self.plan_seleccionado_id,
                nombre=self.entry_nombre.get(),
                duracion_dias=duracion,
                precio=precio
            )
            messagebox.showinfo("Éxito", "Plan actualizado correctamente.")
            self._limpiar_formulario()
            self.refrescar()
        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error de integridad",
                "Ya existe un plan con ese nombre."
            )

    def _desactivar(self):
        """Desactiva el plan seleccionado con confirmación."""
        if self.plan_seleccionado_id is None:
            messagebox.showwarning(
                "Selección", "Seleccione un plan de la tabla."
            )
            return
        if messagebox.askyesno(
            "Confirmar desactivación",
            "¿Está seguro de desactivar este plan?\n"
            "El plan no será eliminado, solo desactivado."
        ):
            try:
                self.service.desactivar_plan(self.plan_seleccionado_id)
                messagebox.showinfo(
                    "Éxito", "Plan desactivado correctamente."
                )
                self._limpiar_formulario()
                self.refrescar()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def _activar(self):
        """Reactiva el plan seleccionado."""
        if self.plan_seleccionado_id is None:
            messagebox.showwarning(
                "Selección", "Seleccione un plan de la tabla."
            )
            return
        try:
            self.service.activar_plan(self.plan_seleccionado_id)
            messagebox.showinfo("Éxito", "Plan activado correctamente.")
            self._limpiar_formulario()
            self.refrescar()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.plan_seleccionado_id = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_duracion.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
