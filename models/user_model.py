import enum

from tortoise import fields

from models.base_model import BaseModel

from .base_model import BaseModel



class User(BaseModel):
    first_name = fields.CharField(50, null=True)
    last_name = fields.CharField(50, null=True)
    email = fields.CharField(200, unique=True)
    password = fields.CharField(200)
    is_verified = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        table = "users"
