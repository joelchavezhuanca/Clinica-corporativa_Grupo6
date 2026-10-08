import csv
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.ui.common import (
    titulo,
    aplicar_zebra,
    COLOR_PRIMARIO,
    COLOR_EXITO,
    COLOR_PELIGRO,
)


class ReportesPage:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services

    def render(self):
        titulo(self.parent, "Reportes", "Indicadores y exportación de citas")

        citas = self.services.citas.listar()

        resumen = ctk.CTkFrame(self.parent, fg_color="white", corner_radius=15)
        resumen.pack(fill="x", pady=(0, 16))

        datos = [
            ("Total citas", len(citas), COLOR_PRIMARIO),
            ("Programadas", sum(c["estado"] == "PROGRAMADA" for c in citas), "#0D6EFD"),
            ("Atendidas", sum(c["estado"] == "ATENDIDA" for c in citas), COLOR_EXITO),
            ("Canceladas", sum(c["estado"] == "CANCELADA" for c in citas), COLOR_PELIGRO),
        ]

        for nombre, valor, color in datos:
            bloque = ctk.CTkFrame(resumen, fg_color="transparent")
            bloque.pack(side="left", expand=True, fill="x", padx=12, pady=16)
            ctk.CTkLabel(bloque, text=nombre, text_color="#64748B").pack()
            ctk.CTkLabel(
                bloque,
                text=str(valor),
                font=("Segoe UI", 26, "bold"),
                text_color=color,
            ).pack()

        zona = ctk.CTkFrame(self.parent, fg_color="transparent")
        zona.pack(fill="x", pady=(0, 14))

        ctk.CTkButton(
            zona,
            text="Exportar citas a CSV",
            command=self.exportar,
        ).pack(side="right")

        graf = ctk.CTkFrame(self.parent, fg_color="white", corner_radius=15, height=260)
        graf.pack(fill="x", pady=(0, 16))
        graf.pack_propagate(False)
        self._grafico(graf, citas)

        self.tabla = ttk.Treeview(
            self.parent,
            columns=("id", "fecha", "hora", "dni", "cmp", "estado"),
            show="headings",
            height=10,
        )
        aplicar_zebra(self.tabla)

        for col, txt, width in [
            ("id", "ID", 110),
            ("fecha", "Fecha", 110),
            ("hora", "Hora", 80),
            ("dni", "DNI paciente", 130),
            ("cmp", "CMP médico", 130),
            ("estado", "Estado", 130),
        ]:
            self.tabla.heading(col, text=txt)
            self.tabla.column(col, width=width)

        for i, c in enumerate(citas):
            self.tabla.insert(
                "",
                "end",
                values=(
                    c["id"],
                    c["fecha"],
                    c["hora"],
                    c["dni_paciente"],
                    c["cmp_medico"],
                    c["estado"],
                ),
                tags=(c["estado"].lower(), "par" if i % 2 == 0 else "impar"),
            )

        self.tabla.pack(fill="both", expand=True)

    def _grafico(self, parent, citas):
        fig = Figure(figsize=(8, 2.4), dpi=90, facecolor="white")
        ax = fig.add_subplot(111)

        conteos = {
            "Programadas": sum(c["estado"] == "PROGRAMADA" for c in citas),
            "Atendidas": sum(c["estado"] == "ATENDIDA" for c in citas),
            "Canceladas": sum(c["estado"] == "CANCELADA" for c in citas),
        }

        ax.bar(
            list(conteos.keys()),
            list(conteos.values()),
            color=["#0D6EFD", "#198754", "#C0392B"],
            width=0.5,
        )
        ax.set_title("Distribución general de citas", fontsize=11)
        ax.grid(axis="y", alpha=0.15)
        for spine in ax.spines.values():
            spine.set_visible(False)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=8)

    def exportar(self):
        destino = filedialog.asksaveasfilename(
            title="Guardar reporte",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
        )
        if not destino:
            return

        with open(destino, "w", newline="", encoding="utf-8-sig") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["ID", "Fecha", "Hora", "DNI paciente", "CMP médico", "Estado"])
            for c in self.services.citas.listar():
                writer.writerow(
                    [
                        c["id"],
                        c["fecha"],
                        c["hora"],
                        c["dni_paciente"],
                        c["cmp_medico"],
                        c["estado"],
                    ]
                )

        messagebox.showinfo("Reporte", "Archivo CSV exportado correctamente.")
