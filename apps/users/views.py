from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.users.models import TelegramVerification, User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import random
import requests

@api_view(['POST'])
@permission_classes([AllowAny])
def generate_code(request):
    try:
        telegram_id = request.data.get("telegram_id")
        if not telegram_id:
            return Response({"error": "Telegram ID kerak"}, status=400)

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={"phone_number": ""}
        )

        code = str(random.randint(100000, 999999))
        TelegramVerification.objects.create(user=user, code=code)

        res = requests.post("http://localhost:8081/send_code", json={
            "telegram_id": telegram_id,
            "code": code
        }, headers={"Authorization": "Bearer YOUR_BOT_TOKEN"})
        if res.status_code != 200:
            return Response({"error": res.json()}, status=500)

        return Response({"message": "Kod yuborildi."}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_code(request):
    telegram_id = request.data.get("telegram_id")
    code = request.data.get("code")

    try:
        user = User.objects.get(telegram_id=telegram_id)
        verification = TelegramVerification.objects.filter(user=user, code=code, is_used=False).last()

        if not verification or verification.is_expired():
            return Response({"error": "Code is invalid or expired"}, status=400)

        verification.is_used = True
        verification.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    refresh = request.data.get("refresh")
    if not refresh:
        return Response({"error": "Refresh token kerak"}, status=400)

    try:
        refresh_token = RefreshToken(refresh)
        new_access_token = str(refresh_token.access_token)
        return Response({"access": new_access_token}, status=200)
    except Exception as e:
        return Response({"error": "Refresh token noto‘g‘ri yoki eskirgan"}, status=400)