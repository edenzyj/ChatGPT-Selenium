import json

input_dir = "input_file/3163/"
output_dir = "output_file/3163/"

if __name__ == "__main__":
    file_1 = input_dir + "graphRAG_Qwen_Gen_1000Q_150W_llama3.2.json"
    file_2 = input_dir + "pure_Gen_1000Q_150W_llama3.2.json"
    
    with open(file_1, 'r') as fr1:
        answer_1_list = json.load(fr1)
        fr1.close()
    
    with open(file_2, 'r') as fr2:
        answer_2_list = json.load(fr2)
        fr2.close()
    
    length_1 = 0
    length_2 = 0
    
    for i in range(0, len(answer_1_list)):
        item = answer_1_list[i]
        query = item['query']
        answer_1 = item['answer'].replace("<|start_header_id|>assistant<|end_header_id|>\n\n", "")
        answer_2 = answer_2_list[i]['answer'].replace("<|start_header_id|>assistant<|end_header_id|>\n\n", "")
        # print(f"qid: {i}, length of answer 1: {len(answer_1)}, length of answer 2: {len(answer_2)}")
        
        length_1 += len(answer_1)
        length_2 += len(answer_2)
    
    print(f"Avr. length of answer 1 list: {length_1 / 1000}")
    print(f"Avr. length of answer 2 list: {length_2 / 1000}")
    