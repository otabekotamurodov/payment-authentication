import { useEffect, useState } from "react";
import axios from "axios";
import WelcomeHeader from "@/components/WelcomeHeader";
import BalanceCard from "@/components/BalanceCard";
import TransactionsList from "@/components/TransactionsList";

function DashboardPage() {
  const [balance, setBalance] = useState(0);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const accessToken = localStorage.getItem("access_token");

    const fetchData = async () => {
      try {
        const balanceRes = await axios.get("http://localhost:8000/api/account/balance/", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        setBalance(balanceRes.data.balance);

        const transRes = await axios.get("http://localhost:8000/api/transactions/", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        setTransactions(transRes.data);
      } catch (error) {
        console.error("Xatolik yuz berdi:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-black text-white p-6">
      <WelcomeHeader />
      <div className="grid gap-6">
        <BalanceCard amount={balance} />
        <h3 className="text-xl font-semibold mt-6">So‘nggi tranzaksiyalar</h3>
        <TransactionsList transactions={transactions} />
      </div>
    </div>
  );
}

export default DashboardPage;
