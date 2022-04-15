from django.db import models

class Price(models.Model):
    product_id = models.IntegerField()
    channel_id = models.IntegerField()
    price = models.FloatField()
    date = models.CharField(max_length=128)
    timestamp = models.BigIntegerField()
    is_latest = models.BooleanField()
    flag = models.CharField(max_length=64, default='', blank=True)
    latest_change = models.CharField(max_length=128, default='', blank=True)
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
            'flag': self.flag,
            'date': self.date,
            'timestamp': self.timestamp,
            'isLatest': self.is_latest,
            'latestChange': self.latest_change,
            'createdAt': self.created_at.timestamp(),
            'updatedAt': self.updated_at.timestamp(),
        }

    def from_json(self, data):
        self.product_id = data['productId']
        self.channel_id = data['channelId']
        self.price = data['price']
        self.flag = data['flag']
        self.date = data['date']
        self.timestamp = data['timestamp']
        self.is_latest = data['isLatest']
        self.latest_change = data['latestChange']
