type Props = {
  amount: number;
};

function BalanceCard({ amount }: Props) {
  return (
    <div className="bg-white text-black rounded-xl shadow-md p-4">
      <h2 className="text-xl font-semibold">Balans</h2>
      <p className="text-2xl mt-2">{amount.toLocaleString()} so‘m</p>
    </div>
  );
}

export default BalanceCard;
