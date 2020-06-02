import random
import csv
import sys
import json

def _populate_data_lists():
  states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

  with open('first-names.json', 'r') as fp:
    first_names = json.load(fp)

  with open('last-names.json', 'r') as fp:
    last_names = json.load(fp)
  return states, first_names, last_names


def generate_data(rows=1000, csv_file='sample_person_data.csv'):
  '''
  output a csv file with multiple rows of data to be imported into postgres
  id, firstname, lastname, state
  '''
  states, first_names, last_names = _populate_data_lists()
  with open(csv_file, 'w', newline='') as fp:
    writer = csv.writer(fp)

    for number in range(rows):
      row = [random.choice(first_names), random.choice(last_names), random.choice(states)]
      writer.writerow(row)  

if __name__ == '__main__':

  usage = 'USAGE: generate_data.py number_of_rows'
  assert len(sys.argv) == 2, usage
  rows = int(sys.argv[1])
  generate_data(rows=rows)
