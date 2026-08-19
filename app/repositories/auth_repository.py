from app.repositories.base.CRUDBase import CRUDBase
from app.models.token import Token
from app.schemas.token import TokenCreate, TokenUpdate
from sqlalchemy.orm import Session
from datetime import UTC, datetime
from app.core.security import create_token, verify_password, decode_token
from datetime import timedelta
from app.core.config import settings
from app.schemas.auth import LoginSchema, LoginResponse, LogOutSchema
from app.models.user import User
from app.schemas.token import refresh_token


class AuthRepository(CRUDBase[Token, TokenCreate, TokenUpdate]):
    def __init__(self):
        super().__init__(Token)

    def login(self, db: Session, user_data: LoginSchema) -> LoginResponse:

        query = db.query(User).filter(User.phone == user_data.phone_number).first()

        if query is None:
            return None

        islogin = verify_password(user_data.password, query.password_hash)
        if not islogin:
            return None

        refresh_token = self.create_refresh_token(db, query.id)
        access_token = create_token(
            {"sub": str(query.id), "type": "access", "role": str(query.role.name)}
        )
        res = LoginResponse(
            access_token=access_token, refresh_token=refresh_token.refresh_token
        )
        return res

    def logout(self, db: Session, refresh_token: LogOutSchema):
        token_data = decode_token(refresh_token.refresh_token)
        db_token = (
            db.query(Token)
            .filter(
                Token.refresh_token == refresh_token.refresh_token,
                Token.is_revoked == False,
            )
            .first()
        )
        if db_token is None:
            raise None
        db_token.is_revoked = True
        db.commit()
        db.refresh(db_token)
        return True

    def refresh_access_token(self, db: Session, refresh_token: str):
        db_refresh_token = (
            db.query(Token)
            .filter(Token.refresh_token == refresh_token, Token.is_revoked == False)
            .first()
        )

        if not db_refresh_token:
            return None

        refresh_decode = decode_token(db_refresh_token.refresh_token)

        db_refresh_token.is_revoked = True
        db.commit()
        db.refresh(db_refresh_token)

        new_refresh_token = self.create_refresh_token(db, refresh_decode["sub"])

        access_token = create_token(
            {
                "sub": refresh_decode["sub"],
                "type": "access",
            }
        )

        return LoginResponse(
            access_token=access_token, refresh_token=new_refresh_token.refresh_token
        )

    def create_refresh_token(self, db: Session, user_id: int) -> Token:
        active_token = (
            db.query(Token)
            .filter(
                Token.user_id == user_id,
                Token.expires_at > datetime.utcnow(),
                Token.is_revoked == False,
            )
            .first()
        )

        if active_token:
            return active_token
        refresh_token = create_token(
            {
                "sub": str(user_id),
                "type": "refresh",
            },
            timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        token = Token(
            user_id=user_id,
            refresh_token=refresh_token,
            expires_at=datetime.now(UTC)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            is_revoked=False,
        )

        db.add(token)
        db.commit()
        db.refresh(token)

        return token
