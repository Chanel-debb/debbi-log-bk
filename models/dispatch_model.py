from .base_model import BaseModel
from enum import Enum
import uuid
from tortoise import fields

def generate_dispatch_code():
    number = str(uuid.uuid4().int)[:10]  
    return f"ship_{number}"


class STATUS(str, Enum):
    PENDING = "PENDING"
    PICKED = "PROCESSING"
    ACCESSING = "ACCESSING"
    PACKAGING = "PACKAGING"
    EN_ROUTE = "EN ROUTE"
    DELIVERED = "DELIVERED"

class Recipient(BaseModel):
    full_name = fields.CharField(150, unique=True)
    address = fields.CharField(250, unique=True)
    phone_number_1 = fields.CharField(15, unique=True)
    phone_number_2 = fields.CharField(15, unique=True)

    

class Dispatch(BaseModel):
    sender = fields.ForeignKeyField("models.User",  related_name="deliver_owner")
    recipient = fields.ForeignKeyField("models.Recipient",   related_name="deliver_owner", on_delete=fields.SET_NULL, null=True)
    status = fields.CharEnumField(STATUS, default=STATUS.PENDING)
    content = fields.TextField()
    weight = fields.IntField()
    note = fields.TextField()
    delievery_date = fields.DateField()
    code = fields.CharField(16, default=generate_dispatch_code, null=True, unique=True)
    
