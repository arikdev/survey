import pandas as pd
import sys

survey_file = '/home/manage/arik/survey/FCE_Quiz.xlsx'
res_part1_file = '/home/manage/arik/survey/CyberSecuritySurveyPart1.xlsx'
tmp_csv_file = "tmp_file.csv"

questions = []
results = {}

def excel_to_csv(excel_file):
    tmp_csv_file = "tmp_file.csv"
    read_file = pd.read_excel(excel_file)
    read_file.to_csv (tmp_csv_file,
                    index = None,
                    header=True)
    return tmp_csv_file

def handle_res_file(res_file, question_start, num_of_questions):
    with open(excel_to_csv(res_file)) as fin:
        first = False
        for line in fin:
            if first:
                first= False
                continue
            line = line[:-1]
            tokens = line.split(',')
            email = tokens[3]
            if email not in results:
                answers = [-1 for i in range(num_of_questions)]
                results[email] = {'answers': answers}

def load_db():
    with open(excel_to_csv(survey_file)) as fin:
        count = 0
        for line in fin:
            if count < 3:
                count += 1
                continue
            line = line[:-1]
            tokens = line.split(',')
            if tokens[0] == 'Training':
                break
            if len(tokens[0]) > 0:
                category = tokens[0]
            if len(tokens[1]) > 0:
                sub_category = tokens[1]
            question = tokens[3]
            weight = tokens[4]
            answer = tokens[-1]
            questions.append({'category':category, 'sub_category':sub_category, 'question':question, 'weight':weight, 'answer':answer})

    handle_res_file(res_part1_file, 9, 25)
    
load_db()


print('------------- Questions -----------------')
for i,v in enumerate(questions):
    print('------------------------------------------------------------')
    print(i)
    print(v)
print('------------- Results -----------------')
for k,v in results.items():
    print(k, v)
