from django.db import models

class Attachment(models.Model):
    name = models.CharField(max_length=512)
    s3_bucket = models.CharField(max_length=256)
    s3_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=512)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            's3Bucket': self.s3_bucket,
            's3Key': self.s3_key,
            'createdAt': self.created_at.timestamp(),
            'updatedAt': self.updated_at.timestamp(),
            'createdBy': self.created_by,
        }

    def from_json(self, data):
        self.name = data['name']
        self.s3_bucket = data['s3Bucket']
        self.s3_key = data['s3Key']
        self.created_by = data['createdBy']
