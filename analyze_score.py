comparison_folder = "output_file/1st_answers/"

comparison_file = "llama3.1_llama3_comparison_revised.txt"

first_scores = []
second_scores = []

with open(comparison_folder + comparison_file, "r") as fr:
    text = fr.read()
    
    comparisons_list = text.split("Comparison ")
    
    for i in range(1, len(comparisons_list)):
        comparison_str = comparisons_list[i]
        
        if "/100" not in comparison_str:
            continue
        
        score_list = comparison_str.split("/100")
        
        first_scores.append(float(score_list[int(len(score_list)//2)-1].split(" ")[-1]))
        second_scores.append(float(score_list[-2].split(" ")[-1]))
        
    fr.close()

first_avr = sum(first_scores) / len(first_scores)
second_avr = sum(second_scores) / len(second_scores)

first_mse = sum([(score - first_avr)**2 for score in first_scores]) / len(first_scores)
second_mse = sum([(score - second_avr)**2 for score in second_scores]) / len(second_scores)

print("First Average : {}".format(first_avr))
print("First MSE : {}".format(first_mse))
print("Second Average : {}".format(second_avr))
print("Second MSE : {}".format(second_mse))
