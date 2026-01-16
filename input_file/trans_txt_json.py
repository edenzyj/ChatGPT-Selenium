import json

if __name__ == "__main__":
    input_file = "queries_1000.txt"
    output_file = "queries_1000.json"
    
    with open(input_file, "r") as fr:
        lines = fr.readlines()
    
    json_list = []
    
    for id, line in enumerate(lines):
        line = line.strip()
        if line:  # Ensure the line is not empty
            json_list.append({
                "qid": id,
                "query": line
            })
    
    with open(output_file, "w") as fw:
        json.dump(json_list, fw, indent=4)
