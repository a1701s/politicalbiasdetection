import csv
import sys

maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

filename = "data/articles3.csv"
rows = []

with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)
    
    for row in csvreader:
        rows.append(row)

def assign_leaning(publication):
    leanings = {
        'Atlantic': 'left', #
        'Breitbart': 'right', #
        'Business Insider': 'left', #
        'Buzzfeed News': 'left', #
        'CNN': 'left', #
        'Fox News': 'right', #
        'Guardian': 'left', #
        'National Review': 'right',
        'New York Post': 'right', #
        'New York Times': 'left', #
        'NPR': 'left', #
        'Reuters': 'center', #
        'Talking Points Memo': 'left', #
        'Vox': 'left', #
        'Washington Post': 'left', #
    }
    return leanings.get(publication, 'unknown')

publication_index = headers.index('publication')
headers.append('leaning')

for row in rows:
    publication = row[publication_index]
    row.append(assign_leaning(publication))

output_filename = "processed3.csv"

with open(output_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers)
    csvwriter.writerows(rows)