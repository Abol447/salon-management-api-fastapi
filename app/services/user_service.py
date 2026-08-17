from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base.CRUDBase import CRUDBase
from app.core.messages import messages
from app.services.role_service import RoleService
from app.services.customer_service import CustomerService
from app.exceptions import ForbiddenException
from app.core.security import hash_password
from app.core.logger import logger
from app.exceptions import InternalServerException, NotFoundException
from app.schemas.customer import CustomerCreate
from app.models.customer import Customer
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate
from app.schemas.customer import CustomerCreate, CustomerUpdate
from fastapi import HTTPException
from app.models.owner import Owner
from app.schemas.owner import OwnerCreate, OwnerUpdate


class UserService:

    def __init__(
        self,
        repository: CRUDBase[User, UserCreate, UserUpdate],
        role_service: CRUDBase[Role, RoleCreate, RoleUpdate],
        customer_service: CRUDBase[Customer, CustomerCreate, CustomerUpdate],
        owner_repo: CRUDBase[Owner, OwnerCreate, OwnerUpdate],
    ):
        self.repository = repository
        self.role_service = role_service
        self.customer_service = customer_service
        self.owner = owner_repo

    def create(self, db: Session, user_data: UserCreate):

        try:
            role = self.role_service.get_by_id(db, user_data.role_id)

            user_data.password_hash = hash_password(user_data.password_hash)

            if user_data.user_name:
                user_name = self.repository.filter_by(db, user_name=user_data.user_name)
                print(user_data.user_name)
                if len(user_name):
                    logger.warning(
                        f"Duplicate entry {user_data.user_name} for key 'user_name' "
                    )
                    raise ForbiddenException(messages.USERNAME_ALREADY_EXISTS)
            if user_data.email:
                email = self.repository.filter_by(db, email=user_data.email)
                if len(email) > 0:
                    logger.warning(f"Duplicate entry {user_data.email} for key 'email'")
                    raise ForbiddenException(messages.EMAIL_ALREADY_EXISTS)

            response = self.repository.create(db, user_data)
            if role.name.lower() == "customer":
                self.customer_service.create(db, CustomerCreate(user_id=response.id))
            if role.name.lower() == "owner":
                self.owner.create(db, OwnerCreate(user_id=response.id))
            logger.info(f"user created successfully id={response.id}")

            return response

        except HTTPException:
            raise
        except Exception as e:

            logger.error(f"failed to create user: {e}")

            raise InternalServerException(messages.USER_CREATED_ERROR)

    def get(self, db: Session, user_id: int):

        try:

            response = self.repository.get_by_id(db, user_id)

            if not response:
                logger.warning(f"user not found id={user_id}")
                raise NotFoundException(messages.USER_NOT_FOUND)

            else:
                logger.info(f"user fetched successfully id={user_id}")

            return response

        except HTTPException:
            raise

        except Exception as e:

            logger.error(f"failed to get user {user_id}: {e}")

            raise InternalServerException(messages.USER_GET_ERROR)

    def get_all(self, db: Session):

        try:

            response = self.repository.get_all(db)

            logger.info("users fetched successfully")

            return response

        except Exception as e:

            logger.error(f"failed to get users: {e}")

            raise InternalServerException(messages.USER_GET_ERROR)

    def update(self, db: Session, user_id: int, user_data: UserUpdate):

        try:

            user = self.get(db, user_id)

            if not user:
                logger.warning(f"user not found for update id={user_id}")

                raise InternalServerException(messages.USER_NOT_FOUND)

            response = self.repository.update(db, user, user_data)

            logger.info(f"user updated successfully id={user_id}")

            return response

        except Exception as e:

            logger.error(f"failed to update user {user_id}: {e}")

            raise InternalServerException(messages.USER_UPDATED_ERROR)

    def delete(self, db: Session, user_id: int):

        try:

            response = self.repository.delete(db, user_id)

            logger.info(f"user deleted successfully id={user_id}")

            return response

        except Exception as e:

            logger.error(f"failed to delete user {user_id}: {e}")

            raise InternalServerException(messages.DELETE_ERROR)
