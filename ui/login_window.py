"""Ventana de inicio de sesión del sistema."""

import tkinter as tk
from tkinter import ttk, messagebox
from services.auth_service import AuthService


class LoginWindow:
    """Ventana de login con autenticación SHA-256."""

    def __init__(self, root, on_login_success):
        """
        Args:
            root: Ventana raíz de Tkinter.
            on_login_success: Callback que recibe el objeto Usuario autenticado.
        """
        self.root = root
        self.on_login_success = on_login_success
        self.auth_service = AuthService()

        self.root.title("Club Deportivo - Iniciar Sesión")
        self.root.resizable(False, False)

        # Centrar ventana
        ancho, alto = 400, 300
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        self._crear_widgets()

    def _crear_widgets(self):
        """Construye la interfaz del formulario de login."""
        # Frame principal
        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True, fill='both')

        # Título
        ttk.Label(
            frame, text="🏋️ Club Deportivo",
            font=('Segoe UI', 18, 'bold')
        ).pack(pady=(0, 5))

        ttk.Label(
            frame, text="Iniciar Sesión",
            font=('Segoe UI', 12)
        ).pack(pady=(0, 20))

        # Usuario
        ttk.Label(frame, text="Usuario:").pack(anchor='w')
        self.entry_usuario = ttk.Entry(frame, width=35)
        self.entry_usuario.pack(pady=(0, 10), ipady=3)
        self.entry_usuario.focus()

        # Contraseña
        ttk.Label(frame, text="Contraseña:").pack(anchor='w')
        self.entry_password = ttk.Entry(frame, width=35, show="•")
        self.entry_password.pack(pady=(0, 20), ipady=3)

        # Botón
        ttk.Button(
            frame, text="Ingresar", command=self._intentar_login
        ).pack(ipadx=20, ipady=5)

        # Bind Enter
        self.root.bind('<Return>', lambda e: self._intentar_login())

    def _intentar_login(self):
        """Valida credenciales e inicia sesión o muestra error."""
        username = self.entry_usuario.get().strip()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning(
                "Campos vacíos",
                "Por favor ingrese usuario y contraseña."
            )
            return

        usuario = self.auth_service.autenticar(username, password)

        if usuario is None:
            messagebox.showerror(
                "Error de autenticación",
                "Usuario o contraseña incorrectos, o la cuenta está "
                "desactivada."
            )
            self.entry_password.delete(0, tk.END)
            return

        # Login exitoso
        self.on_login_success(usuario)
