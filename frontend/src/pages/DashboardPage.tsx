import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "@/api"; // api.ts dan import qilindi
import WelcomeHeader from "@/components/WelcomeHeader";
import BalanceCard from "@/components/BalanceCard";
import TransactionsList from "@/components/TransactionsList";

function DashboardPage() {
  const [balance, setBalance] = useState(0);
  const [cardNumber, setCardNumber] = useState("");
  const [transactions, setTransactions] = useState([]);
  const [recipientCard, setRecipientCard] = useState("");
  const [amount, setAmount] = useState("");
  const [verifyCode, setVerifyCode] = useState("");
  const [isAwaitingCode, setIsAwaitingCode] = useState(false);
  const [accessToken] = useState<string | null>(localStorage.getItem("access_token"));
  const navigate = useNavigate();

  useEffect(() => {
    if (!accessToken) {
      console.warn("Access token yo‘q. Foydalanuvchi login qilmagan.");
      navigate("/login");
      return;
    }

    const fetchData = async () => {
      try {
        const [balanceRes, transRes] = await Promise.all([
          api.get("/api/account/balance/"), // api.ts ishlatildi, headers qo‘shish shart emas
          api.get("/api/transactions/"), // api.ts ishlatildi
        ]);
        setBalance(balanceRes.data.balance);
        setCardNumber(balanceRes.data.card_number);
        setTransactions(transRes.data);
      } catch (error) {
        console.error("Xatolik yuz berdi:", error);
        alert("Ma’lumotlarni yuklashda xatolik yuz berdi!");
      }
    };

    fetchData();
  }, [accessToken, navigate]);

  const handleTransferRequest = async () => {
    try {
      await api.post("/api/transactions/request-transfer/", {
        recipient_card: recipientCard,
        amount: parseFloat(amount),
      }); // api.ts ishlatildi
      setIsAwaitingCode(true);
      alert("Telegram orqali tasdiqlash kodi yuborildi");
    } catch (error) {
      console.error("Pul o‘tkazish so‘rovida xatolik:", error);
      alert("Xatolik: Pul o‘tkazish kodi yuborilmadi");
    }
  };

  const handleTransferConfirm = async () => {
    try {
      await api.post("/api/transactions/confirm-transfer/", {
        code: verifyCode,
      }); // api.ts ishlatildi, withCredentials avtomatik qo‘shilgan
      alert("Pul o‘tkazmasi muvaffaqiyatli amalga oshdi");
      setIsAwaitingCode(false);
      setRecipientCard("");
      setAmount("");
      setVerifyCode("");
    } catch (error) {
      console.error("Tasdiqlashda xatolik:", error);
      alert("Xatolik: Noto‘g‘ri yoki eskirgan kod");
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-6">
      <WelcomeHeader />
      <div className="grid gap-6">
        <BalanceCard amount={balance} cardNumber={cardNumber} />

        {/* Pul o'tkazish formasi */}
        <div className="bg-gray-800 p-4 rounded-lg">
          <h3 className="text-lg font-bold mb-2">Pul o‘tkazish</h3>
          <input
            type="text"
            placeholder="Qabul qiluvchining karta raqami"
            className="w-full mb-2 px-3 py-1 text-black rounded"
            value={recipientCard}
            onChange={(e) => setRecipientCard(e.target.value)}
          />
          <input
            type="number"
            placeholder="Summani kiriting"
            className="w-full mb-2 px-3 py-1 text-black rounded"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />

          {!isAwaitingCode ? (
            <button
              onClick={handleTransferRequest}
              className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white"
            >
              O‘tkazish uchun kod so‘rash
            </button>
          ) : (
            <div className="mt-3">
              <input
                type="text"
                placeholder="Telegram kodingizni kiriting"
                className="w-full mb-2 px-3 py-1 text-black rounded"
                value={verifyCode}
                onChange={(e) => setVerifyCode(e.target.value)}
              />
              <button
                onClick={handleTransferConfirm}
                className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded text-white"
              >
                Tasdiqlash
              </button>
            </div>
          )}
        </div>

        <h3 className="text-xl font-semibold mt-6">So‘nggi tranzaksiyalar</h3>
        <TransactionsList transactions={transactions} />
      </div>
    </div>
  );
}

export default DashboardPage;