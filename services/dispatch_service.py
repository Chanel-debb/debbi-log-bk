from fastapi import HTTPException
from dto.dispatch_dto import DispatchSchema, RecipientSchema
from models.dispatch_model import Recipient, Dispatch
from models.user_model import User
import uuid
from datetime import date

def generate_dispatch_code():
    number = str(uuid.uuid4().int)[:10]  
    return f"ship_{number}"

class RecipientService:
    @staticmethod
    async def list():
        return await Dispatch.all()
    
    @staticmethod
    async def get(id: str):
        return await Dispatch.get_or_none(id=id)
    
    @staticmethod
    async def create(user_id: str, dto: DispatchSchema):
        user = await User.get_or_none(id=user_id)
        if not user:
            raise HTTPException(detail="Invalid user", status_code=400)

        recipient = None
        if dto.recipient_id:
            recipient = await Recipient.get_or_none(id=dto.recipient_id)

       
        if not recipient and dto.new_recipient:
            recipient = await Recipient.create(
                full_name=dto.new_recipient.full_name,
                address=dto.new_recipient.address,
                phone_number_1=dto.new_recipient.phone_number_1,
                phone_number_2=dto.new_recipient.phone_number_2
            )

 
        if not recipient:
            raise HTTPException(detail="Recipient not found or not provided", status_code=400)

        return await Dispatch.create(
            sender=user,
            recipient=recipient,
            content=dto.content,
            weight=dto.weight,
            note=dto.note or None,
            delievery_date=dto.delievery_date or date.today(),
            code=dto.code or generate_dispatch_code()
        )


    @staticmethod
    async def update(dispatch_id: str,  dto: DispatchSchema):

        dispatch = await Dispatch.get_or_none(id=dispatch_id).prefetch_related("recipient")
        if not dispatch:
            raise HTTPException(status_code=404, detail="Dispatch not found")
        if dto.recipient_id:
            recipient = await Recipient.get_or_none(id=dto.recipient_id)
            if not recipient:
                raise HTTPException(status_code=400, detail="Recipient not found")

        elif dto.new_recipient:
            recipient = await Recipient.create(
                full_name=dto.new_recipient.full_name,
                address=dto.new_recipient.address,
                phone_number_1=dto.new_recipient.phone_number_1,
                phone_number_2=dto.new_recipient.phone_number_2
            )

        if recipient:
            dispatch.recipient = recipient

        if dto.content is not None:
            dispatch.content = dto.content

        if dto.weight is not None:
            dispatch.weight = dto.weight

        if dto.note is not None:
            dispatch.note = dto.note

        if dto.delievery_date is not None:
            dispatch.delievery_date = dto.delievery_date

        if dto.code is not None:
            dispatch.code = dto.code

        await dispatch.save()
        return dispatch