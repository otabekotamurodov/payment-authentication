type Transaction = {
  id: number;
  amount: number;
  type: "plus" | "minus";
  description: string;
};

type Props = {
  transactions: Transaction[];
};

function TransactionsList({ transactions }: Props) {
  if (transactions.length === 0) {
    return <p className="text-gray-300 mt-4">Hali hech qanday tranzaksiya yo‘q.</p>;
  }

  return (
    <ul className="mt-4 space-y-2">
      {transactions.map((tx) => (
        <li key={tx.id} className="bg-gray-800 p-3 rounded-lg">
          <div className="flex justify-between">
            <span>{tx.description}</span>
            <span
              className={tx.type === "plus" ? "text-green-400" : "text-red-400"}
            >
              {tx.type === "plus" ? "+" : "-"}
              {tx.amount.toLocaleString()} so‘m
            </span>
          </div>
        </li>
      ))}
    </ul>
  );
}

export default TransactionsList;
