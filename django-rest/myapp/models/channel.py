from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'createdAt': self.created_at.timestamp(),
            'updatedAt': self.updated_at.timestamp(),
        }

    def from_json(self, data):
        self.name = data['name']
