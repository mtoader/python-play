from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class List(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    list = models.ForeignKey(List)
    text = models.TextField()
    due_on = models.DateField(blank=True, null=True)
    started_on = models.DateField(blank=True, null=True)
    priority = models.CharField(
        max_length=1,
        blank=True,
        choices=(
                ('A', 'Urgent and Important'),
                ('B', 'Important but Not Urgent'),
                ('C', 'Neither Urgent nor Important')
            )
    )
    completed = models.BooleanField()

    def __unicode__(self):
        return self.text

    
    class Meta:
        order_with_respect_to = 'list'
