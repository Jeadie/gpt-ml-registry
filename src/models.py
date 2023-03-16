import datetime 

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, JSONAttribute


class ModelTable(Model):
    """
    DynamoDB table for storing metadata about machine learning models
    """
    class Meta:
        table_name = 'model-table'
        region = 'us-east-1'
    model_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    created_at = UTCDateTimeAttribute(default=datetime.utcnow())
    last_updated_at = UTCDateTimeAttribute(default=datetime.utcnow())
    version = NumberAttribute(default=1)
    tags = JSONAttribute(null=True)
