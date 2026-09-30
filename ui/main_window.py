"""Ventana principal del sistema con menú y navegación por pestañas."""

import tkinter as tk
from tkinter import ttk, messagebox

from ui.socios_frame import SociosFrame
from ui.planes_frame import PlanesFrame
from ui.pagos_frame import PagosFrame
from ui.reportes_frame import ReportesFrame


class MainWindow:
    """Ventana principal con menú superior, pestañas y barra de estado."""

    def __init__(self, root, usuario):
        """
        Args:
            root: Ventana raíz de Tkinter (reutilizada tras login).
            usuario: Objeto Usuario autenticado.
        """
        self.root = root
        self.usuario = usuario

        self.root.title(
            f"Club Deportivo - {usuario.username} ({usuario.rol})"
        )

        # Maximizar ventana
        ancho, alto = 1100, 700
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.root.resizable(True, True)

        self._crear_menu()
        self._crear_pestanas()
        self._crear_barra_estado()

    def _crear_menu(self):
        """Crea el menú superior de la aplicación."""
        menubar = tk.Menu(self.root)

        # Menú Módulos
        menu_modulos = tk.Menu(menubar, tearoff=0)
        menu_modulos.add_command(
            label="Socios", command=lambda: self.notebook.select(0)
        )
        menu_modulos.add_command(
            label="Planes", command=lambda: self.notebook.select(1)
        )
        menu_modulos.add_command(
            label="Pagos / Inscripciones",
            command=lambda: self.notebook.select(2)
        )
        menu_modulos.add_command(
            label="Reportes", command=lambda: self.notebook.select(3)
        )
        menu_modulos.add_separator()
        menu_modulos.add_command(
            label="Cerrar Sesión", command=self._cerrar_sesion
        )
        menu_modulos.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Módulos", menu=menu_modulos)

        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menu_ayuda.add_command(
            label="Acerca de...", command=self._mostrar_acerca_de
        )
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)

        self.root.config(menu=menubar)

    def _crear_pestanas(self):
        """Crea el sistema de pestañas (notebook) con los módulos."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Pestaña Socios
        self.socios_frame = SociosFrame(self.notebook, self.usuario)
        self.notebook.add(self.socios_frame, text="  📋 Socios  ")

        # Pestaña Planes
        self.planes_frame = PlanesFrame(self.notebook, self.usuario)
        self.notebook.add(self.planes_frame, text="  📦 Planes  ")

        # Pestaña Pagos
        self.pagos_frame = PagosFrame(self.notebook, self.usuario)
        self.notebook.add(self.pagos_frame, text="  💳 Pagos  ")

        # Pestaña Reportes
        self.reportes_frame = ReportesFrame(self.notebook, self.usuario)
        self.notebook.add(self.reportes_frame, text="  📊 Reportes  ")

        # Refrescar datos al cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _crear_barra_estado(self):
        """Crea la barra de estado inferior."""
        self.barra_estado = ttk.Label(
            self.root,
            text=(f"  Usuario: {self.usuario.username}  |  "
                  f"Rol: {self.usuario.rol}  |  "
                  f"Club Deportivo v1.0"),
            relief='sunken',
            anchor='w',
            padding=5
        )
        self.barra_estado.pack(side='bottom', fill='x')

    def _on_tab_changed(self, event):
        """Refresca los datos al cambiar de pestaña."""
        tab_index = self.notebook.index(self.notebook.select())
        if tab_index == 0:
            self.socios_frame.refrescar()
        elif tab_index == 1:
            self.planes_frame.refrescar()
        elif tab_index == 2:
            self.pagos_frame.refrescar()
        elif tab_index == 3:
            self.reportes_frame.refrescar()

    def _cerrar_sesion(self):
        """Cierra la sesión actual y regresa al login."""
        if messagebox.askyesno("Cerrar Sesión",
                               "¿Desea cerrar la sesión actual?"):
            self.root.quit()

    @staticmethod
    def _mostrar_acerca_de():
        """Muestra información sobre la aplicación."""
        messagebox.showinfo(
            "Acerca de",
            "Club Deportivo v1.0\n\n"
            "Proyecto Final - Tópicos Avanzados de Programación\n"
            "Unidad 1 - Opción 6: Club Deportivo / Gimnasio\n\n"
            "Arquitectura en capas con Python, Tkinter y SQLite."
        )
