from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.users.models import TelegramVerification, User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from bot.config import BOT_TOKEN
import random
import traceback

bot = Bot(token=BOT_TOKEN)

@api_view(['POST'])
@permission_classes([AllowAny])
def generate_code(request):
    try:
        print("REQUEST DATA:", request.data)
        telegram_id = request.data.get("telegram_id")
        if not telegram_id:
            return Response({"error": "Telegram ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        telegram_id = int(telegram_id)

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={"phone_number": f"998000000000"}
        )
        print(f"USER: {user}, CREATED: {created}")

        # Code generation
        code = str(random.randint(100000, 999999))
        TelegramVerification.objects.create(user=user, code=code)

        # Send code via Telegram
        import asyncio
        asyncio.run(
            bot.send_message(
                chat_id=user.telegram_id,
                text=f"<b>Sizning tasdiqlash kodingiz:</b> <code>{code}</code>\n\nKod 5 daqiqa amal qiladi.",
                parse_mode=ParseMode.HTML
            )
        )

        return Response({"message": "Kod Telegram orqali yuborildi!"}, status=status.HTTP_200_OK)

    except Exception as e:
        print("ERROR:", str(e))
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_code(request):
    telegram_id = request.data.get("telegram_id")
    code = request.data.get("code")
    print("VERIFY REQUEST:", telegram_id, code)

    try:
        user = User.objects.get(telegram_id=telegram_id)
        print("USER:", user)
        verification = TelegramVerification.objects.filter(user=user, code=code, is_used=False).last()
        print("VERIFICATION:", verification)

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
