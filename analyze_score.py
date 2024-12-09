comparison_folder = "output_file/finetune/"

comparison_file = "finetuned360k_9907_comparison_revised.txt"

first_scores = []
second_scores = []

first_win = 0
second_win = 0

with open(comparison_folder + comparison_file, "r") as fr:
    text = fr.read()
    
    comparisons_list = text.split("Comparison ")
    
    for i in range(1, len(comparisons_list)):
        comparison_str = comparisons_list[i]
        
        if "/100" not in comparison_str:
            print("Comparison {} lack scores!".format(i))
            continue
        
        score_list = comparison_str.split("/100")
        
        first_score = float(score_list[int(len(score_list)//2)-1].split(" ")[-1])
        second_score = float(score_list[-2].split(" ")[-1])
        
        first_scores.append(first_score)
        second_scores.append(second_score)
        
        if first_score > second_score:
            first_win = first_win + 1
        else:
            second_win = second_win + 1
        
    fr.close()

first_avr = sum(first_scores) / len(first_scores)
second_avr = sum(second_scores) / len(second_scores)

first_mse = sum([(score - first_avr)**2 for score in first_scores]) / len(first_scores)
second_mse = sum([(score - second_avr)**2 for score in second_scores]) / len(second_scores)

print("First Win : {}".format(first_win))
print("First Average : {}".format(first_avr))
print("First MSE : {}".format(first_mse))
print("Second Win : {}".format(second_win))
print("Second Average : {}".format(second_avr))
print("Second MSE : {}".format(second_mse))
