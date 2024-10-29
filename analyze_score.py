import numpy as np

comparison_folder = "output_file/1st_answers/"

comparison_file = "llama3.2_llama3_comparison_revised.txt"

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
        
        first_scores.append(int(score_list[int(len(score_list)//2)-1].split(" ")[-1]))
        second_scores.append(int(score_list[-2].split(" ")[-1]))
        
    fr.close()

first_avr = sum(first_scores) / len(first_scores)
second_avr = sum(second_scores) / len(second_scores)

first_rms = np.sqrt(np.mean(score**2 for score in first_scores))
second_rms = np.sqrt(np.mean(score**2 for score in second_scores))

print("First Average : {}".format(first_avr))
print("First RMS : {}".format(first_rms))
print("Second Average : {}".format(second_avr))
print("Second RMs : {}".format(second_rms))
