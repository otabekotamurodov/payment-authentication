import { useEffect, useState } from 'react';
import axios from 'axios';

function DashboardPage() {
  const [balance, setBalance] = useState<number | null>(null);
  const [transactions, setTransactions] = useState<any[]>([]);

  const token = localStorage.getItem('access_token');

  useEffect(() => {
    if (!token) {
      window.location.href = '/';
    }

    axios.get('http://localhost:8000/api/account/balance/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => setBalance(res.data.balance))
    .catch(err => console.error('Balansni olishda xatolik:', err));

    axios.get('http://localhost:8000/api/transactions/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => setTransactions(res.data))
    .catch(err => console.error('Transactionlarda xatolik:', err));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 p-6">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

      <div className="bg-white rounded shadow p-4 mb-6">
        <h2 className="text-xl font-semibold">Balans</h2>
        <p className="text-3xl text-green-600">
          {balance !== null ? `${balance.toLocaleString()} so'm` : 'Yuklanmoqda...'}
        </p>
      </div>

      <div className="bg-white rounded shadow p-4">
        <h2 className="text-xl font-semibold mb-2">So‘nggi tranzaksiyalar</h2>
        {transactions.length === 0 ? (
          <p>Hali hech qanday tranzaksiya yo‘q.</p>
        ) : (
          <ul className="space-y-2">
            {transactions.map((txn, index) => (
              <li key={index} className="border-b pb-2">
                {txn.amount} so‘m → {txn.to_card?.owner_name || 'Noma’lum'}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default DashboardPage;
