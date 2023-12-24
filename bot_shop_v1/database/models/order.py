from tortoise import fields
from tortoise.models import Model


class Order(Model):
    id = fields.IntField(pk=True)
    products = fields.ManyToManyField(
        'models.Product', related_name='order', through='order_product')
    user = fields.ForeignKeyField(
        'models.User', related_name='orders')
    status = fields.CharField(max_length=50, default='proceed', null=True)
    price = fields.FloatField(default=0)
