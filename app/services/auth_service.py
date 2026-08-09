from app.models.token import Token
from app.repositories.auth_repository import AuthRepository
from app.core.security import create_token
from sqlalchemy.orm import Session
from app.schemas.auth import LoginSchema, LogOutSchema
from app.core.logger import logger
from fastapi import HTTPException
from app.exceptions import InternalServerException, UnauthorizedException


class AuthService:

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def logout_service(self, db: Session, refresh_token: LogOutSchema):
        try:
            res = self.repo.logout(db, refresh_token)
            if res is None:
                logger.error("invalied refreshToken")
                raise UnauthorizedException("invalied refreshToken")
            if res:
                logger.info(f"user logout seccussed")
                return "user logout seccussed"
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"logout error {e}")
            raise InternalServerException("failed to logout user")

    def login_service(self, db: Session, login_data: LoginSchema):
        try:
            print(login_data.user_name)
            result = self.repo.login(db, login_data)

            if result is None:
                logger.warning(f"login failed for username {login_data.user_name}")
                return None

            logger.info(f"user {login_data.user_name} logged in successfully")

            return result

        except Exception as e:
            logger.error(f"login error for username {login_data.user_name}: {e}")
            print(e)
            raise InternalServerException("failed to login user")

    def refresh_access_token_service(self, db: Session, refresh_token: str):
        try:
            result = self.repo.refresh_access_token(db, refresh_token)

            if result is None:
                logger.warning("invalid refresh token")
                raise UnauthorizedException("invalid refresh token")

            logger.info("access token refreshed successfully")

            return result

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"refresh token error: {e}")

            raise InternalServerException("failed to refresh access token")
