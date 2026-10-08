import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

COLOR_PRIMARIO = "#103B5D"
COLOR_SECUNDARIO = "#1E6D8F"
COLOR_ACENTO = "#19A7A0"
COLOR_EXITO = "#198754"
COLOR_ALERTA = "#F59E0B"
COLOR_PELIGRO = "#C0392B"
COLOR_FONDO = "#EEF3F7"
COLOR_CARD = "#FFFFFF"
COLOR_TEXTO = "#1F2937"
COLOR_TEXTO_SUAVE = "#64748B"


def configurar_estilo_treeview():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "Treeview",
        background="white",
        fieldbackground="white",
        foreground=COLOR_TEXTO,
        rowheight=34,
        font=("Segoe UI", 10),
        borderwidth=0,
    )
    style.configure(
        "Treeview.Heading",
        background="#E8EEF3",
        foreground=COLOR_PRIMARIO,
        font=("Segoe UI", 10, "bold"),
        padding=8,
        relief="flat",
    )
    style.map(
        "Treeview",
        background=[("selected", "#DDECF5")],
        foreground=[("selected", COLOR_PRIMARIO)],
    )


def aplicar_zebra(tabla):
    tabla.tag_configure("par", background="#F8FAFC")
    tabla.tag_configure("impar", background="#FFFFFF")
    tabla.tag_configure("programada", foreground="#0D6EFD")
    tabla.tag_configure("atendida", foreground=COLOR_EXITO)
    tabla.tag_configure("cancelada", foreground=COLOR_PELIGRO)


def limpiar(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def titulo(frame, texto, subtitulo=None):
    ctk.CTkLabel(
        frame,
        text=texto,
        font=("Segoe UI", 30, "bold"),
        text_color=COLOR_TEXTO,
    ).pack(anchor="w")

    if subtitulo:
        ctk.CTkLabel(
            frame,
            text=subtitulo,
            font=("Segoe UI", 13),
            text_color=COLOR_TEXTO_SUAVE,
        ).pack(anchor="w", pady=(3, 18))


def crear_logo(parent, fondo=COLOR_PRIMARIO, compacto=False):
    """Logo corporativo dibujado completamente con Python."""
    alto = 65 if compacto else 92
    cont = ctk.CTkFrame(parent, fg_color=fondo, height=alto, corner_radius=0)
    cont.pack(fill="x", padx=12 if compacto else 18, pady=(16, 20))
    cont.pack_propagate(False)

    canvas = tk.Canvas(
        cont,
        width=52 if compacto else 64,
        height=52 if compacto else 64,
        bg=fondo,
        highlightthickness=0,
    )
    canvas.pack(side="left", padx=(2, 10))

    size = 52 if compacto else 62
    c = size / 2
    canvas.create_oval(4, 4, size-4, size-4, fill="#E8F7F6", outline="")
    canvas.create_rectangle(c-5, 14, c+5, size-14, fill=COLOR_ACENTO, outline="")
    canvas.create_rectangle(14, c-5, size-14, c+5, fill=COLOR_ACENTO, outline="")

    texto = ctk.CTkFrame(cont, fg_color="transparent")
    texto.pack(side="left", fill="both", expand=True)

    ctk.CTkLabel(
        texto,
        text="SALUD INTEGRAL",
        font=("Segoe UI", 18 if compacto else 21, "bold"),
        text_color="white",
    ).pack(anchor="w", pady=(7 if compacto else 12, 0))

    ctk.CTkLabel(
        texto,
        text="Clínica & Centro Médico",
        font=("Segoe UI", 10 if compacto else 11),
        text_color="#CFE5F2",
    ).pack(anchor="w")


def card(parent, titulo_card, valor, subtitulo="", color=COLOR_PRIMARIO):
    marco = ctk.CTkFrame(parent, fg_color=COLOR_CARD, corner_radius=15, height=126)
    marco.pack(side="left", fill="x", expand=True, padx=(0, 12))
    marco.pack_propagate(False)

    ctk.CTkFrame(marco, fg_color=color, width=5, corner_radius=3).pack(
        side="left", fill="y", padx=(0, 14)
    )

    contenido = ctk.CTkFrame(marco, fg_color="transparent")
    contenido.pack(side="left", fill="both", expand=True, pady=17)

    ctk.CTkLabel(
        contenido,
        text=titulo_card,
        font=("Segoe UI", 13),
        text_color=COLOR_TEXTO_SUAVE,
    ).pack(anchor="w")

    ctk.CTkLabel(
        contenido,
        text=str(valor),
        font=("Segoe UI", 30, "bold"),
        text_color=color,
    ).pack(anchor="w", pady=(2, 0))

    if subtitulo:
        ctk.CTkLabel(
            contenido,
            text=subtitulo,
            font=("Segoe UI", 10),
            text_color=COLOR_TEXTO_SUAVE,
        ).pack(anchor="w")
    return marco
