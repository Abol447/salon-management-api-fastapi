from datetime import datetime
from typing import Any, Dict, Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Session

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # ---------------------------------
    # GET BY ID
    # ---------------------------------
    def get_by_id(
        self,
        db: Session,
        obj_id: int,
        include_deleted: bool = False,
    ) -> Optional[ModelType]:

        query = db.query(self.model).filter(
            self.model.id == obj_id
        )

        if hasattr(self.model, "IsDeleted") and not include_deleted:
            query = query.filter(
                self.model.IsDeleted == False
            )

        return query.first()

    # ---------------------------------
    # GET ALL
    # ---------------------------------
    def get_all(
        self,
        db: Session,
        include_deleted: bool = False,
    ) -> list[ModelType]:

        query = db.query(self.model)

        if hasattr(self.model, "IsDeleted") and not include_deleted:
            query = query.filter(
                self.model.IsDeleted == False
            )

        return query.all()

    # ---------------------------------
    # CREATE
    # ---------------------------------
    def create(
        self,
        db: Session,
        obj_in: CreateSchemaType,
    ) -> ModelType:

        db_obj = self.model(
            **obj_in.model_dump()
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    # ---------------------------------
    # UPDATE
    # ---------------------------------
    def update(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any],
    ) -> ModelType:

        update_data = (
            obj_in.model_dump(exclude_unset=True)
            if isinstance(obj_in, BaseModel)
            else obj_in
        )

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)

        return db_obj

    # ---------------------------------
    # SOFT DELETE
    # ---------------------------------
    def delete(
        self,
        db: Session,
        obj_id: int,
    ) -> Optional[ModelType]:

        obj = self.get_by_id(
            db,
            obj_id,
            include_deleted=True,
        )

        if obj is None:
            return None

        if hasattr(obj, "IsDeleted"):

            obj.IsDeleted = True

            if hasattr(obj, "DeletedAt"):
                obj.DeletedAt = datetime.utcnow()

        else:
            db.delete(obj)

        db.commit()

        if hasattr(obj, "IsDeleted"):
            db.refresh(obj)

        return obj

    # ---------------------------------
    # RESTORE
    # ---------------------------------
    def restore(
        self,
        db: Session,
        obj_id: int,
    ) -> Optional[ModelType]:

        obj = self.get_by_id(
            db,
            obj_id,
            include_deleted=True,
        )

        if obj is None:
            return None

        if not hasattr(obj, "IsDeleted"):
            return None

        obj.IsDeleted = False

        if hasattr(obj, "DeletedAt"):
            obj.DeletedAt = None

        db.commit()
        db.refresh(obj)

        return obj

    # ---------------------------------
    # EXISTS
    # ---------------------------------
    def exists(
        self,
        db: Session,
        include_deleted: bool = False,
        **filters,
    ) -> bool:

        query = db.query(self.model)

        if hasattr(self.model, "IsDeleted") and not include_deleted:
            query = query.filter(
                self.model.IsDeleted == False
            )

        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(
                    getattr(self.model, field) == value
                )

        return query.first() is not None

    # ---------------------------------
    # FIRST BY
    # ---------------------------------
    def first_by(
        self,
        db: Session,
        include_deleted: bool = False,
        **filters,
    ) -> Optional[ModelType]:

        query = db.query(self.model)

        if hasattr(self.model, "IsDeleted") and not include_deleted:
            query = query.filter(
                self.model.IsDeleted == False
            )

        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(
                    getattr(self.model, field) == value
                )

        return query.first()

    # ---------------------------------
    # FILTER BY
    # ---------------------------------
    def filter_by(
        self,
        db: Session,
        include_deleted: bool = False,
        **filters,
    ) -> list[ModelType]:

        query = db.query(self.model)

        if hasattr(self.model, "IsDeleted") and not include_deleted:
            query = query.filter(
                self.model.IsDeleted == False
            )

        for field, value in filters.items():
            if hasattr(self.model, field):
                query = query.filter(
                    getattr(self.model, field) == value
                )

        return query.all()