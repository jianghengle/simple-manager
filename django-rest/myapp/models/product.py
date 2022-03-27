from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=512)
    brand = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    home_depot_item_id = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'model': self.model,
            'homeDepotItemId': self.home_depot_item_id,
            'createdAt': self.created_at.timestamp(),
            'updatedAt': self.updated_at.timestamp(),
        }

    def from_json(self, data):
        self.name = data['name']
        self.brand = data['brand']
        self.model = data['model']
        self.home_depot_item_id = data['homeDepotItemId']
