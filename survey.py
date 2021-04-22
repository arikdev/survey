import pandas as pd
import json
import sys

DEBUG = False
survey_file = '/home/manage/arik/survey/FCE_Quiz.xlsx'
res_part1_file = '/home/manage/arik/survey/CyberSecuritySurveyPart1.xlsx'
res_part2_file = '/home/manage/arik/survey/CyberSecuritySurveyPart2.xlsx'
tmp_csv_file = "tmp_file.csv"
SEP = '^'
questions = []
results = {}

def get_grade(category, grades):
    grade = 0.0
    max_grade = 0.0

    for i,q in enumerate(questions):
        if q['category'] != category:
            continue
        grade += grades[i] * questions[i]['weight']
        max_grade += 5 * questions[i]['weight']

    return grade / max_grade


def summerize_grades(mail, result):
    result['categories'] = {}
    old_category = None
    for i,q in enumerate(questions):
        if i >= len(result['grades']):
                print(mail + ' did not finish 2 parts! ')
                break
        if q['category'] not in result['categories']:
            if old_category is not None:
                result['categories'][old_category]['grade'] = get_grade(old_category, result['grades'])
            result['categories'][q['category']] = {}
            old_category = q['category']
    if old_category is not None:
        result['categories'][old_category]['grade'] = get_grade(old_category, result['grades'])


def cacl_grade(answers):
    grades = [0 for i in answers]
    category_graes = {}

    for i,answer in enumerate(answers):
        if answer == -1:
            return -1
        if answer == 5:
            continue
        correct = questions[i]['answer']
        if correct < 5:
            if answer > 5:
                continue
        else:
            if answer < 5:
                continue
        grades[i] = 5 - abs(correct - answer)

    return grades

def excel_to_csv(excel_file):
    tmp_csv_file = "tmp_file.csv"
    read_file = pd.read_excel(excel_file)
    read_file.to_csv (tmp_csv_file,
                    index = None,
                    sep = SEP, 
                    header=True)
    return tmp_csv_file

def handle_res_file(res_file, question_start, num_of_questions, is_part1):
    with open(excel_to_csv(res_file)) as fin:
        jump = True
        for line in fin:
            line = line[:-1]
            tokens = line.split(SEP)
            email = tokens[3]
            if '@' in email:
                jump = False
            if jump:
                continue
            if is_part1:
                group = tokens[6]
            else:
                group = 'None'
            if email not in results:
                answers = [-1 for i in range(num_of_questions)]
                results[email] = {'answers': answers, 'group':group}
            answers = results[email]['answers']
            q_pos = 0 if is_part1 else len(answers)
            if not is_part1:
                part2 = [-1 for i in range(num_of_questions)]
                answers += part2
            for i in range(question_start, question_start + num_of_questions):
                answers[q_pos] = int(tokens[i])
                q_pos += 1


def load_db():
    with open(excel_to_csv(survey_file)) as fin:
        count = 0
        for line in fin:
            if count < 3:
                count += 1
                continue
            line = line[:-1]
            tokens = line.split(SEP)
            if tokens[0] == 'Training':
                break
            if len(tokens[0]) > 0:
                category = tokens[0]
            if len(tokens[1]) > 0:
                sub_category = tokens[1]
            question = tokens[3]
            weight = float(tokens[4])
            answer = int(tokens[-1])
            questions.append({'category':category, 'sub_category':sub_category, 'question':question, 'weight':weight, 'answer':answer})

    handle_res_file(res_part1_file, 9, 25, True)
    handle_res_file(res_part2_file, 6, 33, False)
    
load_db()

if DEBUG:
    print('------------- Questions -----------------')
    for i,v in enumerate(questions):
        print('------------------------------------------------------------')
        print(i)
        print(v)
    
for k,v in results.items():
    grade = cacl_grade(v['answers'])
    if grade == -1:
        print(k + ' did not finish 2 parts! ')
        continue
    v['grades'] = grade
    summerize_grades(k, v)

with open('questions.json', 'w') as fout:
    json.dump(questions, fout)
with open('results.json', 'w') as fout:
    json.dump(results, fout)
