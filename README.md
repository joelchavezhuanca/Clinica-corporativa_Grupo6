# Clínica Salud Integral — Sistema de Gestión Clínica

Aplicación de escritorio **100% Python** con interfaz corporativa y arquitectura por capas.

## Mejoras incluidas

1. Datos demo automáticos para que el sistema no aparezca vacío.
2. Dashboard corporativo con indicadores y accesos rápidos.
3. Tablas mejoradas con búsqueda, filtros y estados.
4. Logo generado por código Python (sin imágenes externas).
5. Gráficos estadísticos integrados con Matplotlib.
6. Calendario médico interactivo con citas por fecha.

## Módulos

- Inicio de sesión.
- Dashboard.
- Pacientes.
- Médicos.
- Citas.
- Calendario médico.
- Historias clínicas.
- Reportes.
- Exportación CSV.
- Persistencia JSON.
- Pruebas unitarias.

## Credenciales de demostración

- Usuario: `admin`
- Contraseña: `admin123`

## Instalación

En PowerShell, dentro de la carpeta del proyecto:

```powershell
py -m pip install -r requirements.txt
```

## Ejecución

```powershell
py main.py
```

## Pruebas

```powershell
py -m unittest discover -s tests -v
```

## Estructura

```text
clinica_corporativa_realista/
├── main.py
├── requirements.txt
├── README.md
├── data/
├── docs/
├── src/
│   ├── domain/
│   ├── services/
│   └── ui/
└── tests/
```

Todo el código, incluidos estilos, logo, gráficos y calendario, está implementado desde Python.
