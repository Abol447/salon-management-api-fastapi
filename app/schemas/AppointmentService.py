from pydantic import BaseModel


class AppointmentServiceCreate(BaseModel):
    appointment_id: int
    service_id: int


class AppointmentServiceUpdate(BaseModel):
    appointment_id: int | None = None
    service_id: int | None = None


class AppointmentServiceResponse(BaseModel):
    id: int
    appointment_id: int
    service_id: int

    model_config = {"from_attributes": True}


class AppointmentServiceDelete(BaseModel):
    service_id: int
    appointment_id: int
