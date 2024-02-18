from pydantic import BaseModel


# Свойство пинга БД
class PingDb(BaseModel):
    postgres: str
    redis: str

    class Config:
        from_attributes = True
