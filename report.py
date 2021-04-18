import pandas as pd
import json
import sys

results_file = 'results.json'
questions_file = 'questions.json'
tmp_csv_file = 'tmp_file.csv'
output_file= 'grades.xlsx'
SEP = '^'

#  DB:
# question_stats [{'num_of_anwers':'', 'sum_of_grades':'..', 'avrg_score';')

questions_stats = []
with open(questions_file, 'r') as fin:
    data = json.load(fin)
for i,v in enumerate(data):
    questions_stats.append({'question':v['question'], 'sum_of_grades':0, 'num_of_grades':0})

with open(results_file, 'r') as fin:
    results = json.load(fin)

for i,q in enumerate(questions_stats):
    for k,v in results.items():
        if len(v['grades']) <= i:
            continue
        q['num_of_grades'] += 1
        q['sum_of_grades'] += 20 * v['grades'][i]

questions_stats = sorted(questions_stats, reverse=True, key=lambda v : round(v['sum_of_grades'] / v['num_of_grades']))
with open(tmp_csv_file, 'w') as fout:
    for v in questions_stats:
        print(v['question'] + SEP ,end='', file=fout)
        print(round((v['sum_of_grades'] / v['num_of_grades']) / 100, 4), file=fout)

df_new = pd.read_csv(tmp_csv_file, sep=SEP)
GFG = pd.ExcelWriter(output_file)
df_new.to_excel(GFG, index = False)
GFG.save()
