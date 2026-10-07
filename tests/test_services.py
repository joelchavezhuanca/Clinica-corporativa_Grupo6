import tempfile
import unittest
from pathlib import Path
from datetime import date, timedelta

from src.services.json_repository import JsonRepository
from src.services.paciente_service import PacienteService
from src.services.medico_service import MedicoService
from src.services.cita_service import CitaService
from src.services.historia_service import HistoriaService


class TestServices(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)

        self.pacientes = PacienteService(JsonRepository(base / "pacientes.json"))
        self.medicos = MedicoService(JsonRepository(base / "medicos.json"))
        self.citas = CitaService(
            JsonRepository(base / "citas.json"),
            self.pacientes,
            self.medicos,
        )
        self.historias = HistoriaService(
            JsonRepository(base / "historias.json"),
            self.citas,
        )

        self.pacientes.registrar("12345678", "Ana", "Quispe")
        self.medicos.registrar("CMP001", "Luis", "Pérez", "Cardiología")

    def tearDown(self):
        self.tmp.cleanup()

    def test_cita_y_conflicto(self):
        fecha = (date.today() + timedelta(days=1)).isoformat()
        self.citas.programar("12345678", "CMP001", fecha, "09:00")

        with self.assertRaises(ValueError):
            self.citas.programar("12345678", "CMP001", fecha, "09:00")

    def test_historia_solo_atendida(self):
        fecha = (date.today() + timedelta(days=1)).isoformat()
        cita = self.citas.programar("12345678", "CMP001", fecha, "10:00")

        with self.assertRaises(ValueError):
            self.historias.registrar(cita["id"], "Control")

        self.citas.cambiar_estado(cita["id"], "ATENDIDA")
        historia = self.historias.registrar(cita["id"], "Control")
        self.assertEqual(historia["dni_paciente"], "12345678")


if __name__ == "__main__":
    unittest.main()
