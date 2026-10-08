from datetime import date
from uuid import uuid4
from src.domain.historia_clinica import HistoriaClinica


class HistoriaService:
    def __init__(self, repo, cita_service):
        self.repo = repo
        self.cita_service = cita_service

    def listar(self):
        return self.repo.load_all()

    def registrar(self, cita_id, diagnostico, tratamiento="", observaciones=""):
        cita = self.cita_service.obtener_por_id(cita_id)

        if not cita:
            raise ValueError("La cita no existe.")
        if cita["estado"] != "ATENDIDA":
            raise ValueError("Solo una cita ATENDIDA puede generar historia clínica.")

        historias = self.repo.load_all()
        if any(h["cita_id"] == cita_id for h in historias):
            raise ValueError("La cita ya tiene una historia clínica.")

        historia = HistoriaClinica(
            id=uuid4().hex[:10].upper(),
            dni_paciente=cita["dni_paciente"],
            cita_id=cita_id,
            fecha=date.today().isoformat(),
            diagnostico=diagnostico,
            tratamiento=tratamiento,
            observaciones=observaciones,
        )
        historias.append(historia.to_dict())
        self.repo.save_all(historias)
        return historia.to_dict()

    def buscar_por_dni(self, dni):
        dni = str(dni).strip()
        return [h for h in self.repo.load_all() if h["dni_paciente"] == dni]
