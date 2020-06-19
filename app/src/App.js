import React from 'react';
import TransactionList from './components/TransactionList/TransactionList'

function App() {
  return (
    <div>
      <h1>Finance Manager</h1>
      <h3>Upcoming manual </h3>
      <TransactionList listType="manual" />
      <h3>Upcoming automatic transactions</h3>
      <TransactionList listType="auto" />
      <h3>Pending Transactions</h3>
      <TransactionList listType="pending" />
    </div>
  );
}

export default App;