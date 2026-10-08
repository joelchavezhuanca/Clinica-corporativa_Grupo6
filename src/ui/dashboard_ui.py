import customtkinter as ctk
from tkinter import ttk
from datetime import date
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.ui.common import (
    titulo,
    card,
    aplicar_zebra,
    COLOR_PRIMARIO,
    COLOR_SECUNDARIO,
    COLOR_EXITO,
    COLOR_ALERTA,
    COLOR_PELIGRO,
    COLOR_CARD,
)


class DashboardPage:
    def __init__(self, parent, services, navegar=None):
        self.parent = parent
        self.services = services
        self.navegar = navegar

    def render(self):
        titulo(
            self.parent,
            "Dashboard",
            "Resumen operativo y actividad clínica del día",
        )

        pacientes = self.services.pacientes.listar()
        medicos = self.services.medicos.listar()
        citas = self.services.citas.listar()
        historias = self.services.historias.listar()
        hoy = date.today().isoformat()
        citas_hoy = [c for c in citas if c["fecha"] == hoy]

        tarjetas = ctk.CTkFrame(self.parent, fg_color="transparent")
        tarjetas.pack(fill="x", pady=(0, 20))

        card(tarjetas, "Pacientes", len(pacientes), "Registrados", "#0D6EFD")
        card(tarjetas, "Médicos", len(medicos), "Profesionales activos", COLOR_EXITO)
        card(tarjetas, "Citas de hoy", len(citas_hoy), hoy, COLOR_ALERTA)
        card(tarjetas, "Historias", len(historias), "Registros clínicos", "#7C3AED")

        cuerpo = ctk.CTkFrame(self.parent, fg_color="transparent")
        cuerpo.pack(fill="x", pady=(0, 18))

        estado = ctk.CTkFrame(cuerpo, fg_color=COLOR_CARD, corner_radius=15)
        estado.pack(side="left", fill="both", expand=True, padx=(0, 12))

        ctk.CTkLabel(
            estado,
            text="Estado de atención de hoy",
            font=("Segoe UI", 18, "bold"),
            text_color=COLOR_PRIMARIO,
        ).pack(anchor="w", padx=18, pady=(16, 5))

        programadas = sum(c["estado"] == "PROGRAMADA" for c in citas_hoy)
        atendidas = sum(c["estado"] == "ATENDIDA" for c in citas_hoy)
        canceladas = sum(c["estado"] == "CANCELADA" for c in citas_hoy)

        fila_estado = ctk.CTkFrame(estado, fg_color="transparent")
        fila_estado.pack(fill="x", padx=18, pady=(6, 14))

        for nombre, valor, color in [
            ("Programadas", programadas, "#0D6EFD"),
            ("Atendidas", atendidas, COLOR_EXITO),
            ("Canceladas", canceladas, COLOR_PELIGRO),
        ]:
            bloque = ctk.CTkFrame(fila_estado, fg_color="#F8FAFC", corner_radius=12, height=85)
            bloque.pack(side="left", expand=True, fill="x", padx=(0, 8))
            bloque.pack_propagate(False)
            ctk.CTkLabel(bloque, text=nombre, text_color="#64748B").pack(pady=(13, 2))
            ctk.CTkLabel(
                bloque, text=str(valor), font=("Segoe UI", 25, "bold"), text_color=color
            ).pack()

        grafico = ctk.CTkFrame(cuerpo, fg_color=COLOR_CARD, corner_radius=15, width=420)
        grafico.pack(side="left", fill="both")
        grafico.pack_propagate(False)

        ctk.CTkLabel(
            grafico,
            text="Distribución de citas",
            font=("Segoe UI", 18, "bold"),
            text_color=COLOR_PRIMARIO,
        ).pack(anchor="w", padx=18, pady=(16, 0))

        self._crear_grafico(grafico, citas)

        acciones = ctk.CTkFrame(self.parent, fg_color="transparent")
        acciones.pack(fill="x", pady=(0, 18))

        ctk.CTkLabel(
            acciones,
            text="Acciones rápidas",
            font=("Segoe UI", 18, "bold"),
            text_color=COLOR_PRIMARIO,
        ).pack(side="left", padx=(0, 15))

        botones = [
            ("+ Nueva cita", "citas", COLOR_EXITO),
            ("Ver calendario", "calendario", COLOR_SECUNDARIO),
            ("Pacientes", "pacientes", "#0D6EFD"),
            ("Historias", "historias", "#7C3AED"),
        ]
        for texto, destino, color in botones:
            ctk.CTkButton(
                acciones,
                text=texto,
                height=38,
                fg_color=color,
                command=lambda d=destino: self.navegar(d) if self.navegar else None,
            ).pack(side="left", padx=4)

        ctk.CTkLabel(
            self.parent,
            text="Próximas citas",
            font=("Segoe UI", 19, "bold"),
            text_color=COLOR_PRIMARIO,
        ).pack(anchor="w", pady=(4, 10))

        tabla = ttk.Treeview(
            self.parent,
            columns=("fecha", "hora", "paciente", "medico", "especialidad", "estado"),
            show="headings",
            height=10,
        )
        aplicar_zebra(tabla)

        for col, txt, width in [
            ("fecha", "Fecha", 110),
            ("hora", "Hora", 80),
            ("paciente", "Paciente", 220),
            ("medico", "Médico", 220),
            ("especialidad", "Especialidad", 170),
            ("estado", "Estado", 120),
        ]:
            tabla.heading(col, text=txt)
            tabla.column(col, width=width, anchor="center" if col in ("fecha", "hora", "estado") else "w")

        pacientes_map = {
            p["dni"]: f'{p["nombres"]} {p["apellidos"]}'
            for p in pacientes
        }
        medicos_map = {
            m["cmp"]: (f'{m["nombres"]} {m["apellidos"]}', m["especialidad"])
            for m in medicos
        }

        proximas = sorted(
            [c for c in citas if c["estado"] != "CANCELADA"],
            key=lambda x: (x["fecha"], x["hora"]),
        )[:12]

        for i, c in enumerate(proximas):
            medico, esp = medicos_map.get(c["cmp_medico"], (c["cmp_medico"], ""))
            estado_tag = c["estado"].lower()
            tabla.insert(
                "",
                "end",
                values=(
                    c["fecha"],
                    c["hora"],
                    pacientes_map.get(c["dni_paciente"], c["dni_paciente"]),
                    medico,
                    esp,
                    c["estado"],
                ),
                tags=(estado_tag, "par" if i % 2 == 0 else "impar"),
            )

        tabla.pack(fill="both", expand=True)

    def _crear_grafico(self, parent, citas):
        programadas = sum(c["estado"] == "PROGRAMADA" for c in citas)
        atendidas = sum(c["estado"] == "ATENDIDA" for c in citas)
        canceladas = sum(c["estado"] == "CANCELADA" for c in citas)

        fig = Figure(figsize=(4.1, 2.2), dpi=90, facecolor="white")
        ax = fig.add_subplot(111)
        categorias = ["Programadas", "Atendidas", "Canceladas"]
        valores = [programadas, atendidas, canceladas]
        colores = ["#0D6EFD", "#198754", "#C0392B"]

        ax.bar(categorias, valores, color=colores, width=0.55)
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", alpha=0.15)
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=(0, 8))
