from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.users.models import TelegramVerification, User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import random
import traceback



@api_view(['POST'])
def generate_code(request):
    try:
        print("REQUEST DATA:", request.data)
        telegram_id = request.data.get("telegram_id")
        if not telegram_id:
            return Response({"error": "Telegram ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        # Type casting to int, just in case
        telegram_id = int(telegram_id)
        # User create with minimal fields
        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={"phone_number": f"998000000000"}
        )
        print(f"USER: {user}, CREATED: {created}")
        # Code generation
        code = str(random.randint(100000, 999999))
        TelegramVerification.objects.create(user=user, code=code)

        return Response({"message": f"Verification code generated: {code}"}, status=status.HTTP_200_OK)

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
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
