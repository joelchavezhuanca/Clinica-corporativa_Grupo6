from dataclasses import dataclass
from datetime import datetime

ESTADOS_CITA = ("PROGRAMADA", "ATENDIDA", "CANCELADA")


@dataclass
class Cita:
    id: str
    dni_paciente: str
    cmp_medico: str
    fecha: str
    hora: str
    estado: str = "PROGRAMADA"

    def __post_init__(self):
        self.dni_paciente = self.dni_paciente.strip()
        self.cmp_medico = self.cmp_medico.strip()
        self.fecha = self.fecha.strip()
        self.hora = self.hora.strip()
        self.estado = self.estado.upper().strip()

        if self.estado not in ESTADOS_CITA:
            raise ValueError("Estado de cita no válido.")

        datetime.strptime(self.fecha, "%Y-%m-%d")
        datetime.strptime(self.hora, "%H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "dni_paciente": self.dni_paciente,
            "cmp_medico": self.cmp_medico,
            "fecha": self.fecha,
            "hora": self.hora,
            "estado": self.estado,
        }
