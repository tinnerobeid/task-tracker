from tortoise.models import Model
from tortoise.fields import IntField, CharField, BooleanField

class Task(Model):
    id = IntField(pk=True)
    task = CharField(max_length=100, null=False)
    done = BooleanField(default=False, null=False)