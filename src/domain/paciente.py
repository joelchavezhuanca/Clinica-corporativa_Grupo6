from dataclasses import dataclass


@dataclass
class Paciente:
    dni: str
    nombres: str
    apellidos: str
    telefono: str = ""
    direccion: str = ""
    fecha_nacimiento: str = ""

    def __post_init__(self):
        self.dni = str(self.dni).strip()
        self.nombres = self.nombres.strip()
        self.apellidos = self.apellidos.strip()

        if not (self.dni.isdigit() and len(self.dni) == 8):
            raise ValueError("El DNI debe contener exactamente 8 dígitos.")
        if not self.nombres:
            raise ValueError("Los nombres son obligatorios.")
        if not self.apellidos:
            raise ValueError("Los apellidos son obligatorios.")

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}".strip()

    def to_dict(self):
        return {
            "dni": self.dni,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "telefono": self.telefono.strip(),
            "direccion": self.direccion.strip(),
            "fecha_nacimiento": self.fecha_nacimiento.strip(),
        }
