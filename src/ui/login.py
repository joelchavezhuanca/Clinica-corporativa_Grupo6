import customtkinter as ctk
from tkinter import messagebox
from src.ui.common import (
    COLOR_PRIMARIO,
    COLOR_SECUNDARIO,
    COLOR_FONDO,
    crear_logo,
)


class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, on_success):
        super().__init__(master, fg_color=COLOR_FONDO)
        self.on_success = on_success
        self.pack(fill="both", expand=True)
        self._crear()

    def _crear(self):
        card = ctk.CTkFrame(self, width=470, height=565, corner_radius=24, fg_color="white")
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        crear_logo(card, fondo="white")

        ctk.CTkLabel(
            card,
            text="Acceso al sistema",
            font=("Segoe UI", 25, "bold"),
            text_color=COLOR_PRIMARIO,
        ).pack(pady=(8, 4))

        ctk.CTkLabel(
            card,
            text="Ingrese sus credenciales para continuar",
            font=("Segoe UI", 12),
            text_color="#64748B",
        ).pack(pady=(0, 25))

        self.usuario = ctk.CTkEntry(
            card, width=350, height=45, placeholder_text="Usuario"
        )
        self.usuario.pack(pady=8)

        self.clave = ctk.CTkEntry(
            card, width=350, height=45, placeholder_text="Contraseña", show="●"
        )
        self.clave.pack(pady=8)

        self.usuario.insert(0, "admin")
        self.clave.insert(0, "admin123")

        ctk.CTkButton(
            card,
            text="INICIAR SESIÓN",
            width=350,
            height=47,
            fg_color=COLOR_SECUNDARIO,
            hover_color=COLOR_PRIMARIO,
            font=("Segoe UI", 13, "bold"),
            command=self.validar,
        ).pack(pady=(28, 15))

        ctk.CTkLabel(
            card,
            text="Demo académica: admin / admin123",
            font=("Segoe UI", 10),
            text_color="#94A3B8",
        ).pack()

        self.clave.bind("<Return>", lambda _: self.validar())

    def validar(self):
        if self.usuario.get().strip() == "admin" and self.clave.get() == "admin123":
            self.destroy()
            self.on_success()
        else:
            messagebox.showerror("Acceso denegado", "Usuario o contraseña incorrectos.")
