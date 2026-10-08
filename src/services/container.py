from pathlib import Path
from src.services.json_repository import JsonRepository
from src.services.paciente_service import PacienteService
from src.services.medico_service import MedicoService
from src.services.cita_service import CitaService
from src.services.historia_service import HistoriaService

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


class ServiceContainer:
    def __init__(self):
        paciente_repo = JsonRepository(DATA_DIR / "pacientes.json")
        medico_repo = JsonRepository(DATA_DIR / "medicos.json")
        cita_repo = JsonRepository(DATA_DIR / "citas.json")
        historia_repo = JsonRepository(DATA_DIR / "historias.json")

        self.pacientes = PacienteService(paciente_repo)
        self.medicos = MedicoService(medico_repo)
        self.citas = CitaService(cita_repo, self.pacientes, self.medicos)
        self.historias = HistoriaService(historia_repo, self.citas)
