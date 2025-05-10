from .serializers import CardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Card
from decimal import Decimal


class TestProtectedView(APIView):
    def get(self, request):
        return Response({"message": f"Hello, {request.user.telegram_id}. You are authenticated!"})


class CardListCreateView(APIView):
    def get(self, request):
        cards = Card.objects.filter(user=request.user)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositView(APIView):
    def post(self, request):
        card_id = request.data.get("card_id")
        amount = request.data.get("amount")

        if not card_id or not amount:
            return Response({"error": "card_id va amount majburiy"}, status=400)

        try:
            card = Card.objects.get(id=card_id, user=request.user)
        except Card.DoesNotExist:
            return Response({"error": "Karta topilmadi yoki sizga tegishli emas"}, status=404)

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError()
        except:
            return Response({"error": "amount noto‘g‘ri kiritilgan"}, status=400)

        card.balance += amount
        card.save()

        return Response({
            "message": "Hisob to‘ldirildi",
            "card_id": card.id,
            "new_balance": card.balance
        }, status=200)


class TransferView(APIView):
    def post(self, request):
        from_card_id = request.data.get("from_card_id")
        to_card_number = request.data.get("to_card_number")
        amount = request.data.get("amount")

        if not all([from_card_id, to_card_number, amount]):
            return Response({"error": "Barcha maydonlar to‘ldirilishi kerak"}, status=400)

        try:
            from_card = Card.objects.get(id=from_card_id, user=request.user)
        except Card.DoesNotExist:
            return Response({"error": "Sizga tegishli karta topilmadi"}, status=404)

        try:
            to_card = Card.objects.get(card_number=to_card_number)
        except Card.DoesNotExist:
            return Response({"error": "Qabul qiluvchi karta topilmadi"}, status=404)

        try:
            amount = Decimal(amount)
            if amount <= 0:
                raise ValueError()
        except:
            return Response({"error": "Miqdor noto‘g‘ri kiritilgan"}, status=400)

        if from_card.balance < amount:
            return Response({"error": "Balans yetarli emas"}, status=400)

        # Pul o‘tkazish
        from_card.balance -= amount
        to_card.balance += amount
        from_card.save()
        to_card.save()

        return Response({
            "message": f"{to_card.card_number} raqamiga {amount} so‘m jo‘natildi",
            "from_card": from_card.card_number,
            "new_balance": from_card.balance
        }, status=200)


class BalanceView(APIView):
    def get(self, request):
        card = Card.objects.filter(user=request.user).first()
        if not card:
            return Response({"error": "Sizda hech qanday karta mavjud emas"}, status=404)

        return Response({
            "card_number": card.card_number,
            "balance": card.balance
        }, status=200)
