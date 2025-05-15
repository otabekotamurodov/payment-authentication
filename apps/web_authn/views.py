from fido2.server import Fido2Server
from fido2.webauthn import PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity
from fido2.utils import websafe_encode, websafe_decode
from fido2.webauthn import AttestationObject
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json
from fido2.webauthn import CollectedClientData

# RP – Relying Party (sayt ma'lumotlari)
rp = PublicKeyCredentialRpEntity(id="localhost", name="My Payment System")
server = Fido2Server(rp)

# Faqat test uchun, prod uchun Redis, Postgres, yoki cache ishlat
credentials_db = {}
challenges = {}

User = get_user_model()


@csrf_exempt
def begin_registration(request):
    user = request.user  # yoki token orqali olish
    if not user.is_authenticated:
        return HttpResponseBadRequest("User not authenticated")

    user_entity = PublicKeyCredentialUserEntity(
        id=str(user.id).encode(),
        name=user.username,
        display_name=user.username
    )

    registration_data, state = server.register_begin(
        user=user_entity,
        credentials=credentials_db.get(user.id, []),
        user_verification="required"
    )

    # Challenge’ni saqlab qo‘yamiz (prod: DB)
    challenges[user.id] = state

    return JsonResponse(registration_data)


@csrf_exempt
def finish_registration(request):
    user = request.user  # yoki token orqali olish
    if not user.is_authenticated:
        return HttpResponseBadRequest("User not authenticated")

    body = json.loads(request.body)

    try:
        att_obj = AttestationObject(websafe_decode(body["response"]["attestationObject"]))
        client_data = CollectedClientData(websafe_decode(body["response"]["clientDataJSON"]))
    except Exception as e:
        return HttpResponseBadRequest(f"Decoding error: {e}")

    state = challenges.get(user.id)
    if not state:
        return HttpResponseBadRequest("Challenge not found")

    auth_data = server.register_complete(
        state=state,
        client_data=client_data,
        attestation_object=att_obj
    )

    # Credential’ni userga bog‘laymiz
    credentials_db.setdefault(user.id, []).append(auth_data.credential_data)

    return JsonResponse({"status": "ok", "message": "Credential saqlandi"})


@csrf_exempt
def begin_authentication(request):
    user = request.user  # yoki token orqali
    if not user.is_authenticated:
        return HttpResponseBadRequest("User not authenticated")

    credentials = credentials_db.get(user.id, [])
    auth_data, state = server.authenticate_begin(
        credentials=credentials,
        user_verification="required"
    )

    challenges[user.id] = state  # Auth uchun alohida key ishlatish mumkin

    return JsonResponse(auth_data)


@csrf_exempt
def finish_authentication(request):
    user = request.user  # yoki token orqali
    if not user.is_authenticated:
        return HttpResponseBadRequest("User not authenticated")

    body = json.loads(request.body)
    credential_id = websafe_decode(body["id"])
    client_data = CollectedClientData(websafe_decode(body["response"]["clientDataJSON"]))
    # authenticator_data = websafe_decode(body["response"]["authenticatorData"])
    authenticator_data: bytes = websafe_decode(body["response"]["authenticatorData"])
    signature = websafe_decode(body["response"]["signature"])

    state = challenges.get(user.id)
    if not state:
        return HttpResponseBadRequest("Challenge not found")

    credentials = credentials_db.get(user.id, [])
    auth_data = server.authenticate_complete(
        state,
        credentials,
        credential_id,
        client_data,
        authenticator_data,
        signature
    )

    # Agar shu yerga yetgan bo‘lsa — Face ID muvaffaqiyatli
    return JsonResponse({"status": "ok", "message": "Face ID tasdiqlandi"})
