# 🏋️ Club Deportivo - Sistema de Gestión

**Proyecto Final de Tópicos Avanzados de Programación**
**Unidad 1 - Opción 6: Club Deportivo / Gimnasio**

---

## 📝 Descripción

Sistema de escritorio para la gestión integral de un club deportivo/gimnasio, desarrollado con **Python**, **Tkinter** y **SQLite**. Permite administrar socios, planes de membresía, pagos/inscripciones y generar reportes con exportación a CSV.

El proyecto implementa una **arquitectura en capas** (Modelos → Repositorios → Servicios → UI) que garantiza la separación de responsabilidades y la mantenibilidad del código.

---

## ⚙️ Requisitos de Ejecución

- **Python 3.10** o superior
- **Tkinter** (incluido por defecto con Python en la mayoría de distribuciones)
- **SQLite3** (incluido con Python)
- No se requieren dependencias externas adicionales

---

## 🚀 Guía de Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd mi_club_deportivo
```

### 2. (Opcional) Crear entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Ejecutar la aplicación

```bash
python main.py
```

Al ejecutarse por primera vez, la aplicación creará automáticamente la base de datos `club_deportivo.db` con tablas y datos de prueba.

---

## 🔑 Credenciales de Prueba

| Usuario      | Contraseña     | Rol             |
|-------------|----------------|-----------------|
| `admin`     | `admin123`     | Administrador   |
| `operador1` | `operador123`  | Operador        |

> Las contraseñas se almacenan cifradas con **SHA-256** (hashlib). Nunca se guardan en texto plano.

---

## 🗄️ Modelo de Datos

La base de datos SQLite contiene 4 tablas relacionadas:

### `usuarios_sistema`
Almacena las cuentas de acceso al sistema.

| Campo           | Tipo    | Restricción                                  |
|----------------|---------|----------------------------------------------|
| `id`           | INTEGER | PRIMARY KEY AUTOINCREMENT                    |
| `username`     | TEXT    | UNIQUE NOT NULL                              |
| `password_hash`| TEXT    | NOT NULL (SHA-256)                           |
| `rol`          | TEXT    | CHECK('administrador', 'operador') NOT NULL  |
| `activo`       | INTEGER | DEFAULT 1                                    |

### `socios`
Registro de miembros del club deportivo.

| Campo      | Tipo    | Restricción              |
|-----------|---------|--------------------------|
| `id`      | INTEGER | PRIMARY KEY AUTOINCREMENT|
| `folio`   | TEXT    | UNIQUE NOT NULL          |
| `nombre`  | TEXT    | NOT NULL                 |
| `telefono`| TEXT    |                          |
| `correo`  | TEXT    | UNIQUE NOT NULL          |
| `activo`  | INTEGER | DEFAULT 1                |

### `planes`
Planes de membresía disponibles en el club.

| Campo           | Tipo    | Restricción                       |
|----------------|---------|-----------------------------------|
| `id`           | INTEGER | PRIMARY KEY AUTOINCREMENT         |
| `nombre`       | TEXT    | UNIQUE NOT NULL                   |
| `duracion_dias`| INTEGER | NOT NULL, CHECK(duracion_dias > 0)|
| `precio`       | REAL    | NOT NULL, CHECK(precio >= 0)      |
| `activo`       | INTEGER | DEFAULT 1                         |

### `pagos`
Historial de pagos e inscripciones.

| Campo            | Tipo    | Restricción                 |
|-----------------|---------|-----------------------------|
| `id`            | INTEGER | PRIMARY KEY AUTOINCREMENT   |
| `socio_id`      | INTEGER | FK → socios(id), NOT NULL   |
| `plan_id`       | INTEGER | FK → planes(id), NOT NULL   |
| `fecha_pago`    | TEXT    | NOT NULL (YYYY-MM-DD)       |
| `vigencia_hasta`| TEXT    | NOT NULL (YYYY-MM-DD)       |
| `monto`         | REAL    | NOT NULL                    |

### Relaciones

```
usuarios_sistema (independiente)

socios ──┐
         ├── pagos (socio_id FK, plan_id FK)
planes ──┘
```

---

## 📁 Estructura de Carpetas

```
mi_club_deportivo/
│
├── main.py                    # Punto de entrada de la aplicación
├── README.md                  # Esta documentación
├── .gitignore                 # Archivos ignorados por Git
├── requirements.txt           # Dependencias del proyecto
│
├── db/
│   └── database.py            # Conexión SQLite, DDL y datos semilla
│
├── models/                    # Clases de dominio (POO pura)
│   ├── usuario.py             # Modelo Usuario
│   ├── socio.py               # Modelo Socio
│   ├── plan.py                # Modelo Plan
│   └── pago.py                # Modelo Pago
│
├── repositories/              # Capa de persistencia (SQL + mapeo)
│   ├── usuario_repository.py  # CRUD usuarios
│   ├── socio_repository.py    # CRUD socios
│   ├── plan_repository.py     # CRUD planes
│   └── pago_repository.py     # CRUD pagos + JOINs
│
├── services/                  # Reglas de negocio y validaciones
│   ├── auth_service.py        # Autenticación SHA-256
│   ├── socio_service.py       # Lógica de socios
│   ├── plan_service.py        # Lógica de planes
│   └── pago_service.py        # Lógica de pagos, vigencia, CSV
│
└── ui/                        # Interfaz Gráfica (Tkinter/ttk)
    ├── login_window.py        # Ventana de Login
    ├── main_window.py         # Ventana principal con menú
    ├── socios_frame.py        # CRUD de Socios
    ├── planes_frame.py        # CRUD de Planes
    ├── pagos_frame.py         # Alta de pagos/inscripciones
    └── reportes_frame.py      # Reportes y exportación CSV
```

---

## 🔧 Reglas de Negocio Implementadas

1. **Contraseñas seguras:** Cifrado SHA-256 con `hashlib`. Nunca se almacenan en texto plano.
2. **Cálculo de vigencia:** `vigencia_hasta = fecha_pago + duracion_dias`. Si el socio ya tiene membresía activa, se suma desde la fecha de vencimiento actual.
3. **Validaciones:**
   - No se permite vender planes inactivos.
   - No se permite registrar pagos a socios inactivos.
   - Campos obligatorios validados antes de guardar.
4. **Desactivación lógica:** Los socios y planes nunca se eliminan físicamente (`DELETE`), se desactivan (`activo = 0`).
5. **Separación estricta de capas:** La UI solo interactúa con servicios; los repositorios manejan exclusivamente SQL.

---

## 📊 Datos de Prueba (Seeders)

La aplicación carga automáticamente en la primera ejecución:
- **2 usuarios** del sistema (admin + operador)
- **8 socios** (7 activos, 1 inactivo)
- **5 planes** de membresía (Diario, Mensual, Trimestral, Anual, VIP)
- **3 pagos** de ejemplo:
  - 1 vigente
  - 1 vencido
  - 1 por vencer en los próximos 7 días

---

## 📄 Licencia

Proyecto académico - Uso educativo.
