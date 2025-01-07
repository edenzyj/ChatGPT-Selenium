import os
import time
import json
from call_gpt import gptParser, gpt_url

def ask_gpt_for_final_answer(query, answer_one, answer_two, qid, data):    
    driver = gptParser.get_driver()
    gpt_parser = gptParser(driver)
    
    answer_one = answer_one.replace('\n', ' ')
    answer_two = answer_two.replace('\n', ' ')

    prompt = "There is a farmer asking a question: " + query + "  This is the first answer: " + answer_one + "  And this is the second answer: " + answer_two + "  Which of the following answers is better, the first answer or the second answer?  Give both answers a score in 100.  Generate response in this form:  First Score =   Second Score =   Reason:"
    
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
        "First_Score": int(comparison.split("First Score = ")[1].split("\n")[0]),
        "Second_Score": int(comparison.split("Second Score = ")[1].split("\n")[0]),
        "Reason": comparison.split("Reason:")[1],
        "answer_1": answer_one,
        "answer_2": answer_two
    })
    
    return data

input_dir = "input_file/json/"
output_dir = "output_file/9907/"

if __name__ == "__main__":
    file_1 = input_dir + "9907_RR100_nFT_Llama32_1000Q_k10_noReference.json"
    file_2 = input_dir + "9907_RR100_nFT_Llama32_1000Q_k10.json"
    
    with open(file_1, 'r') as fr:
        no_ref_data = json.load(fr)
        fr.close()
        
    with open(file_2, 'r') as fr:
        ref_data = json.load(fr)
        fr.close()
    
    comparison_num = 0
    output_data = []
    
    for qid, item in enumerate(no_ref_data):
        if len(item['retrieved_context']) < 10:
            comparison_num += 1
            query = item['query']
            answer_1 = item['Answer']
            answer_2 = ref_data[qid]['answer']
            output_data = ask_gpt_for_final_answer(query, answer_1, answer_2, qid, output_data)
        if comparison_num == 100:
            break
    
    file_out = output_dir + "no_reference_vs_reference.json"
    
    with open(file_out, 'w') as fw:
        json.dump(output_data, fw, indent=4)
        fw.close()
