import argparse
import csv
import re
import sys
import glob
import json
from decimal import Decimal

import file_conversion

IS_PYTHON_3 = sys.version_info[0] == 3

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
    print('Month given is invalid')
    sys.exit(0)

files = args.files
target_year = str(args.year)
target_month = str(args.month)
if len(target_month) == 1:
    target_month = '0' + target_month

print('================================================================')
print('Extracting data for month of {} in year {}'.format(
    target_month, target_year))
print('================================================================')


def generateKey(date, desc, outflow, inflow):
    return '{}-{}-{}-{}'.format(date, desc, outflow, inflow)


def accum(results, category, inflow, outflow):
    if outflow != '':
        outflow = outflow.replace(',', '')
        results[category] -= float(outflow)
        results['Total'] -= float(outflow)

    if inflow != '':
        inflow = inflow.replace(',', '')
        results[category] += float(inflow)
        results['Total'] += float(inflow)


def parse_file(file, source):
    reader = csv.reader(file, delimiter=',')
    for idx, row in enumerate(reader):
        if source == 'amex':
            [date, desc, flow, flow2] = row[:5]  # , _, _, _, _, _, _] = row

            # WTF Amex
            if flow == '':
                flow = flow2

            if flow[0] == '-':
                inflow = flow[2:]  # omit - and $
                outflow = '0'
            else:
                inflow = '0'
                outflow = flow[1:]  # omit $

            [day, month, year] = date.split(' ')

            try:
                int(day)
            except:
                continue

            month = month_dict[month]
        elif source == 'td':
            [date, desc, outflow, inflow, _total] = row
            if re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}").match(date):
                [year, month, day] = date.replace('"', '').split('-')
            else:
                [month, day, year] = date.split('/')

        if month != target_month or year != target_year:
            continue

        key = generateKey(date, desc, outflow, inflow)
        if key in seen:
            if file not in seen[key]: # if same key in the same file, treat it as non-duplicate
                seen[key].append(file)
                continue
        else:
            seen[key] = []
        seen[key].append(file)

        matched = None
        for entry in patterns_dict:
            category = entry['label']
            patterns = entry['patterns']
            pattern_regex = '.*(' + '|'.join(patterns) + ').*'
            matched = re.match(pattern_regex, desc)
            if matched is None:
                continue

            print('[{}] Categorizing {} as {} ({}-{})'.format(source,
                                                              desc, category, inflow, outflow))

            accum(results, category, inflow, outflow)
            break

        if matched is None:
            # Couldn't be extracted, enter as a separate column
            print('[{}] Could not categorize {} ({}-{}) ({})'.format(source,
                                                                     desc, inflow, outflow, date))
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

file_conversion.convert_all_xls(provider='amex')

if files is None:
    files = glob.glob('./data/*.csv')

for filename in files:
    with open(filename, 'rt') as file:
        source = 'amex' if 'amex' in filename else 'td'
        parse_file(file, source)

categories.append('Total')

output = ','.join(categories) + '\n'
output += ','.join(
    map(lambda c: str(Decimal(results[c]).quantize(Decimal('1.00'))), categories))

print('================================================================')
print(' OUTPUT')
print('================================================================')
print(output)
