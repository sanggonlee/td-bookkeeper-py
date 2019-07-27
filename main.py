import argparse
import csv
import re
import sys
import glob
import json

month_dict = {
  'Jan': '01',
  'Feb': '02',
  'Mar': '03',
  'Apr': '04',
  'May': '05',
  'Jun': '06',
  'Jul': '07',
  'Aug': '08',
  'Sep': '09',
  'Oct': '10',
  'Nov': '11',
  'Dec': '12'
}

parser = argparse.ArgumentParser(description='Takes month and year')
parser.add_argument('year', metavar='y', type=int)
parser.add_argument('month', metavar='m', type=int)
parser.add_argument('--files', nargs='+')
args = parser.parse_args()
if args.month < 1 or args.month > 12:
  print 'Month given is invalid'
  sys.exit(0)

files = args.files
target_year = str(args.year)
target_month = str(args.month)
if len(target_month) == 1:
  target_month = '0' + target_month

print '================================================================'
print 'Extracting data for month of {} in year {}'.format(target_month, target_year)
print '================================================================'

def generateKey(date, desc, outflow, inflow):
  return '{}-{}-{}-{}'.format(date, desc, outflow, inflow)

def accum(results, category, inflow, outflow):
  if outflow != '':
    results[category] -= float(outflow)
    results['Total'] -= float(outflow)
  
  if inflow != '':
    results[category] += float(inflow)
    results['Total'] += float(inflow)

def parse_file(file, source):
  reader = csv.reader(file, delimiter=',')
  for row in reader:
    if source == 'amex':
      [date, desc, inflow, outflow] = row
      inflow = inflow[1:]
      outflow = outflow[1:]
      [day, month, year] = date.split(' ')
      month = month_dict[month]
    elif source == 'td':
      [date, desc, outflow, inflow, _total] = row
      [month, day, year] = date.split('/')

    if month != target_month or year != target_year:
      continue

    key = generateKey(date, desc, outflow, inflow)
    if key in seen:
      continue

    seen[key] = True

    matched = None
    for entry in patterns_dict:
      category = entry['label']
      patterns = entry['patterns']
      pattern_regex = '.*(' + '|'.join(patterns) + ').*'
      matched = re.match(pattern_regex, desc)
      if matched is None:
        continue

      print 'Categorizing {} as {} ({}-{})'.format(desc, category, inflow, outflow)

      accum(results, category, inflow, outflow)
      break
    
    if matched is None:
      # Couldn't be extracted, enter as a separate column
      print 'Could not categorize {} ({}-{}) ({})'.format(desc, inflow, outflow, date)
      if desc not in results:
        results[desc] = 0
        categories.append(desc)
      accum(results, desc, inflow, outflow)

with open('patterns.json', 'r') as patterns_file:
  patterns_dict = json.load(patterns_file)

categories = []
seen = {}
results = {
  'Total': 0
}

for entry in patterns_dict:
  category = entry['label']
  categories.append(category)
  if category not in results:
    results[category] = 0

if files is None:
  files = glob.glob('./data/*.csv')
for filename in files:
  with open(filename, 'rb') as file:
    source = 'amex' if 'amex' in filename else 'td'
    parse_file(file, source)

categories.append('Total')

output = ','.join(categories) +'\n'
output += ','.join(map(lambda c: str(results[c]), categories))

print '================================================================'
print ' OUTPUT'
print '================================================================'
print output

    







