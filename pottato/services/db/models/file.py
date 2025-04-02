from tortoise import fields, models


class FileModel(models.Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField(max_length=200)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    filepath = fields.CharField(max_length=300)
