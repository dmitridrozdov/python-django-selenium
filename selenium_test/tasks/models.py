from django.db import models


# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200, default='<add tests>')
    test_name = models.CharField(max_length=200, default='runtest')
    result = models.CharField(max_length=200, blank=True)
    log = models.CharField(max_length=1000, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.test_name
