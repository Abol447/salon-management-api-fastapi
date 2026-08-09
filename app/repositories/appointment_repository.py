from app.repositories.base.CRUDBase import CRUDBase
from app.models.appointment import Appointment
from app.schemas.Appointment import AppointmentCreate, AppointmentUpdate


class AppointmentRepository(
    CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]
):
    def __init__(self):
        super().__init__(Appointment)
