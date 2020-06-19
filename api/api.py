import falcon
import sqlite3
import json
import os
from datetime import datetime, date, timedelta

def execute_query(query, params=[], wrap_array=True):
  conn = sqlite3.connect(os.environ['DB_FILE'])
  conn.row_factory = sqlite3.Row
  db = conn.cursor()
  rows = db.execute(query, params).fetchall()
  conn.commit()
  conn.close()
  data = [dict(i) for i in rows]
  if len(data) == 1:
    if wrap_array:
      return json.dumps([data[0]])
    else:
      return json.dumps(data[0])
  else:
    return json.dumps(data)

class HealthCheck():
  def on_get(self, req, resp):
    resp.body = "OK"

class Transactions():
  def on_get(self, req, resp):
    if req.relative_uri == '/api/transactions?next_auto=1':
      resp.status = falcon.HTTP_200
      resp.body = execute_query("SELECT * FROM transactions WHERE status = 'automatic' AND submit_date < '" + str(date.today() + timedelta(days=30)) + "'")
    elif req.relative_uri == '/api/transactions?next_manual=1':
      resp.status = falcon.HTTP_200
      resp.body = execute_query("SELECT * FROM transactions WHERE status = 'manual' AND submit_date < '" + str(date.today() + timedelta(days=30)) + "'")
    elif req.relative_uri == '/api/transactions?pending=1':
      resp.status = falcon.HTTP_200
      resp.body = execute_query("SELECT * FROM transactions WHERE status = 'pending'")
    else:
      resp.status = falcon.HTTP_200
      resp.body = execute_query("SELECT * FROM transactions")

  def on_post(self, req, resp):
    data = req.media
    sql = "INSERT INTO transactions (name, payment_method, amount, submit_date, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))"
    try:
      params = [data['name'], data['payment_method'], data['amount'], data['submit_date'], data['status']]
      execute_query(sql, params)
      result = execute_query("SELECT * FROM transactions WHERE id = (SELECT MAX(id) FROM transactions)", [])
      if result == '[]':
        raise falcon.BadRequest()
      else:
        resp.status = falcon.HTTP_201
        resp.body = result
    except:
      raise falcon.HTTPBadRequest()

class OneTransaction():
  def on_get(self, req, resp, id):
    result = execute_query("SELECT * FROM transactions WHERE id = ?", [id], False)
    if result == '[]':
      raise falcon.HTTPNotFound()
    else:
      resp.status = falcon.HTTP_200
      resp.body = result

  def on_put(self, req, resp, id):
    data = req.media
    sql = "UPDATE transactions SET name = ?, payment_method = ?, amount = ?, submit_date = ?, status = ?, updated_at = datetime('now', 'localtime') WHERE id = ?"
    try:
      params = [data['name'], data['payment_method'], data['amount'], data['submit_date'], data['status'], id]
      execute_query(sql, params)
      result = execute_query("SELECT * FROM transactions WHERE id = ?", [id], False)
      if result == '[]':
        raise falcon.BadRequest()
      else:
        resp.status = falcon.HTTP_200
        resp.body = result
    except:
      raise falcon.HTTPBadRequest()

  def on_delete(self, req, resp, id):
    result = execute_query("SELECT * FROM transactions WHERE id = ?", [id], False)
    if result == '[]':
      raise falcon.HTTPNotFound()
    else:
      try:
        execute_query("DELETE FROM transactions WHERE id = ?", [id])
        resp.status = falcon.HTTP_200
        resp.body = result
      except:
        raise falcon.HTTPBadRequest()

api = falcon.API()
api.add_route('/healthcheck', HealthCheck())
api.add_route('/api/transactions', Transactions())
api.add_route('/api/transactions/{id:int}', OneTransaction())
