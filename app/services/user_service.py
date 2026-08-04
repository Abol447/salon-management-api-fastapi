from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base.CRUDBase import CRUDBase
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from app.exceptions import InternalServerException
from app.core.logger import logger


class UserService:

    def __init__(
        self,
        repository: CRUDBase[User, UserCreate, UserUpdate]
    ):
        self.repository = repository


    def create(
        self,
        db: Session,
        user_data: UserCreate
    ):

        try:

            user_data.password_hash = hash_password(
                user_data.password_hash
            )

            response = self.repository.create(
                db,
                user_data
            )

            logger.info(
                f"user created successfully id={response.id}"
            )

            return response


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