import customtkinter as ctk
from tkinter import ttk, messagebox
from src.ui.common import titulo, aplicar_zebra, COLOR_EXITO


class MedicoPage:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services

    def render(self):
        titulo(self.parent, "Médicos", "Profesionales, CMP y especialidades")

        barra = ctk.CTkFrame(self.parent, fg_color="transparent")
        barra.pack(fill="x", pady=(0, 14))

        self.busqueda = ctk.CTkEntry(
            barra, width=430, height=40, placeholder_text="Buscar por CMP, nombre o especialidad..."
        )
        self.busqueda.pack(side="left")
        self.busqueda.bind("<KeyRelease>", lambda _: self.cargar())

        ctk.CTkButton(
            barra, text="+ Nuevo médico", fg_color=COLOR_EXITO, height=40, command=self.nuevo
        ).pack(side="right")

        self.contador = ctk.CTkLabel(barra, text="", text_color="#64748B")
        self.contador.pack(side="right", padx=16)

        self.tabla = ttk.Treeview(
            self.parent,
            columns=("cmp", "medico", "especialidad", "telefono"),
            show="headings",
        )
        aplicar_zebra(self.tabla)

        for col, txt, width in [
            ("cmp", "CMP", 120),
            ("medico", "Médico", 280),
            ("especialidad", "Especialidad", 230),
            ("telefono", "Teléfono", 150),
        ]:
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, width=width)

        self.tabla.pack(fill="both", expand=True)
        self.cargar()

    def cargar(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        datos = self.services.medicos.buscar(self.busqueda.get())
        self.contador.configure(text=f"{len(datos)} profesional(es)")

        for i, m in enumerate(datos):
            self.tabla.insert(
                "",
                "end",
                values=(
                    m["cmp"],
                    f'{m["nombres"]} {m["apellidos"]}',
                    m["especialidad"],
                    m["telefono"],
                ),
                tags=("par" if i % 2 == 0 else "impar",),
            )

    def nuevo(self):
        win = ctk.CTkToplevel(self.parent)
        win.title("Nuevo médico")
        win.geometry("520x540")
        win.grab_set()

        ctk.CTkLabel(win, text="Registrar médico", font=("Segoe UI", 24, "bold")).pack(
            pady=(25, 15)
        )

        campos = {}
        for clave, placeholder in [
            ("cmp", "CMP"),
            ("nombres", "Nombres"),
            ("apellidos", "Apellidos"),
            ("especialidad", "Especialidad"),
            ("telefono", "Teléfono"),
        ]:
            entrada = ctk.CTkEntry(win, width=400, height=42, placeholder_text=placeholder)
            entrada.pack(pady=7)
            campos[clave] = entrada

        def guardar():
            try:
                self.services.medicos.registrar(
                    campos["cmp"].get(),
                    campos["nombres"].get(),
                    campos["apellidos"].get(),
                    campos["especialidad"].get(),
                    campos["telefono"].get(),
                )
                messagebox.showinfo("Correcto", "Médico registrado.")
                win.destroy()
                self.cargar()
            except Exception as exc:
                messagebox.showerror("No se pudo registrar", str(exc))

        ctk.CTkButton(
            win,
            text="Guardar médico",
            width=400,
            height=45,
            fg_color=COLOR_EXITO,
            command=guardar,
        ).pack(pady=24)
