import csv

csv_file = "queries_100.csv"
text_file = "input_file/questions_100.txt"

with open(csv_file, 'r') as fr:
    csv_reader = csv.DictReader(fr)
    queries = [row['query'] for row in csv_reader]
    
with open(text_file, 'w') as fw:
    for query in queries:
        if query == "\n":
            continue
        fw.write('\n')
        fw.write(query)
