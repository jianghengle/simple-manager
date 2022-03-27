from django.db import models

class Price(models.Model):
    product_id = models.IntegerField()
    channel_id = models.IntegerField()
    price = models.FloatField()
    date = models.CharField(max_length=128)
    timestamp = models.BigIntegerField()
    is_latest = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['product_id',]),
        ]

    def to_json(self):
        return {
            'id': self.id,
            'productId': self.product_id,
            'channelId': self.channel_id,
            'price': self.price,
            'date': self.date,
            'timestamp': self.timestamp,
            'isLatest': self.is_latest,
            'createdAt': self.created_at.timestamp(),
            'updatedAt': self.updated_at.timestamp(),
        }

    def from_json(self, data):
        self.product_id = data['productId']
        self.channel_id = data['channelId']
        self.price = data['price']
        self.date = data['date']
        self.timestamp = data['timestamp']
        self.is_latest = data['isLatest']
