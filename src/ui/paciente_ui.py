import customtkinter as ctk
from tkinter import ttk, messagebox
from src.ui.common import titulo, aplicar_zebra, COLOR_EXITO


class PacientePage:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services

    def render(self):
        titulo(self.parent, "Pacientes", "Gestión del padrón de pacientes")

        barra = ctk.CTkFrame(self.parent, fg_color="transparent")
        barra.pack(fill="x", pady=(0, 14))

        self.busqueda = ctk.CTkEntry(
            barra,
            width=430,
            height=40,
            placeholder_text="Buscar por DNI, nombre o apellido...",
        )
        self.busqueda.pack(side="left")
        self.busqueda.bind("<KeyRelease>", lambda _: self.cargar())

        ctk.CTkButton(
            barra,
            text="+ Nuevo paciente",
            fg_color=COLOR_EXITO,
            height=40,
            command=self.nuevo,
        ).pack(side="right")

        self.contador = ctk.CTkLabel(barra, text="", text_color="#64748B")
        self.contador.pack(side="right", padx=16)

        self.tabla = ttk.Treeview(
            self.parent,
            columns=("dni", "paciente", "telefono", "nacimiento", "direccion"),
            show="headings",
        )
        aplicar_zebra(self.tabla)
        for col, txt, width in [
            ("dni", "DNI", 100),
            ("paciente", "Paciente", 250),
            ("telefono", "Teléfono", 130),
            ("nacimiento", "F. nacimiento", 130),
            ("direccion", "Dirección", 320),
        ]:
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, width=width)

        self.tabla.pack(fill="both", expand=True)
        self.cargar()

    def cargar(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        datos = self.services.pacientes.buscar(self.busqueda.get())
        self.contador.configure(text=f"{len(datos)} registro(s)")

        for i, p in enumerate(datos):
            self.tabla.insert(
                "",
                "end",
                values=(
                    p["dni"],
                    f'{p["nombres"]} {p["apellidos"]}',
                    p["telefono"],
                    p["fecha_nacimiento"],
                    p["direccion"],
                ),
                tags=("par" if i % 2 == 0 else "impar",),
            )

    def nuevo(self):
        win = ctk.CTkToplevel(self.parent)
        win.title("Nuevo paciente")
        win.geometry("540x610")
        win.grab_set()

        ctk.CTkLabel(
            win, text="Registrar paciente", font=("Segoe UI", 24, "bold")
        ).pack(pady=(25, 15))

        campos = {}
        for clave, placeholder in [
            ("dni", "DNI (8 dígitos)"),
            ("nombres", "Nombres"),
            ("apellidos", "Apellidos"),
            ("telefono", "Teléfono"),
            ("fecha_nacimiento", "Fecha nacimiento YYYY-MM-DD"),
            ("direccion", "Dirección"),
        ]:
            entrada = ctk.CTkEntry(win, width=420, height=42, placeholder_text=placeholder)
            entrada.pack(pady=7)
            campos[clave] = entrada

        def guardar():
            try:
                self.services.pacientes.registrar(
                    campos["dni"].get(),
                    campos["nombres"].get(),
                    campos["apellidos"].get(),
                    campos["telefono"].get(),
                    campos["direccion"].get(),
                    campos["fecha_nacimiento"].get(),
                )
                messagebox.showinfo("Correcto", "Paciente registrado correctamente.")
                win.destroy()
                self.cargar()
            except Exception as exc:
                messagebox.showerror("No se pudo registrar", str(exc))

        ctk.CTkButton(
            win,
            text="Guardar paciente",
            width=420,
            height=45,
            fg_color=COLOR_EXITO,
            command=guardar,
        ).pack(pady=24)
