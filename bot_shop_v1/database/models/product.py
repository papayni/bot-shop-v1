from tortoise import fields
from tortoise.models import Model


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    category = fields.CharField(max_length=50)
    sub_category = fields.CharField(max_length=50)
    price = fields.FloatField()
    description = fields.TextField()
    image = fields.CharField(max_length=255, default='', null=True)
    order: fields.ManyToManyRelation['Order']
    color = fields.CharField(max_length=255, default='', null=True)
    memory = fields.IntField(max_length=255, default=0, null=True)
