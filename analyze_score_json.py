from cmath import sqrt
from scipy.stats import norm
import numpy as np
import json

question_type_file = "output_file/question_type_1000.json"

question_type = []

with open(question_type_file, "r") as fq:
    question_type = json.load(fq)

comparison_folder = "output_file/RAG_Flow/"

comparison_file = "RAGFlow_pure-llama32-3b_comparison.json"

first_scores = []
second_scores = []

first_win = 0
second_win = 0

try:
    with open(comparison_folder + comparison_file, "r") as fr:
        data = json.load(fr)

        for item in data:
            qid = item['qid']

            if question_type[qid]['query_type'] == "Practice-related": continue

            split_list = item['comparison'].split("/100")

            if len(split_list) < 3:
                print(f"The comparison doesn't include both scores, qid = {qid}")
                continue

            first_score = int(split_list[0].split(" ")[-1])
            second_score = int(split_list[-2].split(" ")[-1])

            first_scores.append(first_score)
            second_scores.append(second_score)

            if first_score > second_score:
                first_win = first_win + 1
            else:
                second_win = second_win + 1

        fr.close()
except Exception as e:
    print(f"An error occurred: {e}")

first_avr = sum(first_scores) / len(first_scores)
second_avr = sum(second_scores) / len(second_scores)

first_vd = sqrt(sum([(score - first_avr)**2 for score in first_scores]) / len(first_scores))
second_vd = sqrt(sum([(score - second_avr)**2 for score in second_scores]) / len(second_scores))

total = first_win + second_win
winning_rate = first_win / total
z = norm.ppf(0.975)  # 1.96 for 95% CI
std_error = np.sqrt(winning_rate * (1 - winning_rate) / total)
lower = winning_rate - z * std_error
upper = winning_rate + z * std_error

print("First Win : {}".format(first_win))
print("First Average : {}".format(first_avr))
print("First VD : {}".format(first_vd))
print("Second Win : {}".format(second_win))
print("Second Average : {}".format(second_avr))
print("Second VD : {}".format(second_vd))
print("Winning rate = {}".format(winning_rate))
print("95 confidence : [{}, {}]".format(lower, upper))
