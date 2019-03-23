from urllib.parse import urljoin
from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from lastcard.models import User, Card, CardUser
from rest_framework import routers, serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .auth import CsrfExemptSessionAuthentication
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

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
    permission_classes = [AllowAny]

    def list(self, request):
        cards = Card.objects.all()

        for card in cards:
            card.qr_code_url = urljoin(settings.DEFAULT_HOST, '/'.join(['qrcodes',str(card.id)]) + '.svg')

        serializer=CardSerializer(cards, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        # Get logged in user or just show last
        card = self.get_object()
        current_user = request.user
        if request.user.is_authenticated:
            card_user_event = CardUser.objects.filter(card=card, user=current_user).order_by("-created_at").last() # get last
            if card_user_event:
                card_users = User.objects.filter(carduser__id__gte=card_user_event.id, carduser__card_id=card_user_event.card_id)
            else:
                card_users = User.objects.filter(carduser__card_id=card.id).order_by("-carduser__created_at")[:1]
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


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)
