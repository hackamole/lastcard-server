from django.contrib import admin
from .models import Card, User, CardUser

class CardAdmin(admin.ModelAdmin):
    # TODO generate n cards
    # TODO associate user to card
    # TODO custom takeoveraction
    list_display = ('id', 'original_user', 'current_user', 'created_at', 'modified_at')

    def response_add(self, request, obj, post_url_continue='../%s/'):
        if obj and obj.id:
            # Add Card User
            card_user = CardUser(card_id=obj.id, user=request.user)
            card_user.save()
        return super(CardAdmin, self).response_add(request, obj, post_url_continue=post_url_continue)

    def response_change(self, request, obj):
        if obj and obj.id and obj.current_user:
            # Check last user of card
            last_card_user = CardUser.objects.filter(card_id=obj.id).order_by("-created_at").first()
            if last_card_user and last_card_user.user_id != obj.current_user:
                card_user = CardUser(card_id=obj.id, user=obj.current_user)
                card_user.save()
        return super(CardAdmin, self).response_change(request, obj)

    def save_model(self, request, obj, form, change):
        return super(CardAdmin, self).save_model(request, obj, form, change)

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Card, CardAdmin)
