import csv
with open('frequency_data_cleaned.csv', 'r') as file:
    #reader = csv.DictReader(file)
    reader = csv.reader(file)
    words = []
    for r in reader:
        words += [(r[0].strip(), int(r[1]))]
    print(words)
    total_count = sum([w[1] for w in words])
    print(total_count)
    words = [(w[0], round(100 * w[1]/total_count, 4)) for w in words]
    print(words)

