from cmath import sqrt
import json

comparison_folder = "output_file/3163/"

comparison_file = "graphRAG_pureLLM_comparison_150W.json"

first_scores = []
second_scores = []

first_win = 0
second_win = 0

with open(comparison_folder + comparison_file, "r") as fr:
    data = json.load(fr)
    
    for item in data:
        qid = item['qid']
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
    
first_avr = sum(first_scores) / len(first_scores)
second_avr = sum(second_scores) / len(second_scores)

first_vd = sqrt(sum([(score - first_avr)**2 for score in first_scores]) / len(first_scores))
second_vd = sqrt(sum([(score - second_avr)**2 for score in second_scores]) / len(second_scores))

print("First Win : {}".format(first_win))
print("First Average : {}".format(first_avr))
print("First VD : {}".format(first_vd))
print("Second Win : {}".format(second_win))
print("Second Average : {}".format(second_avr))
print("Second VD : {}".format(second_vd))
