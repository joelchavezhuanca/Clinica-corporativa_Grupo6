from src.domain.medico import Medico


class MedicoService:
    def __init__(self, repo):
        self.repo = repo

    def listar(self):
        return self.repo.load_all()

    def registrar(self, cmp, nombres, apellidos, especialidad, telefono=""):
        medicos = self.repo.load_all()
        cmp = str(cmp).strip()

        if any(m["cmp"] == cmp for m in medicos):
            raise ValueError("Ya existe un médico con ese CMP.")

        medico = Medico(cmp, nombres, apellidos, especialidad, telefono)
        medicos.append(medico.to_dict())
        self.repo.save_all(medicos)
        return medico.to_dict()

    def buscar(self, texto=""):
        texto = texto.strip().lower()
        if not texto:
            return self.listar()

        return [
            m for m in self.repo.load_all()
            if texto in m["cmp"].lower()
            or texto in m["nombres"].lower()
            or texto in m["apellidos"].lower()
            or texto in m["especialidad"].lower()
        ]

    def obtener_por_cmp(self, cmp):
        cmp = str(cmp).strip()
        return next((m for m in self.repo.load_all() if m["cmp"] == cmp), None)
