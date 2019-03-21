import uuid
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=datetime.now)
    modified_at = models.DateTimeField(default=datetime.now)
    card_url = models.URLField()
    qr_code_url = models.URLField()
    original_user = models.ForeignKey(User,on_delete=models.PROTECT, related_name="original_user")
    current_user = models.ForeignKey(User,on_delete=models.PROTECT, related_name="current_user")

class CardUser(models.Model):
    card_id = models.ForeignKey(Card, on_delete=models.PROTECT)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=datetime.now)
