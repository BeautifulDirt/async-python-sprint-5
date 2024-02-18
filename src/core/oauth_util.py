from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    '''Проверка валидности пароля'''
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    '''Получение зашифрованного пароля'''
    return pwd_context.hash(password)
