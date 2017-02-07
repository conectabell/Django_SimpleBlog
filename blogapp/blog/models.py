from django.db import models
from django.utils import timezone

BOOL_CHOICES = (("1", 'Si'), ("0", 'No'))

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    crypt = models.CharField(default="0", max_length=5, choices=BOOL_CHOICES)
    key = models.CharField(max_length=200, null=True, blank=True)
    rekey = models.CharField(max_length=200, null=True, blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


