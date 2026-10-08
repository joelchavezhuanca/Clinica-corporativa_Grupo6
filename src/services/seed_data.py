from datetime import date, timedelta


def cargar_datos_demo(services):
    """Carga datos demostrativos solo cuando cada colección está vacía."""

    if not services.pacientes.listar():
        datos = [
            ("12345678", "Ana", "Quispe", "984123456", "Av. La Cultura 123", "2000-05-12"),
            ("87654321", "Luis", "Huamán", "965111222", "Urb. Magisterio", "1998-09-21"),
            ("74125896", "Rosa", "Mamani", "951987654", "San Sebastián", "1995-03-10"),
            ("71458963", "Diego", "Soto", "948111555", "Wanchaq", "1990-12-01"),
            ("70881234", "María", "Flores", "977330011", "Santiago", "1987-07-18"),
            ("73995124", "Carlos", "Condori", "989441122", "San Jerónimo", "2002-02-05"),
        ]
        for fila in datos:
            services.pacientes.registrar(*fila)

    if not services.medicos.listar():
        datos = [
            ("CMP001", "Carlos", "Flores", "Cardiología", "987111222"),
            ("CMP002", "María", "Pérez", "Medicina General", "987333444"),
            ("CMP003", "Luis", "Vega", "Pediatría", "987555666"),
            ("CMP004", "Andrea", "Rojas", "Dermatología", "987777888"),
            ("CMP005", "José", "Salazar", "Traumatología", "986222333"),
        ]
        for fila in datos:
            services.medicos.registrar(*fila)

    if not services.citas.listar():
        hoy = date.today()
        agenda = [
            ("12345678", "CMP001", hoy, "08:30", "ATENDIDA"),
            ("87654321", "CMP002", hoy, "09:15", "PROGRAMADA"),
            ("74125896", "CMP003", hoy, "10:00", "PROGRAMADA"),
            ("71458963", "CMP004", hoy, "11:30", "CANCELADA"),
            ("70881234", "CMP005", hoy, "15:00", "PROGRAMADA"),
            ("73995124", "CMP001", hoy + timedelta(days=1), "09:00", "PROGRAMADA"),
            ("12345678", "CMP002", hoy + timedelta(days=1), "10:30", "PROGRAMADA"),
            ("87654321", "CMP003", hoy + timedelta(days=2), "08:00", "PROGRAMADA"),
            ("74125896", "CMP004", hoy + timedelta(days=3), "14:30", "PROGRAMADA"),
        ]

        creadas = []
        for dni, cmp, fecha, hora, estado in agenda:
            cita = services.citas.programar(dni, cmp, fecha.isoformat(), hora)
            if estado != "PROGRAMADA":
                services.citas.cambiar_estado(cita["id"], estado)
            creadas.append((cita, estado))

        # Una historia clínica realista para una cita atendida.
        atendida = next((c for c, estado in creadas if estado == "ATENDIDA"), None)
        if atendida and not services.historias.listar():
            services.historias.registrar(
                atendida["id"],
                "Control cardiológico. Signos vitales estables.",
                "Continuar medicación indicada y control en 30 días.",
                "Paciente orientada, sin signos de alarma.",
            )
