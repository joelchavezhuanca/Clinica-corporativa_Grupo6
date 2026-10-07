import unittest
from src.domain.paciente import Paciente
from src.domain.medico import Medico


class TestDomain(unittest.TestCase):
    def test_paciente_valido(self):
        p = Paciente("12345678", "Ana", "Quispe")
        self.assertEqual(p.dni, "12345678")

    def test_dni_invalido(self):
        with self.assertRaises(ValueError):
            Paciente("123", "Ana", "Quispe")

    def test_medico_requiere_especialidad(self):
        with self.assertRaises(ValueError):
            Medico("CMP001", "Luis", "Pérez", "")


if __name__ == "__main__":
    unittest.main()
