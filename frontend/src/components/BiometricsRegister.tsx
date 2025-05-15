// import React from 'react';

// NGROK orqali ochilgan backend link (HTTPS bo'lishi shart!)
const BASE_URL = import.meta.env.VITE_API_URL;

const BiometricsVerify = () => {
  const verify = async () => {
    try {
      // 1. Serverdan Face ID challenge olish
      const res = await fetch(`${BASE_URL}/api/webauthn/begin-authentication/`);
      const options = await res.json();

      // 2. challenge va credentialId’ni dekodlash
      options.publicKey.challenge = Uint8Array.from(atob(options.publicKey.challenge), c => c.charCodeAt(0));
      options.publicKey.allowCredentials = options.publicKey.allowCredentials.map((cred: any) => ({
        ...cred,
        id: Uint8Array.from(atob(cred.id), c => c.charCodeAt(0)),
      }));

      // 3. Face ID (yoki fingerprint) orqali credentialni olish
      const credential = await navigator.credentials.get({
        publicKey: options.publicKey,
      }) as PublicKeyCredential;

      // 4. Credentialni formatlash
      const authData = {
        id: credential.id,
        rawId: btoa(String.fromCharCode(...new Uint8Array(credential.rawId))),
        type: credential.type,
        response: {
          clientDataJSON: btoa(String.fromCharCode(...new Uint8Array(credential.response.clientDataJSON))),
          authenticatorData: btoa(String.fromCharCode(...new Uint8Array(
            (credential.response as AuthenticatorAssertionResponse).authenticatorData
          ))),
          signature: btoa(String.fromCharCode(...new Uint8Array(
            (credential.response as AuthenticatorAssertionResponse).signature
          ))),
        },
      };

      // 5. Credentialni serverga yuborish va tekshirish
      const verifyRes = await fetch(`${BASE_URL}/api/webauthn/finish-authentication/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(authData),
      });

      const result = await verifyRes.json();
      alert(result.message);
    } catch (error) {
      console.error("Face ID orqali tasdiqlashda xatolik:", error);
      alert("Tizimda xatolik yuz berdi. Iltimos, qayta urinib ko‘ring.");
    }
  };

  return (
    <button onClick={verify} className="bg-purple-600 text-white p-3 rounded-lg">
      Face ID bilan to‘lovni tasdiqlash
    </button>
  );
};

export default BiometricsVerify;
