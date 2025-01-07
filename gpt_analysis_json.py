import os
import time
import json
import random
from call_gpt import gptParser, gpt_url

def ask_gpt_for_final_answer(query, answer_one, answer_two, qid, data):    
    driver = gptParser.get_driver()
    gpt_parser = gptParser(driver)
    
    answer_one = answer_one.replace('\n', ' ')
    answer_two = answer_two.replace('\n', ' ')

    prompt = "There is a farmer asking a question: " + query + "  This is the first answer: " + answer_one + "  And this is the second answer: " + answer_two + "  Which of the following answers is better, the first answer or the second answer?  Give both answers a score in 100.  Generate response in this form:  First score=   Second score=   Reason:"
    
    time.sleep(5)
    while driver.current_url != gpt_url:
        driver.close()
        time.sleep(5)
        driver = gptParser.get_driver()
        gpt_parser = gptParser(driver)
        time.sleep(5)

    time.sleep(5)
    gpt_parser(prompt)
    
    time.sleep(30)
    response = gpt_parser.read_respond()
    comparison = ""
    
    for r in response:
        comparison = comparison + "\n" + r
    
    time.sleep(10)
    driver.close()
    time.sleep(5)
    
    data.append({
        "qid": qid,
        # "First_Score": int(comparison.split("First score= ")[1].split("\n")[0]),
        "First_Score": comparison.split("First score")[1].split("\n")[0],
        # "Second_Score": int(comparison.split("Second score= ")[1].split("\n")[0]),
        "Second_Score": comparison.split("Second score")[1].split("\n")[0],
        "Reason": comparison.split("Reason:")[1],
        "answer_1": answer_one,
        "answer_2": answer_two
    })
    
    return data

input_dir = "input_file/json/"
output_dir = "output_file/9907/"

if __name__ == "__main__":
    file_1 = input_dir + "9907_tart_nFT_Llama3.2_1000Q_k10_pure_Ans.json"
    file_2 = input_dir + "9907_RR100_nFT_Llama32_1000Q_k10.json"
    
    with open(file_1, 'r') as fr:
        no_ref_data = json.load(fr)
        fr.close()
        
    with open(file_2, 'r') as fr:
        ref_data = json.load(fr)
        fr.close()
    
    output_data = []
    
    # Random 100 qids from 1000 queries.
    random_numbers = [random.randint(0, 999) for _ in range(100)]
    
    for qid in random_numbers:
        item = no_ref_data[qid]
        query = item['query']
        answer_1 = item['answer']
        answer_2 = ref_data[qid]['answer']
        output_data = ask_gpt_for_final_answer(query, answer_1, answer_2, qid, output_data)
    
    file_out = output_dir + "without_reference_vs_include_reference.json"
    
    with open(file_out, 'w') as fw:
        json.dump(output_data, fw, indent=4)
        fw.close()
