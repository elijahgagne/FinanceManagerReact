import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import classes from './TransactionList.module.css';
import axios from 'axios';
import { format } from "date-fns";

function TransactionList(props) {
  const [data, setData] = useState([]);
  const location = useLocation();

  useEffect(() => {
    const fetchData = async () => {
      let url = ''
      if (props.listType == "manual") {
        url = 'http://localhost:8080/api/transactions?next_manual=1'
      } else if (props.listType == "auto") {
        url = 'http://localhost:8080/api/transactions?next_auto=1'
      } else if (props.listType == "pending") {
        url = 'http://localhost:8080/api/transactions?pending=1'
      } else {
        url = 'http://localhost:8080/api/transactions'
      }
      const result = await axios(
        url,
      );
      setData(result.data);
    };
    fetchData();
  }, [location]);

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Name</th>
            <th>Amount</th>
            <th>Payment Method</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
          <tr key={item.id}>
            <td>{format(new Date(item.submit_date.substring(0, 10)), "MMMM dd")}</td>
            <td>{item.name}</td>
            <td>{item.amount}</td>
            <td>{item.payment_method}</td>
            <td>Edit</td>
          </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionList;