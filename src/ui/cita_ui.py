import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date
from src.ui.common import (
    titulo,
    aplicar_zebra,
    COLOR_EXITO,
    COLOR_PELIGRO,
    COLOR_SECUNDARIO,
)


class CitaPage:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services

    def render(self):
        titulo(self.parent, "Citas médicas", "Agenda, atención y cancelación")

        barra = ctk.CTkFrame(self.parent, fg_color="transparent")
        barra.pack(fill="x", pady=(0, 12))

        self.buscar = ctk.CTkEntry(
            barra,
            width=310,
            height=40,
            placeholder_text="Buscar DNI, CMP, fecha o ID...",
        )
        self.buscar.pack(side="left")
        self.buscar.bind("<KeyRelease>", lambda _: self.cargar())

        self.estado = ctk.CTkComboBox(
            barra,
            values=["TODOS", "PROGRAMADA", "ATENDIDA", "CANCELADA"],
            width=165,
            command=lambda _: self.cargar(),
        )
        self.estado.set("TODOS")
        self.estado.pack(side="left", padx=10)

        ctk.CTkButton(
            barra,
            text="+ Nueva cita",
            fg_color=COLOR_EXITO,
            height=40,
            command=self.nueva,
        ).pack(side="right")

        acciones = ctk.CTkFrame(self.parent, fg_color="transparent")
        acciones.pack(fill="x", pady=(0, 12))

        ctk.CTkButton(
            acciones,
            text="✓ Marcar ATENDIDA",
            fg_color=COLOR_EXITO,
            command=lambda: self.cambiar("ATENDIDA"),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            acciones,
            text="↺ Volver a PROGRAMADA",
            fg_color=COLOR_SECUNDARIO,
            command=lambda: self.cambiar("PROGRAMADA"),
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            acciones,
            text="✕ Cancelar cita",
            fg_color=COLOR_PELIGRO,
            command=lambda: self.cambiar("CANCELADA"),
        ).pack(side="left")

        self.tabla = ttk.Treeview(
            self.parent,
            columns=("id", "fecha", "hora", "paciente", "medico", "especialidad", "estado"),
            show="headings",
        )
        aplicar_zebra(self.tabla)

        for col, txt, width in [
            ("id", "ID", 110),
            ("fecha", "Fecha", 105),
            ("hora", "Hora", 75),
            ("paciente", "Paciente", 210),
            ("medico", "Médico", 210),
            ("especialidad", "Especialidad", 160),
            ("estado", "Estado", 120),
        ]:
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, width=width)

        self.tabla.pack(fill="both", expand=True)
        self.cargar()

    def cargar(self):
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

        datos = self.services.citas.filtrar(self.buscar.get(), self.estado.get())
        datos = sorted(datos, key=lambda x: (x["fecha"], x["hora"]))

        for i, c in enumerate(datos):
            medico, esp = medicos.get(c["cmp_medico"], (c["cmp_medico"], ""))
            self.tabla.insert(
                "",
                "end",
                values=(
                    c["id"],
                    c["fecha"],
                    c["hora"],
                    pacientes.get(c["dni_paciente"], c["dni_paciente"]),
                    medico,
                    esp,
                    c["estado"],
                ),
                tags=(c["estado"].lower(), "par" if i % 2 == 0 else "impar"),
            )

    def seleccion_id(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Seleccione una cita", "Seleccione una fila de la tabla.")
            return None
        return self.tabla.item(sel[0], "values")[0]

    def cambiar(self, estado):
        cita_id = self.seleccion_id()
        if not cita_id:
            return

        try:
            self.services.citas.cambiar_estado(cita_id, estado)
            self.cargar()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def nueva(self, fecha_inicial=None, al_guardar=None):
        pacientes = self.services.pacientes.listar()
        medicos = self.services.medicos.listar()

        if not pacientes or not medicos:
            messagebox.showwarning(
                "Datos requeridos",
                "Primero debe registrar al menos un paciente y un médico.",
            )
            return

        win = ctk.CTkToplevel(self.parent)
        win.title("Nueva cita")
        win.geometry("590x600")
        win.grab_set()

        ctk.CTkLabel(win, text="Programar cita", font=("Segoe UI", 24, "bold")).pack(
            pady=(25, 15)
        )

        mapa_p = {
            f'{p["dni"]} - {p["nombres"]} {p["apellidos"]}': p["dni"]
            for p in pacientes
        }
        mapa_m = {
            f'{m["cmp"]} - {m["nombres"]} {m["apellidos"]} · {m["especialidad"]}': m["cmp"]
            for m in medicos
        }

        cb_p = ctk.CTkComboBox(win, values=list(mapa_p.keys()), width=480, height=42)
        cb_p.pack(pady=8)
        cb_p.set(list(mapa_p.keys())[0])

        cb_m = ctk.CTkComboBox(win, values=list(mapa_m.keys()), width=480, height=42)
        cb_m.pack(pady=8)
        cb_m.set(list(mapa_m.keys())[0])

        fecha = ctk.CTkEntry(win, width=480, height=42, placeholder_text="Fecha YYYY-MM-DD")
        fecha.pack(pady=8)
        fecha.insert(0, fecha_inicial or date.today().isoformat())

        hora = ctk.CTkEntry(win, width=480, height=42, placeholder_text="Hora HH:MM")
        hora.pack(pady=8)
        hora.insert(0, "09:00")

        ctk.CTkLabel(
            win,
            text="El sistema valida automáticamente cruces de horario del médico y del paciente.",
            text_color="#64748B",
            wraplength=470,
        ).pack(pady=(8, 4))

        def guardar():
            try:
                self.services.citas.programar(
                    mapa_p[cb_p.get()],
                    mapa_m[cb_m.get()],
                    fecha.get().strip(),
                    hora.get().strip(),
                )
                messagebox.showinfo("Correcto", "Cita programada correctamente.")
                win.destroy()
                if al_guardar is not None:
                    al_guardar()
                elif hasattr(self, "tabla"):
                        self.cargar()
            except Exception as exc:
                messagebox.showerror("No se pudo programar", str(exc))

        ctk.CTkButton(
            win,
            text="Guardar cita",
            width=480,
            height=45,
            fg_color=COLOR_EXITO,
            command=guardar,
        ).pack(pady=24)
