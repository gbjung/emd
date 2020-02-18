from django.db import models

class Account(models.Model):
    sf_id = models.CharField(max_length=250,
                             primary_key=True)
    account_name = models.CharField(max_length=250)
    unqualified = models.BooleanField(default=False)
    sam_checked = models.BooleanField(default=False)
    sf_updated = models.BooleanField(default=False)
    cage_code = models.CharField(max_length=250,
                                 null=True)
    usa_spending_updated = models.BooleanField(default=False)
    duns_number = models.CharField(max_length=250,
                                   null=True)

    def __str__(self):
        return self.account_name

    def contacts(self):
        return self.contact_set.all()
