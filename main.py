"""
Club Deportivo - Punto de entrada de la aplicación.

Proyecto Final de Tópicos Avanzados de Programación
Unidad 1 - Opción 6: Club Deportivo / Gimnasio

Ejecutar: python main.py
"""

import sys
import os
import tkinter as tk

# Agregar el directorio raíz al path para imports absolutos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.database import init_db
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main():
    """Punto de entrada principal de la aplicación."""
    # 1. Inicializar base de datos (crear tablas y semillas si es necesario)
    print("Inicializando base de datos...")
    init_db()
    print("Base de datos lista.")

    # 2. Crear ventana raíz
    root = tk.Tk()

    def on_login_success(usuario):
        """Callback: limpia la ventana de login y abre la principal."""
        # Destruir todos los widgets del login
        for widget in root.winfo_children():
            widget.destroy()

        # Limpiar bindings del login
        root.unbind('<Return>')

        # Abrir ventana principal
        MainWindow(root, usuario)

    # 3. Mostrar ventana de login
    LoginWindow(root, on_login_success)

    # 4. Iniciar loop principal
    root.mainloop()


if __name__ == '__main__':
    main()
