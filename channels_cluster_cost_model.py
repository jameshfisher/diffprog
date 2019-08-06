import ad
import optimize
import csv
import datetime

rows = []
with open('channels_clusters_costs.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    rows.append({
      'start_date': datetime.datetime.strptime(row['start_date'], '%Y-%m-%d'),
      'end_date': datetime.datetime.strptime(row['end_date'], '%Y-%m-%d'),
      'aws_cost': float(row['aws_cost']),
      'kconns': float(row['peak_connections']) / 1000,
      'mmsgs': float(row['total_billed_messages']) / 1000000,
    })

def square(x):
  return x*x
def loss(fixed_cost, dollars_per_mmsg, dollars_per_kconn_day):
  err = 0
  for row in rows:
    row_days = (row['end_date'] - row['start_date']).days
    kconn_days = row['kconns'] * row_days
    prediction = fixed_cost
    prediction = prediction + row['mmsgs'] * dollars_per_mmsg
    prediction = prediction + kconn_days * dollars_per_kconn_day
    err = err + square(row['aws_cost']-prediction)
  return err

params = optimize.gradient_descent(loss, [100, 0.0001, 0.0001], learning_rate=0.000000000001)
print(params)