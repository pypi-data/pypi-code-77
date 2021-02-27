from typing import Any, Dict, Optional, Union
from passlib.context import CryptContext
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


def getCrudClass(ModelType, CreateSchemaType, UpdateSchemaType):
    """Return Class for CRUD utilities. You can inherit the class and customize as per your wish.
    Please Note: Constructor requires a parameters: model"""
    return CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def getUserCrudClass(User, UserIn, UserUpdate):
    """
    User must have following fields:
    email, username, hashed_password

    returns the CRUDUser class which could be customized as per your choice.
    """
    class CRUDUser(CRUDBase[User, UserIn, UserUpdate]):

        def create(self, user: UserIn, db: Session):
            ''''''
            temp = user.dict()
            temp["hashed_password"] = hash(user.password)
            del temp["password"]
            db_obj = User(**temp)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

        def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
            return db.query(User).filter(User.email == email).first()

        def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
            return db.query(User).filter(User.username == username).first()

        def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            if update_data["password"]:
                hashed_password = hash(update_data["password"])
                del update_data["password"]
                update_data["hashed_password"] = hashed_password
            return super().update(db, db_obj=db_obj, obj_in=update_data)

        def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
            user = self.get_by_email(db, email=email)
            if not user:
                return None
            if not verify_password(password, user.hashed_password):
                return None
            return user

    return CRUDUser
