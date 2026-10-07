from dataclasses import dataclass


@dataclass
class HistoriaClinica:
    id: str
    dni_paciente: str
    cita_id: str
    fecha: str
    diagnostico: str
    tratamiento: str = ""
    observaciones: str = ""

    def __post_init__(self):
        self.diagnostico = self.diagnostico.strip()
        if not self.diagnostico:
            raise ValueError("El diagnóstico no puede estar vacío.")

    def to_dict(self):
        return {
            "id": self.id,
            "dni_paciente": self.dni_paciente.strip(),
            "cita_id": self.cita_id.strip(),
            "fecha": self.fecha.strip(),
            "diagnostico": self.diagnostico,
            "tratamiento": self.tratamiento.strip(),
            "observaciones": self.observaciones.strip(),
        }
