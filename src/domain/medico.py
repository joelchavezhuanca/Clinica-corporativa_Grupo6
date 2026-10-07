from dataclasses import dataclass


@dataclass
class Medico:
    cmp: str
    nombres: str
    apellidos: str
    especialidad: str
    telefono: str = ""

    def __post_init__(self):
        self.cmp = str(self.cmp).strip()
        self.nombres = self.nombres.strip()
        self.apellidos = self.apellidos.strip()
        self.especialidad = self.especialidad.strip()

        if not self.cmp:
            raise ValueError("El CMP es obligatorio.")
        if not self.nombres or not self.apellidos:
            raise ValueError("El nombre del médico es obligatorio.")
        if not self.especialidad:
            raise ValueError("La especialidad es obligatoria.")

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}".strip()

    def to_dict(self):
        return {
            "cmp": self.cmp,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "especialidad": self.especialidad,
            "telefono": self.telefono.strip(),
        }
