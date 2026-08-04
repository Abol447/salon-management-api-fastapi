from datetime import datetime

from sqlalchemy import Column, DateTime, Boolean


class TimestampMixin:

    CreatedAt = Column(
        DateTime,
        default=datetime.utcnow
    )


    UpdatedAt = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )



class SoftDeleteMixin:

    IsDeleted = Column(
        Boolean,
        default=False
    )


    DeletedAt = Column(
        DateTime,
        nullable=True
    )