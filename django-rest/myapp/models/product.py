from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=512)
    brand = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    home_depot_item_id = models.CharField(max_length=256, default='', blank=True)
    wayfair_sku = models.CharField(max_length=256, default='', blank=True)
    wayfair_option_name = models.CharField(max_length=256, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['model',]),
        ]

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'model': self.model,
            'homeDepotItemId': self.home_depot_item_id,
            'wayfairSku': self.wayfair_sku,
            'wayfairOptionName': self.wayfair_option_name,
            'createdAt': self.created_at.timestamp(),
            'updatedAt': self.updated_at.timestamp(),
        }

    def from_json(self, data):
        self.name = data['name']
        self.brand = data['brand']
        self.model = data['model']
        self.home_depot_item_id = data['homeDepotItemId']
        self.wayfair_sku = data['wayfairSku']
        self.wayfair_option_name = data['wayfairOptionName']
