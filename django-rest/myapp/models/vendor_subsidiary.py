from django.db import models

class VendorSubsidiary(models.Model):
    vendor = models.CharField(max_length=1024)
    subsidiary = models.CharField(max_length=1024)

    def to_json(self):
        return {
            'id': self.id,
            'vendor': self.vendor,
            'subsidiary': self.subsidiary,
        }
