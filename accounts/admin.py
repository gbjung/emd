from django.contrib import admin
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'unqualified', 'sam_checked', 'sf_updated', 'contacts')
    def get_queryset(self, obj):
        qs = super(AccountAdmin, self).get_queryset(obj)
        return qs.prefetch_related('contact_set')

    def contacts(self, obj):
        return len(obj.contact_set.all())

admin.site.register(Account, AccountAdmin)
