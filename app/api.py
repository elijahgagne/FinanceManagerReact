import falcon
import sqlite3
import json

def testDB():
  conn = sqlite3.connect('/usr/src/FinanceManager.sqlite3')
  conn.row_factory = sqlite3.Row
  db = conn.cursor()
  rows = db.execute('SELECT * FROM transactions').fetchall()
  conn.commit()
  conn.close()
  return json.dumps([dict(i) for i in rows])

class Main(object):
  def __call__(self, req, resp):

    if req.path == '/healthcheck':
      resp.status = falcon.HTTP_200
      resp.body = "OK"
      return
    elif req.path == '/':
      resp.status = falcon.HTTP_200
      resp.body = testDB()
      return
    else:
      resp.status = falcon.HTTP_200
      resp.body = "Sink"
      return

api = falcon.API()
api.add_sink(Main(), prefix='/')
