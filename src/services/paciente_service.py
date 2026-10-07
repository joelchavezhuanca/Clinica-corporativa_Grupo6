from src.domain.paciente import Paciente


class PacienteService:
    def __init__(self, repo):
        self.repo = repo

    def listar(self):
        return self.repo.load_all()

    def registrar(self, dni, nombres, apellidos, telefono="", direccion="", fecha_nacimiento=""):
        pacientes = self.repo.load_all()
        dni = str(dni).strip()

        if any(p["dni"] == dni for p in pacientes):
            raise ValueError("Ya existe un paciente con ese DNI.")

        paciente = Paciente(
            dni=dni,
            nombres=nombres,
            apellidos=apellidos,
            telefono=telefono,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
        )
        pacientes.append(paciente.to_dict())
        self.repo.save_all(pacientes)
        return paciente.to_dict()

    def buscar(self, texto=""):
        texto = texto.strip().lower()
        if not texto:
            return self.listar()

        return [
            p for p in self.repo.load_all()
            if texto in p["dni"].lower()
            or texto in p["nombres"].lower()
            or texto in p["apellidos"].lower()
        ]

    def obtener_por_dni(self, dni):
        dni = str(dni).strip()
        return next((p for p in self.repo.load_all() if p["dni"] == dni), None)
