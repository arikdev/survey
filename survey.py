import pandas as pd
import sys

survey_file = '/home/manage/arik/survey/FCE_Quiz.xlsx'
res_part1_file = '/home/manage/arik/survey/CyberSecuritySurveyPart1.xlsx'
res_part2_file = '/home/manage/arik/survey/CyberSecuritySurveyPart2.xlsx'
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

def handle_res_file(res_file, question_start, num_of_questions, is_part1):
    with open(excel_to_csv(res_file)) as fin:
        jump = True
        for line in fin:
            line = line[:-1]
            tokens = line.split(',')
            email = tokens[3]
            if '@' in email:
                jump = False
            if jump:
                continue
            if email not in results:
                answers = [-1 for i in range(num_of_questions)]
                results[email] = {'answers': answers}
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

    handle_res_file(res_part1_file, 9, 25, True)
    handle_res_file(res_part2_file, 6, 33, False)
    
load_db()


print('------------- Questions -----------------')
for i,v in enumerate(questions):
    print('------------------------------------------------------------')
    print(i)
    print(v)
print('------------- Results -----------------')
for k,v in results.items():
    print(k, v)
    sum = 0
    for i in v['answers']:
        sum += i
    print(k, sum)
