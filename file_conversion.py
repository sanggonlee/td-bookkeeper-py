import glob
import os
import xlrd
import csv
import re

amex_date_regex = re.compile('^[0-9]{2} [a-zA-Z]{3} [0-9]{4}$')


def convert_all_xls(provider='amex'):
    os.chdir('data')
    for file in glob.glob('*.xls'):
        excel_to_csv(filename=file)
    os.chdir('..')


def excel_to_csv(filename, provider='amex'):
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)

    filename_without_ext = '.'.join(filename.split('.')[:-1])
    csv_file = open(filename_without_ext + '.csv', 'w')
    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        if provider is 'amex':
            date, description, _, amount = row
            if not amex_date_regex.match(date):
                # Skip headers
                continue

        wr.writerow(row)

    csv_file.close()
