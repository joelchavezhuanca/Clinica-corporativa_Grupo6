import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime

from src.ui.common import titulo, aplicar_zebra, COLOR_EXITO, COLOR_SECUNDARIO
from src.ui.cita_ui import CitaPage


class CalendarioPage:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services

    def render(self):
        titulo(
            self.parent,
            "Calendario médico",
            "Agenda diaria y visualización de citas por fecha",
        )

        cuerpo = ctk.CTkFrame(self.parent, fg_color="transparent")
        cuerpo.pack(fill="both", expand=True)

        izquierda = ctk.CTkFrame(cuerpo, fg_color="white", corner_radius=15, width=390)
        izquierda.pack(side="left", fill="y", padx=(0, 14))
        izquierda.pack_propagate(False)

        derecha = ctk.CTkFrame(cuerpo, fg_color="white", corner_radius=15)
        derecha.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            izquierda,
            text="Seleccione una fecha",
            font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 10))

        self.cal = Calendar(
            izquierda,
            selectmode="day",
            date_pattern="yyyy-mm-dd",
            locale="es_ES",
            background="#103B5D",
            foreground="white",
            headersbackground="#1E6D8F",
            headersforeground="white",
            selectbackground="#19A7A0",
            selectforeground="white",
            normalbackground="white",
            weekendbackground="#F8FAFC",
        )
        self.cal.pack(padx=18, pady=8, fill="x")
        self.cal.bind("<<CalendarSelected>>", lambda _: self.cargar())

        self.fecha_label = ctk.CTkLabel(
            derecha,
            text="",
            font=("Segoe UI", 20, "bold"),
            text_color="#103B5D",
        )
        self.fecha_label.pack(anchor="w", padx=18, pady=(18, 8))

        barra = ctk.CTkFrame(derecha, fg_color="transparent")
        barra.pack(fill="x", padx=18, pady=(0, 10))

        ctk.CTkButton(
            barra,
            text="+ Agendar cita en esta fecha",
            fg_color=COLOR_EXITO,
            command=self.nueva_cita_fecha,
        ).pack(side="right")

        self.tabla = ttk.Treeview(
            derecha,
            columns=("hora", "paciente", "medico", "especialidad", "estado"),
            show="headings",
            height=14,
        )
        aplicar_zebra(self.tabla)

        for col, txt, width in [
            ("hora", "Hora", 75),
            ("paciente", "Paciente", 190),
            ("medico", "Médico", 190),
            ("especialidad", "Especialidad", 150),
            ("estado", "Estado", 110),
        ]:
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, width=width)

        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        self.cargar()

    def cargar(self):
        fecha = self.cal.get_date()
        self.fecha_label.configure(text=f"Agenda del {fecha}")

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        pacientes = {
            p["dni"]: f'{p["nombres"]} {p["apellidos"]}'
            for p in self.services.pacientes.listar()
        }
        medicos = {
            m["cmp"]: (f'{m["nombres"]} {m["apellidos"]}', m["especialidad"])
            for m in self.services.medicos.listar()
        }

        citas = sorted(
            self.services.citas.filtrar(fecha=fecha),
            key=lambda x: x["hora"],
        )

        for i, c in enumerate(citas):
            medico, esp = medicos.get(c["cmp_medico"], (c["cmp_medico"], ""))
            self.tabla.insert(
                "",
                "end",
                values=(
                    c["hora"],
                    pacientes.get(c["dni_paciente"], c["dni_paciente"]),
                    medico,
                    esp,
                    c["estado"],
                ),
                tags=(c["estado"].lower(), "par" if i % 2 == 0 else "impar"),
            )

    def nueva_cita_fecha(self):
        fecha = self.cal.get_date()
        helper = CitaPage(self.parent, self.services)
        helper.nueva(fecha_inicial=fecha, al_guardar=self.cargar)
