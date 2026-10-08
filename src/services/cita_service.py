from datetime import datetime, date
from uuid import uuid4
from src.domain.cita import Cita


class CitaService:
    def __init__(self, repo, paciente_service, medico_service):
        self.repo = repo
        self.paciente_service = paciente_service
        self.medico_service = medico_service

    def listar(self):
        return self.repo.load_all()

    def programar(self, dni_paciente, cmp_medico, fecha, hora):
        dni_paciente = str(dni_paciente).strip()
        cmp_medico = str(cmp_medico).strip()

        if not self.paciente_service.obtener_por_dni(dni_paciente):
            raise ValueError("El paciente no existe.")
        if not self.medico_service.obtener_por_cmp(cmp_medico):
            raise ValueError("El médico no existe.")

        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        datetime.strptime(hora, "%H:%M")

        if fecha_obj < date.today():
            raise ValueError("No se puede programar una cita en una fecha pasada.")

        citas = self.repo.load_all()
        activas = [c for c in citas if c["estado"] != "CANCELADA"]

        if any(
            c["cmp_medico"] == cmp_medico
            and c["fecha"] == fecha
            and c["hora"] == hora
            for c in activas
        ):
            raise ValueError("El médico ya tiene una cita en esa fecha y hora.")

        if any(
            c["dni_paciente"] == dni_paciente
            and c["fecha"] == fecha
            and c["hora"] == hora
            for c in activas
        ):
            raise ValueError("El paciente ya tiene una cita en esa fecha y hora.")

        cita = Cita(
            id=uuid4().hex[:10].upper(),
            dni_paciente=dni_paciente,
            cmp_medico=cmp_medico,
            fecha=fecha,
            hora=hora,
            estado="PROGRAMADA",
        )
        citas.append(cita.to_dict())
        self.repo.save_all(citas)
        return cita.to_dict()

    def cambiar_estado(self, cita_id, nuevo_estado):
        nuevo_estado = nuevo_estado.upper().strip()
        if nuevo_estado not in ("PROGRAMADA", "ATENDIDA", "CANCELADA"):
            raise ValueError("Estado no válido.")

        citas = self.repo.load_all()
        for cita in citas:
            if cita["id"] == cita_id:
                cita["estado"] = nuevo_estado
                self.repo.save_all(citas)
                return cita

        raise ValueError("No se encontró la cita.")

    def obtener_por_id(self, cita_id):
        return next((c for c in self.repo.load_all() if c["id"] == cita_id), None)

    def filtrar(self, texto="", estado="TODOS", fecha=""):
        texto = texto.strip().lower()
        resultado = self.repo.load_all()

        if estado and estado != "TODOS":
            resultado = [c for c in resultado if c["estado"] == estado]

        if fecha:
            resultado = [c for c in resultado if c["fecha"] == fecha]

        if texto:
            resultado = [
                c for c in resultado
                if texto in c["dni_paciente"].lower()
                or texto in c["cmp_medico"].lower()
                or texto in c["fecha"].lower()
                or texto in c["id"].lower()
            ]

        return resultado
