import customtkinter as ctk

from src.services.container import ServiceContainer
from src.services.seed_data import cargar_datos_demo
from src.ui.login import LoginWindow
from src.ui.main_window import MainWindow


class ClinicaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Clínica Salud Integral - Sistema de Gestión")
        self.geometry("1440x860")
        self.minsize(1220, 720)

        self.services = ServiceContainer()
        cargar_datos_demo(self.services)

        LoginWindow(self, self.abrir_principal)

    def abrir_principal(self):
        MainWindow(self, self.services)


def ejecutar_aplicacion():
    app = ClinicaApp()
    app.mainloop()
