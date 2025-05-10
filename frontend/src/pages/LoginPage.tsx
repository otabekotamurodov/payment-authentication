// File: frontend/src/pages/LoginPage.tsx

import { useState } from "react";
import axios from "axios";

function LoginPage() {
  const [telegramId, setTelegramId] = useState("");
  const [code, setCode] = useState("");
  const [step, setStep] = useState(1); // 1: Telegram ID, 2: Code

  const handleSendCode = async () => {
    try {
      await axios.post("http://localhost:8000/api/auth/generate-code/", {
        telegram_id: Number(telegramId),
      });
      alert("Kod Telegram orqali yuborildi!");
      setStep(2);
    } catch (error: any) {
      console.error("ERROR:", error);
      alert("Xatolik: " + (error.response?.data?.error || "Tizimda muammo"));
    }
  };

  const handleVerify = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/auth/verify-code/", {
        telegram_id: Number(telegramId),
        code: code,
      });

      const { access, refresh } = response.data;

      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);

      alert("Muvaffaqiyatli tasdiqlandi!");
      window.location.href = "/dashboard";
    } catch (error: any) {
      console.error("ERROR:", error);
      console.log("Javob: ", error.response?.data);
      alert("Xatolik: " + (error.response?.data?.error || "Kod noto‘g‘ri yoki muddati tugagan!"));
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black text-white">
      <h1 className="text-4xl font-bold mb-8">Telegram Login</h1>

      {step === 1 && (
        <div className="flex gap-2">
          <input
            className="bg-gray-800 text-white px-2 py-1"
            type="text"
            placeholder="Telegram ID"
            value={telegramId}
            onChange={(e) => setTelegramId(e.target.value)}
          />
          <button
            onClick={handleSendCode}
            className="bg-white text-black px-4 py-1 rounded"
          >
            Kodni yuborish
          </button>
        </div>
      )}

      {step === 2 && (
        <div className="flex gap-2">
          <input
            className="bg-gray-800 text-white px-2 py-1"
            type="text"
            placeholder="Kod"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <button
            onClick={handleVerify}
            className="bg-white text-black px-4 py-1 rounded"
          >
            Tasdiqlash
          </button>
        </div>
      )}
    </div>
  );
}

export default LoginPage;
