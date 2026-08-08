from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

from app.repositories.base.CRUDBase import CRUDBase

from app.services.role_service import RoleService
from app.services.customer_service import CustomerService
from app.exceptions import ForbiddenException
from app.core.security import hash_password
from app.core.logger import logger
from app.exceptions import InternalServerException
from app.schemas.customer import CustomerCreate
from app.models.customer import Customer
from app.models.role import Role
from app.schemas.role import  RoleCreate , RoleUpdate
from app.schemas.customer import CustomerCreate , CustomerUpdate
from fastapi import HTTPException
class UserService:

    def __init__(
        self,
        repository: CRUDBase[User, UserCreate, UserUpdate],
        role_service: CRUDBase[Role , RoleCreate , RoleUpdate],
        customer_service: CRUDBase[Customer , CustomerCreate , CustomerUpdate],
    ):
        self.repository = repository
        self.role_service = role_service
        self.customer_service = customer_service


    def create(
        self,
        db: Session,
        user_data: UserCreate
    ):

        try:
            role = self.role_service.get_by_id(db , user_data.role_id)
             

            user_data.password_hash = hash_password(
                user_data.password_hash
            )

            user_name = self.repository.filter_by(db , user_name = user_data.user_name)

            if len(user_name) : 
                logger.warning(f"Duplicate entry {user_data.user_name} for key 'user_name' => {e}")
                raise ForbiddenException(f"Duplicate entry {user_data.user_name} for key 'user_name'")

            email = self.repository.filter_by(db , email = user_data.email)
            if len(email) > 0 :
                logger.warning(f"Duplicate entry {user_data.email} for key 'email' => {e}")
                raise ForbiddenException(f"Duplicate entry {user_data.email} for key 'user_name'")
                
            response = self.repository.create(
                db,
                user_data
            )
            if role.name.lower() == "customer":
                self.customer_service.create(
                    db ,
                    CustomerCreate(
                        user_id= response.id
                    )
                )

            logger.info(
                f"user created successfully id={response.id}"
            ) 

            return response

        except HTTPException :
            raise
        except Exception as e:

            logger.error(
                f"failed to create user: {e}"
            )

            raise InternalServerException(
                "failed to create user"
            )



    def get(
        self,
        db: Session,
        user_id: int
    ):

        try:

            response = self.repository.get_by_id(
                db,
                user_id
            )

            if not response:
                logger.warning(
                    f"user not found id={user_id}"
                )

            else:
                logger.info(
                    f"user fetched successfully id={user_id}"
                )

            return response


        except Exception as e:

            logger.error(
                f"failed to get user {user_id}: {e}"
            )

            raise InternalServerException(
                "failed to get user"
            )



    def get_all(
        self,
        db: Session
    ):

        try:

            response = self.repository.get_all(
                db
            )

            logger.info(
                "users fetched successfully"
            )

            return response


        except Exception as e:

            logger.error(
                f"failed to get users: {e}"
            )

            raise InternalServerException(
                "failed to get users"
            )



    def update(
        self,
        db: Session,
        user_id: int,
        user_data: UserUpdate
    ):

        try:

            user = self.get(
                db,
                user_id
            )


            if not user:
                logger.warning(
                    f"user not found for update id={user_id}"
                )

                raise InternalServerException(
                    "user not found"
                )


            response = self.repository.update(
                db,
                user,
                user_data
            )


            logger.info(
                f"user updated successfully id={user_id}"
            )

            return response


        except Exception as e:

            logger.error(
                f"failed to update user {user_id}: {e}"
            )

            raise InternalServerException(
                "failed to update user"
            )



    def delete(
        self,
        db: Session,
        user_id: int
    ):

        try:

            response = self.repository.delete(
                db,
                user_id
            )


            logger.info(
                f"user deleted successfully id={user_id}"
            )

            return response


        except Exception as e:

            logger.error(
                f"failed to delete user {user_id}: {e}"
            )

            raise InternalServerException(
                "failed to delete user"
            )