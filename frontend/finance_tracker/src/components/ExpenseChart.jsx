import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './ExpenseChart.css'; // <--- ИМПОРТ СТИЛЕЙ

export default function ExpenseChart() {
  const [data, setData] = useState([
    { day: 'Пн', Потрачено: 1200 },
    { day: 'Вт', Потрачено: 2100 },
    { day: 'Ср', Потрачено: 800 },
    { day: 'Чт', Потрачено: 1600 },
    { day: 'Пт', Потрачено: 3200 },
    { day: 'Сб', Потрачено: 4500 },
    { day: 'Вс', Потрачено: 1900 },
  ]);

  const [amount, setAmount] = useState('');
  const [selectedDay, setSelectedDay] = useState('Пн');

  const handleAddExpense = (e) => {
    e.preventDefault();
    if (!amount || isNaN(amount)) return;

    const updatedData = data.map((item) => {
      if (item.day === selectedDay) {
        return { ...item, Потрачено: item.Потрачено + Number(amount) };
      }
      return item;
    });

    setData(updatedData);
    setAmount('');
  };

  return (
    <div className="tracker-container">
      
      {/* ГРАФИК */}
      <div className="chart-box">
        <h2 className="chart-title">Расходы за неделю</h2>
        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="day" tickLine={false} />
            <YAxis tickLine={false} />
            <Tooltip cursor={{ fill: 'rgba(0, 0, 0, 0.05)' }} />
            <Bar dataKey="Потрачено" fill="#6366f1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* ФОРМА ВВОДА */}
      <form onSubmit={handleAddExpense} className="expense-form">
        <select 
          value={selectedDay} 
          onChange={(e) => setSelectedDay(e.target.value)}
          className="form-select"
        >
          {data.map(item => <option key={item.day} value={item.day}>{item.day}</option>)}
        </select>

        <input 
          type="number" 
          placeholder="Сумма расхода" 
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="form-input"
        />

        <button type="submit" className="form-button">
          Добавить
        </button>
      </form>

    </div>
  );
}