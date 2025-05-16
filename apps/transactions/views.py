from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.transactions.models import Transaction
from apps.users.models import User, TelegramVerification
import random
import requests
from django.core.cache import cache

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_transfer(request):
    recipient_card = request.data.get("recipient_card")
    amount = request.data.get("amount")

    if not recipient_card or not amount:
        return Response({"error": "Karta raqami va summa kerak."}, status=400)

    code = str(random.randint(100000, 999999))
    TelegramVerification.objects.create(user=request.user, code=code)

    try:
        res = requests.post("http://localhost:8081/send_code", json={
            "telegram_id": request.user.telegram_id,
            "code": code
        })
        if res.status_code != 200:
            return Response({"error": "Telegramga yuborishda xatolik: " + res.text}, status=500)
    except Exception as e:
        return Response({"error": f"Telegram yuborishda istisno: {str(e)}"}, status=500)

    # Session o‘rniga cache ishlatish
    cache.set(f"pending_transfer_{request.user.id}", {
        "recipient_card": recipient_card,
        "amount": amount
    }, timeout=300)  # 5 daqiqa muddat

    return Response({"message": "Kod yuborildi"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_transfer(request):
    code = request.data.get("code")
    if not code:
        return Response({"error": "Kod kerak."}, status=400)

    verification = TelegramVerification.objects.filter(user=request.user, code=code, is_used=False).last()
    if not verification or verification.is_expired():
        return Response({"error": "Kod noto‘g‘ri yoki eskirgan."}, status=400)

    verification.is_used = True
    verification.save()

    transfer = cache.get(f"pending_transfer_{request.user.id}")
    if not transfer:
        return Response({"error": "Transfer ma'lumotlari topilmadi."}, status=400)

    Transaction.objects.create(
        user=request.user,
        amount=transfer["amount"],
        type="minus",
        note=f"{transfer['recipient_card']} kartaga o‘tkazma"
    )

    cache.delete(f"pending_transfer_{request.user.id}")  # Cache’dan o‘chirish

    return Response({"message": "Pul o'tkazildi!"}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return Response([{
        "amount": float(t.amount),  # Decimal -> float ga o‘zgartirish
        "type": t.type,
        "note": t.note,
        "date": t.created_at.isoformat()
    } for t in transactions], status=200)