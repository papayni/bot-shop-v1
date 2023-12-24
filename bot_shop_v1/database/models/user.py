from pypika import Order
from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    balance = fields.FloatField(default=0)
    orders: fields.ReverseRelation['Order']
