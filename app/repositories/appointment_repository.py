from app.repositories.base.CRUDBase import CRUDBase
from app.models.appointment import Appointment
from app.schemas.Appointment import AppointmentCreate, AppointmentUpdate
from sqlalchemy.orm import Session
from app.schemas.Appointment import AppointmentFilter
from datetime import datetime, date, timedelta
from app.models.AppointmentService import AppointmentService
from app.models.user import User


class AppointmentRepository(
    CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]
):
    def __init__(self):
        super().__init__(Appointment)

    def filter(self, db: Session, appointment_filter: AppointmentFilter):
        query = db.query(Appointment).join(
            AppointmentService, AppointmentService.appointment_id == Appointment.id
        )

        if appointment_filter.start_date:
            start = datetime.combine(appointment_filter.start_date, datetime.min.time())

            end = start + timedelta(days=1)

            query = query.filter(
                Appointment.start_time >= start, Appointment.start_time < end
            )

        if appointment_filter.service_id:
            query = query.filter(
                AppointmentService.service_id == appointment_filter.service_id
            )

        if appointment_filter.customer_id:
            query = query.filter(
                Appointment.customer_id == appointment_filter.customer_id
            )

        if appointment_filter.salon_id:
            query = query.filter(Appointment.salon_id == appointment_filter.salon_id)

        total = query.distinct().count()

        offset = (appointment_filter.page - 1) * appointment_filter.page_size

        appointments = (
            query.distinct().offset(offset).limit(appointment_filter.page_size).all()
        )

        return appointments, total
