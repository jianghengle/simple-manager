from django.db import models

class Cost(models.Model):
    subject = models.CharField(max_length=512, default='')
    description = models.TextField(default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=512, default='')
    status = models.CharField(max_length=64, default='')
    closed_by = models.CharField(max_length=512, default='', blank=True)
    reviewers = models.TextField(default='', blank=True)
    amount = models.FloatField(default=0.0)
    tags = models.TextField(default='', blank=True)
    comment = models.TextField(default='', blank=True)
    attachments = models.TextField(default='', blank=True)
    last_updated_by = models.CharField(max_length=512, default='', blank=True)

    def to_json(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'description': self.description,
            'createdAt': self.created_at.timestamp(),
            'updatedAt': self.updated_at.timestamp(),
            'createdBy': self.created_by,
            'status': self.status,
            'closedBy': self.closed_by,
            'reviewers': self.reviewers,
            'amount': self.amount,
            'tags': self.tags,
            'comment': self.comment,
            'attachments': self.attachments,
            'lastUpdatedBy': self.last_updated_by,
        }

    def from_json(self, data):
        self.subject = data['subject']
        self.description = data['description']
        self.created_by = data['createdBy']
        self.status = data['status']
        self.closed_by = data['closedBy']
        self.reviewers = data['reviewers']
        self.amount = data['amount']
        self.tags = data['tags']
        self.comment = data['comment']
        self.attachments = data['attachments']
