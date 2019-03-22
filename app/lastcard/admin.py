from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Card, User, CardUser
from .qrcode import generate as generate_qrcode

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
    

@receiver(post_save, sender=Card, dispatch_uid="create_qrcode")
def create_qrcode(sender, instance, **kwargs):
    generate_qrcode(settings.DEFAULT_HOST, settings.QRCODE_IMAGES_PATH, str(instance.id))

class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'password', 'address', 'country', 'birthday', 'company', 'role', 'mobile', 'url', 'social_profile')
    pass

class CardUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(CardUser, CardUserAdmin)