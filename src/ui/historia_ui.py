import customtkinter as ctk
from tkinter import ttk, messagebox
from src.ui.common import titulo, aplicar_zebra, COLOR_EXITO


class HistoriaPage:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services

    def render(self):
        titulo(
            self.parent,
            "Historias clínicas",
            "Diagnósticos, tratamientos y observaciones",
        )

        barra = ctk.CTkFrame(self.parent, fg_color="transparent")
        barra.pack(fill="x", pady=(0, 14))

        self.dni = ctk.CTkEntry(
            barra, width=320, height=40, placeholder_text="Buscar por DNI del paciente..."
        )
        self.dni.pack(side="left")
        self.dni.bind("<KeyRelease>", lambda _: self.cargar())

        ctk.CTkButton(
            barra,
            text="+ Nueva historia",
            fg_color=COLOR_EXITO,
            command=self.nueva,
        ).pack(side="right")

        self.tabla = ttk.Treeview(
            self.parent,
            columns=("fecha", "dni", "cita", "diagnostico", "tratamiento", "observaciones"),
            show="headings",
        )
        aplicar_zebra(self.tabla)

        for col, txt, width in [
            ("fecha", "Fecha", 110),
            ("dni", "DNI", 100),
            ("cita", "Cita", 110),
            ("diagnostico", "Diagnóstico", 260),
            ("tratamiento", "Tratamiento", 260),
            ("observaciones", "Observaciones", 260),
        ]:
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, width=width)

        self.tabla.pack(fill="both", expand=True)
        self.cargar()

    def cargar(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        dni = self.dni.get().strip()
        datos = (
            self.services.historias.buscar_por_dni(dni)
            if dni
            else self.services.historias.listar()
        )

        for i, h in enumerate(datos):
            self.tabla.insert(
                "",
                "end",
                values=(
                    h["fecha"],
                    h["dni_paciente"],
                    h["cita_id"],
                    h["diagnostico"],
                    h["tratamiento"],
                    h["observaciones"],
                ),
                tags=("par" if i % 2 == 0 else "impar",),
            )

    def nueva(self):
        historias = self.services.historias.listar()
        usados = {h["cita_id"] for h in historias}
        citas = [
            c for c in self.services.citas.listar()
            if c["estado"] == "ATENDIDA" and c["id"] not in usados
        ]

        if not citas:
            messagebox.showwarning(
                "Sin citas disponibles",
                "No existen citas ATENDIDAS pendientes de historia clínica.",
            )
            return

        win = ctk.CTkToplevel(self.parent)
        win.title("Nueva historia clínica")
        win.geometry("650x670")
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="Registrar historia clínica",
            font=("Segoe UI", 24, "bold"),
        ).pack(pady=(25, 15))

        opciones = [
            f'{c["id"]} | DNI {c["dni_paciente"]} | {c["fecha"]} {c["hora"]}'
            for c in citas
        ]
        mapa = {op: op.split("|")[0].strip() for op in opciones}

        cita = ctk.CTkComboBox(win, values=opciones, width=540, height=42)
        cita.pack(pady=8)
        cita.set(opciones[0])

        diagnostico = ctk.CTkTextbox(win, width=540, height=120)
        diagnostico.pack(pady=8)
        diagnostico.insert("1.0", "Diagnóstico")

        tratamiento = ctk.CTkTextbox(win, width=540, height=110)
        tratamiento.pack(pady=8)
        tratamiento.insert("1.0", "Tratamiento")

        observaciones = ctk.CTkTextbox(win, width=540, height=100)
        observaciones.pack(pady=8)
        observaciones.insert("1.0", "Observaciones")

        def guardar():
            try:
                self.services.historias.registrar(
                    mapa[cita.get()],
                    diagnostico.get("1.0", "end").strip(),
                    tratamiento.get("1.0", "end").strip(),
                    observaciones.get("1.0", "end").strip(),
                )
                messagebox.showinfo("Correcto", "Historia clínica registrada.")
                win.destroy()
                self.cargar()
            except Exception as exc:
                messagebox.showerror("No se pudo registrar", str(exc))

        ctk.CTkButton(
            win,
            text="Guardar historia",
            width=540,
            height=45,
            fg_color=COLOR_EXITO,
            command=guardar,
        ).pack(pady=20)
