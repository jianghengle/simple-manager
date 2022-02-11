import json
from django.db import models

DEFAULT_CONFIG = {
    'approvalReceivers': [],
    'reviewerMappings': {},
}

# This table should only have one record, 
# which is the web app's global config
# The config is saved on the `config` text field in json format
class MyConfig(models.Model):
    config = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_json(self):
        return json.loads(self.config)

    @staticmethod
    def get_record():
        # Get the only one record from MyConfig table
        # if there is no record, create one with the default config value
        return None
