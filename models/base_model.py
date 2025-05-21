from tortoise import Model, fields


class BaseModel(Model):
    id = fields.UUIDField(pk=True)
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]
