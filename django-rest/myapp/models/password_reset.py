from django.db import models

class PasswordReset(models.Model):
    email = models.CharField(max_length=512)
    key = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'key': self.key,
            'createdAt': self.created_at.timestamp(),
        }
