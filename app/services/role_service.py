from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.role import RoleCreate, RoleUpdate

from app.exceptions import (
    InternalServerException,
    BadRequestException,
    NotFoundException
)

from app.core.logger import logger



class RoleService:


    def __init__(
        self,
        repo: CRUDBase[Role, RoleCreate, RoleUpdate]
    ):
        self.repo = repo



   

    def create(
        self,
        db: Session,
        role_data: RoleCreate
    ) -> Role:


        try:


            exists = self.repo.exists(
                db,
                name=role_data.name
            )


            if exists:

                raise BadRequestException(
                    "Role already exists"
                )


            role = self.repo.create(
                db,
                role_data
            )


            logger.info(
                f"Role created successfully: {role.name}"
            )


            return role



        except BadRequestException:

            raise


        except Exception as e:


            logger.exception(
                "Error while creating role"
            )


            raise InternalServerException(
                "Can't create role"
            ) from e





    def get_all(
        self,
        db: Session
    ) -> list[Role]:


        try:

            return self.repo.get_all(db)


        except Exception as e:


            logger.exception(
                "Error while getting roles"
            )


            raise InternalServerException(
                "Can't get roles"
            ) from e



    def get_by_id(
        self,
        db: Session,
        role_id: int
    ) -> Role:


        try:


            role = self.repo.get_by_id(
                db,
                role_id
            )


            if not role:

                raise NotFoundException(
                    "Role not found"
                )


            return role



        except NotFoundException:

            raise


        except Exception as e:


            logger.exception(
                "Error while getting role"
            )


            raise InternalServerException(
                "Can't get role"
            ) from e




   

    def update(
        self,
        db: Session,
        role_id: int,
        role_data: RoleUpdate
    ) -> Role:


        try:


            role = self.get_by_id(
                db,
                role_id
            )


            updated_role = self.repo.update(
                db,
                role,
                role_data
            )


            logger.info(
                f"Role updated: {role_id}"
            )


            return updated_role



        except NotFoundException:

            raise



        except Exception as e:


            logger.exception(
                "Error while updating role"
            )


            raise InternalServerException(
                "Can't update role"
            ) from e





    def delete(
        self,
        db: Session,
        role_id: int
    ) -> Role:


        try:


            role = self.repo.delete(
                db,
                role_id
            )


            if not role:

                raise NotFoundException(
                    "Role not found"
                )


            logger.info(
                f"Role deleted: {role_id}"
            )


            return role



        except NotFoundException:

            raise



        except Exception as e:


            logger.exception(
                "Error while deleting role"
            )


            raise InternalServerException(
                "Can't delete role"
            ) from e