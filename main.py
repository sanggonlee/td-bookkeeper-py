import argparse
import csv
import re
import sys

patterns = (
  ("Pay", 'UNCHARTED .*PAY'),
  ("Tax", '.*TAX.*'),
  ("Mort/Maint", ".*(T\.S\.C\.C\.2448|GENESIS HOME SERVICES|MTGE).*"),
  ("Cash Withdrawl", ".* ATM *W/D"),
  ("E-Transfer", "E-TRANSFER.*"),
  ("Transfer", ".*(TFR-TO C/C|PAYMENT - THANK YOU).*"),
  ("Food", ".*(RESTAUR|RICE|NOODL|METRO|SUBWAY|RAMEN|P\.A\.T|MCDONALD|RITUAL|FRESHCO|DOO ROO AE|LCBO|EATERY|GRILL|TIM HORTONS|KFC|SUSHI|NURI VILLAGE|LEVETTO|KEN OH).*"),
  ("Transportation", ".*(PRESTO|UNION BUS|BIKE SHARE TORONTO).*"),
  ("Travel", ".*(AIR CAN|AIRBNB|HOTEL|TOUR TRAIN).*"),
  ("Internet/Phone", ".*(FIDO).*"),
  ("Charity", ".*(UW OFFICE OF ADVANCEME).*"),
  ("Amazon", ".*(Amazon|AWS).*"),
  ("Medical", ".*(OPTOMETRY|DENTAL).*"),
  ("Bank", ".*(BALANCE PROTECTION|ACCT BAL REBATE|MONTHLY ACCOUNT FEE).*"),
  ("OSAP", ".*(NSLSC).*"),
  ("Etc", ".*(STEAMGAMES|YOUR DOLLAR|WISH\.COM|WAL-MART|DOLLARAMA|MILL|HUDSON'S BAY|REXALL|PEACE OF MIND).*")
)

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

print 'Extracting data for month of {} in year {}'.format(target_month, target_year)

def accum(results, category, inflow, outflow):
  if outflow != '':
    results[category] -= float(outflow)
    results['Total'] -= float(outflow)
  
  if inflow != '':
    results[category] += float(inflow)
    results['Total'] += float(inflow)

def parse_file(file):
  reader = csv.reader(file, delimiter=',')
  for row in reader:
    [date, desc, outflow, inflow, _total] = row
    [month, day, year] = date.split('/')

    if month != target_month or year != target_year:
      continue

    matched = None
    for category, pattern in patterns:
      matched = re.match(pattern, desc)
      if matched is None:
        continue

      print 'Categorizing {} as {}'.format(desc, category)

      accum(results, category, inflow, outflow)
      break
    
    if matched is None:
      # Couldn't be extracted, enter as a separate column
      print 'Could not categorize {}'.format(desc)
      if desc not in results:
        results[desc] = 0
        categories.append(desc)
      accum(results, desc, inflow, outflow)

categories = []
results = {
  'Total': 0
}
for category, pattern in patterns:
  categories.append(category)
  if category not in results:
    results[category] = 0

for filename in files:
  with open(filename, 'rb') as file:
    parse_file(file)

categories.append('Total')

output = ','.join(categories) +'\n'
output += ','.join(map(lambda c: str(results[c]), categories))

print '================================================================'
print ' OUTPUT'
print '================================================================'
print output

    







