from cmath import sqrt
import json

comparison_folder = "output_file/9907/"

comparison_file = "without_reference_vs_include_reference.json"

first_scores = []
second_scores = []

first_win = 0
second_win = 0

with open(comparison_folder + comparison_file, "r") as fr:
    data = json.load(fr)
    
    for item in data:
        first_score = int(item['First_Score'][-2:])
        second_score = int(item['Second_Score'][-2:])
        
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
