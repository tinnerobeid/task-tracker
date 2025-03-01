from tortoise.models import Model
from tortoise.fields import IntField, CharField, BooleanField
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

class Task(Model):
    id = IntField(pk=True)
    task = CharField(max_length=100, null=False)
    done = BooleanField(default=False, null=False)