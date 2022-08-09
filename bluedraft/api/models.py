from django.db import models
from django.utils import timezone


class Coin(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(editable=False)
    date_updated = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.date_updated = timezone.now()
        return super(Coin, self).save(*args, **kwargs)
