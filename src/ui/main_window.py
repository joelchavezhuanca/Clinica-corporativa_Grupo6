from datetime import datetime
import customtkinter as ctk

from src.ui.common import (
    COLOR_PRIMARIO,
    COLOR_SECUNDARIO,
    COLOR_FONDO,
    COLOR_ACENTO,
    limpiar,
    configurar_estilo_treeview,
    crear_logo,
)
from src.ui.dashboard_ui import DashboardPage
from src.ui.paciente_ui import PacientePage
from src.ui.medico_ui import MedicoPage
from src.ui.cita_ui import CitaPage
from src.ui.calendario_ui import CalendarioPage
from src.ui.historia_ui import HistoriaPage
from src.ui.reportes_ui import ReportesPage


class MainWindow(ctk.CTkFrame):
    def __init__(self, master, services):
        super().__init__(master, fg_color=COLOR_FONDO)
        self.services = services
        self.pack(fill="both", expand=True)

        configurar_estilo_treeview()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._crear_sidebar()
        self._crear_contenido()
        self.mostrar("dashboard")
        self._actualizar_reloj()

    def _crear_sidebar(self):
        sidebar = ctk.CTkFrame(
            self, width=245, corner_radius=0, fg_color=COLOR_PRIMARIO
        )
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        crear_logo(sidebar, fondo=COLOR_PRIMARIO, compacto=True)

        opciones = [
            ("▣  Dashboard", "dashboard"),
            ("👤  Pacientes", "pacientes"),
            ("✚  Médicos", "medicos"),
            ("◷  Citas", "citas"),
            ("▦  Calendario", "calendario"),
            ("▤  Historias", "historias"),
            ("▥  Reportes", "reportes"),
        ]

        for texto, clave in opciones:
            ctk.CTkButton(
                sidebar,
                text=texto,
                anchor="w",
                height=46,
                fg_color="transparent",
                hover_color=COLOR_SECUNDARIO,
                font=("Segoe UI", 14),
                command=lambda c=clave: self.mostrar(c),
            ).pack(fill="x", padx=14, pady=3)

        ctk.CTkLabel(sidebar, text="", fg_color="transparent").pack(expand=True)

        perfil = ctk.CTkFrame(sidebar, fg_color="#0D314D", corner_radius=12)
        perfil.pack(fill="x", padx=14, pady=16)

        ctk.CTkLabel(
            perfil,
            text="● Administrador",
            text_color="#A7F3D0",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(
            perfil,
            text="Sesión local · Administrador",
            text_color="#C9D6E2",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=12, pady=(0, 10))

    def _crear_contenido(self):
        columna = ctk.CTkFrame(self, corner_radius=0, fg_color=COLOR_FONDO)
        columna.grid(row=0, column=1, sticky="nsew")
        columna.grid_rowconfigure(1, weight=1)
        columna.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(columna, height=72, corner_radius=0, fg_color="white")
        header.grid(row=0, column=0, sticky="ew")
        header.grid_propagate(False)

        ctk.CTkLabel(
            header,
            text="Sistema de Gestión de Citas e Historias Clínicas",
            font=("Segoe UI", 16, "bold"),
            text_color=COLOR_PRIMARIO,
        ).pack(side="left", padx=25, pady=20)

        estado = ctk.CTkFrame(header, fg_color="transparent")
        estado.pack(side="right", padx=25)

        self.reloj = ctk.CTkLabel(
            estado,
            text="",
            font=("Segoe UI", 11),
            text_color="#64748B",
        )
        self.reloj.pack(anchor="e")

        ctk.CTkLabel(
            estado,
            text="● Sistema operativo",
            text_color="#198754",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="e")

        self.contenido = ctk.CTkScrollableFrame(
            columna, fg_color=COLOR_FONDO, corner_radius=0
        )
        self.contenido.grid(
            row=1, column=0, sticky="nsew", padx=24, pady=20
        )

    def _actualizar_reloj(self):
        self.reloj.configure(
            text=datetime.now().strftime("%d/%m/%Y · %H:%M:%S")
        )
        self.after(1000, self._actualizar_reloj)

    def mostrar(self, clave):
        limpiar(self.contenido)

        if clave == "dashboard":
            DashboardPage(
                self.contenido,
                self.services,
                navegar=self.mostrar,
            ).render()
        elif clave == "pacientes":
            PacientePage(self.contenido, self.services).render()
        elif clave == "medicos":
            MedicoPage(self.contenido, self.services).render()
        elif clave == "citas":
            CitaPage(self.contenido, self.services).render()
        elif clave == "calendario":
            CalendarioPage(self.contenido, self.services).render()
        elif clave == "historias":
            HistoriaPage(self.contenido, self.services).render()
        elif clave == "reportes":
            ReportesPage(self.contenido, self.services).render()
