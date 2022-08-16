from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Wallet(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)


class Coin(models.Model):
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True, blank=True, related_name='coins')

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.date_updated = timezone.now()
        return super(Coin, self).save(*args, **kwargs)
