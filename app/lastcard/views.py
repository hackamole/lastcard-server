from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from lastcard.models import User, Card, CardUser
from rest_framework import routers, serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .auth import CsrfExemptSessionAuthentication


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name', 'mobile', 'email', 'birthday', 'url', 'social_profile')


class CardSerializer(serializers.ModelSerializer):
    original_user = UserSerializer()
    current_user = UserSerializer()
    class Meta:
        model = Card
        fields = "__all__"

class CardsSerializer(CardSerializer):
    users = UserSerializer(many=True)

# ViewSets define the view behavior.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        # Get logged in user or just show last
        card = self.get_object()
        current_user = request.user
        if request.user.is_authenticated:
            card_user_event = CardUser.objects.filter(card=card, user=current_user).order_by("-created_at").last() # get last
            card_users = User.objects.filter(carduser__id__gte=card_user_event.id, carduser__card_id=card_user_event.card_id)
        else:
            card_users = User.objects.filter(carduser__card_id=card.id).order_by("-carduser__created_at")[:1]

        serializer = CardSerializer(card)
        card_data = serializer.data
        card_data["users"] = UserSerializer(card_users, many=True).data
        return Response(card_data)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated], authentication_classes=[CsrfExemptSessionAuthentication, TokenAuthentication])
    def takeover(self, request, pk=None):
        card = self.get_object()
        current_user = request.user

        card.current_user = current_user
        card.save()

        card_user = CardUser(card_id=card.id, user=current_user)
        card_user.save()

        return Response(status=status.HTTP_201_CREATED)
