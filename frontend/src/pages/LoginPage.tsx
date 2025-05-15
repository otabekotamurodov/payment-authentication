import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const BASE_URL = import.meta.env.VITE_API_URL;

function LoginPage() {
  const [telegramId, setTelegramId] = useState("");
  const [code, setCode] = useState("");
  const [step, setStep] = useState<1 | 2>(1);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSendCode = async () => {
    setLoading(true);
    try {
      await axios.post(`${BASE_URL}/api/auth/generate-code/`, {
        telegram_id: Number(telegramId),
      });
      alert("Kod Telegram orqali yuborildi!");
      setStep(2);
    } catch (error: any) {
      console.error("ERROR:", error.response?.data || error.message);
      alert("Xatolik: " + (error.response?.data?.error || "Tizimda muammo"));
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${BASE_URL}/api/auth/verify-code/`, {
        telegram_id: Number(telegramId),
        code: code,
      });

      const { access, refresh } = response.data;
      localStorage.setItem("access_token", access);
      localStorage.setItem("refresh_token", refresh);

      alert("Muvaffaqiyatli tasdiqlandi!");
      navigate("/dashboard");
    } catch (error: any) {
      console.error("ERROR:", error.response?.data || error.message);
      alert("Xatolik: " + (error.response?.data?.error || "Kod noto‘g‘ri yoki muddati tugagan!"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black text-white transition-all">
      <h1 className="text-4xl font-bold mb-6">Telegram Login</h1>
      {step === 1 && (
        <div className="flex flex-col items-center gap-3 w-80">
          <input
            type="text"
            placeholder="Telegram ID"
            className="bg-gray-800 text-white px-3 py-2 rounded w-full"
            value={telegramId}
            onChange={(e) => setTelegramId(e.target.value)}
          />
          <button
            onClick={handleSendCode}
            disabled={loading || !telegramId}
            className="bg-white text-black px-4 py-2 rounded w-full hover:bg-gray-200 transition"
          >
            {loading ? "Yuborilmoqda..." : "Kod yuborish"}
          </button>
        </div>
      )}
      {step === 2 && (
        <div className="flex flex-col items-center gap-3 w-80">
          <input
            type="text"
            placeholder="Telegram kodingiz"
            className="bg-gray-800 text-white px-3 py-2 rounded w-full"
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <button
            onClick={handleVerify}
            disabled={loading}
            className="bg-white text-black px-4 py-2 rounded w-full hover:bg-gray-200 transition"
          >
            {loading ? "Tekshirilmoqda..." : "Tasdiqlash"}
          </button>
        </div>
      )}
    </div>
  );
}

export default LoginPage;