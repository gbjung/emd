from django.db import models
from accounts.models import Account

class Contact(models.Model):
    sf_id = models.CharField(max_length=250,
                             primary_key=True)
    first_name = models.CharField(max_length=100,
                                  null=True)
    last_name = models.CharField(max_length=100,
                                 null=True)
    middle_name = models.CharField(max_length=100,
                                   null=True)
    title = models.CharField(max_length=100,
                             null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
