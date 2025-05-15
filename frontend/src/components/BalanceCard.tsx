function BalanceCard({ amount, cardNumber }: { amount: number; cardNumber: string }) {
  return (
    <div className="bg-white text-black rounded-xl shadow-md p-4">
      <h2 className="text-xl font-semibold">Balans</h2>
      <p className="text-2xl mt-2">{amount.toLocaleString()} so‘m</p>
      <p className="text-sm text-gray-500 mt-1">Karta: **** **** **** {cardNumber.slice(-4)}</p> {/* Yangi qator */}
    </div>
  );
}


export default BalanceCard;
