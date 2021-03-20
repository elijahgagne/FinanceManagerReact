import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import TransactionList from './components/TransactionList/TransactionList'

function App() {
  return (
    <div>
      <h1>Finance Manager</h1>
      <Router>
        <Switch>
          <Route path="/transactions">
            <Link to="/">Home</Link>
            <h3>All transactions</h3>
            <TransactionList />
          </Route>
          <Route path="/">
            <Link to="/transactions">All transactions</Link>
            <h3>Upcoming manual </h3>
            <TransactionList listType="manual" />
            <h3>Upcoming automatic transactions</h3>
            <TransactionList listType="auto" />
            <h3>Pending Transactions</h3>
            <TransactionList listType="pending" />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;