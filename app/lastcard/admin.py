from django.contrib import admin
from .models import Card

class CardAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        return super(CardAdmin, self).save_model(request, obj, form, change)

admin.site.register(Card, CardAdmin)