from services.db import RepositoryDB
from models.user import User
from schemas.users import UserCreate, UserUpdate


class RepositoryUser(RepositoryDB[User, UserCreate, UserUpdate]):
    pass


user_rep = RepositoryUser(User)
