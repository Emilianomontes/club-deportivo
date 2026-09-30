"""Frame CRUD para la gestión de socios del club."""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

from services.socio_service import SocioService


class SociosFrame(ttk.Frame):
    """Módulo de gestión de socios con Treeview, búsqueda y formulario."""

    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.service = SocioService()
        self.socio_seleccionado_id = None

        self._crear_widgets()
        self.refrescar()

    def _crear_widgets(self):
        """Construye la interfaz del módulo de socios."""
        # ── Panel superior: Búsqueda ─────────────────────────────────────
        frame_busqueda = ttk.LabelFrame(self, text="Buscar Socios",
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

        columnas = ('id', 'folio', 'nombre', 'telefono', 'correo', 'estado')
        self.tree = ttk.Treeview(frame_tabla, columns=columnas,
                                 show='headings', height=12)

        self.tree.heading('id', text='ID')
        self.tree.heading('folio', text='Folio')
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('telefono', text='Teléfono')
        self.tree.heading('correo', text='Correo')
        self.tree.heading('estado', text='Estado')

        self.tree.column('id', width=40, anchor='center')
        self.tree.column('folio', width=70, anchor='center')
        self.tree.column('nombre', width=200)
        self.tree.column('telefono', width=120, anchor='center')
        self.tree.column('correo', width=220)
        self.tree.column('estado', width=80, anchor='center')

        scrollbar = ttk.Scrollbar(frame_tabla, orient='vertical',
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<<TreeviewSelect>>', self._on_seleccionar)

        # ── Panel inferior: Formulario ───────────────────────────────────
        frame_form = ttk.LabelFrame(self, text="Datos del Socio", padding=10)
        frame_form.pack(fill='x', padx=10, pady=(5, 10))

        # Fila 1
        row1 = ttk.Frame(frame_form)
        row1.pack(fill='x', pady=2)

        ttk.Label(row1, text="Folio:").pack(side='left')
        self.entry_folio = ttk.Entry(row1, width=15)
        self.entry_folio.pack(side='left', padx=(5, 20))

        ttk.Label(row1, text="Nombre:").pack(side='left')
        self.entry_nombre = ttk.Entry(row1, width=30)
        self.entry_nombre.pack(side='left', padx=5)

        # Fila 2
        row2 = ttk.Frame(frame_form)
        row2.pack(fill='x', pady=2)

        ttk.Label(row2, text="Teléfono:").pack(side='left')
        self.entry_telefono = ttk.Entry(row2, width=15)
        self.entry_telefono.pack(side='left', padx=(5, 20))

        ttk.Label(row2, text="Correo:").pack(side='left')
        self.entry_correo = ttk.Entry(row2, width=30)
        self.entry_correo.pack(side='left', padx=5)

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

        ttk.Button(
            frame_botones, text="📋 Auto-Folio", command=self._auto_folio
        ).pack(side='right', padx=2)

    def refrescar(self):
        """Recarga los datos del Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        solo_activos = not self.var_mostrar_inactivos.get()
        socios = self.service.listar_socios(solo_activos)

        for socio in socios:
            estado = "Activo" if socio.activo else "Inactivo"
            self.tree.insert('', 'end', values=(
                socio.id, socio.folio, socio.nombre,
                socio.telefono, socio.correo, estado
            ))

    def _buscar(self):
        """Filtra socios según el término de búsqueda."""
        termino = self.entry_busqueda.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)

        solo_activos = not self.var_mostrar_inactivos.get()
        if termino:
            socios = self.service.buscar_socios(termino, solo_activos)
        else:
            socios = self.service.listar_socios(solo_activos)

        for socio in socios:
            estado = "Activo" if socio.activo else "Inactivo"
            self.tree.insert('', 'end', values=(
                socio.id, socio.folio, socio.nombre,
                socio.telefono, socio.correo, estado
            ))

    def _on_seleccionar(self, event):
        """Carga los datos del socio seleccionado en el formulario."""
        seleccion = self.tree.selection()
        if not seleccion:
            return
        valores = self.tree.item(seleccion[0], 'values')
        self.socio_seleccionado_id = int(valores[0])

        self.entry_folio.delete(0, tk.END)
        self.entry_folio.insert(0, valores[1])
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, valores[2])
        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, valores[3])
        self.entry_correo.delete(0, tk.END)
        self.entry_correo.insert(0, valores[4])

    def _agregar(self):
        """Agrega un nuevo socio."""
        try:
            self.service.crear_socio(
                folio=self.entry_folio.get(),
                nombre=self.entry_nombre.get(),
                telefono=self.entry_telefono.get(),
                correo=self.entry_correo.get()
            )
            messagebox.showinfo("Éxito", "Socio registrado correctamente.")
            self._limpiar_formulario()
            self.refrescar()
        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error de integridad",
                "El folio o correo ya existe en el sistema."
            )

    def _actualizar(self):
        """Actualiza los datos del socio seleccionado."""
        if self.socio_seleccionado_id is None:
            messagebox.showwarning(
                "Selección", "Seleccione un socio de la tabla."
            )
            return
        try:
            self.service.actualizar_socio(
                socio_id=self.socio_seleccionado_id,
                folio=self.entry_folio.get(),
                nombre=self.entry_nombre.get(),
                telefono=self.entry_telefono.get(),
                correo=self.entry_correo.get()
            )
            messagebox.showinfo("Éxito", "Socio actualizado correctamente.")
            self._limpiar_formulario()
            self.refrescar()
        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error de integridad",
                "El folio o correo ya existe en el sistema."
            )

    def _desactivar(self):
        """Desactiva el socio seleccionado con confirmación."""
        if self.socio_seleccionado_id is None:
            messagebox.showwarning(
                "Selección", "Seleccione un socio de la tabla."
            )
            return
        if messagebox.askyesno(
            "Confirmar desactivación",
            "¿Está seguro de desactivar este socio?\n"
            "El socio no será eliminado, solo desactivado."
        ):
            try:
                self.service.desactivar_socio(self.socio_seleccionado_id)
                messagebox.showinfo(
                    "Éxito", "Socio desactivado correctamente."
                )
                self._limpiar_formulario()
                self.refrescar()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def _activar(self):
        """Reactiva el socio seleccionado."""
        if self.socio_seleccionado_id is None:
            messagebox.showwarning(
                "Selección", "Seleccione un socio de la tabla."
            )
            return
        try:
            self.service.activar_socio(self.socio_seleccionado_id)
            messagebox.showinfo("Éxito", "Socio activado correctamente.")
            self._limpiar_formulario()
            self.refrescar()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        self.socio_seleccionado_id = None
        self.entry_folio.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)

    def _auto_folio(self):
        """Genera automáticamente el siguiente folio disponible."""
        folio = self.service.generar_folio()
        self.entry_folio.delete(0, tk.END)
        self.entry_folio.insert(0, folio)
