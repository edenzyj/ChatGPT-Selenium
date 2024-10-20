from selenium.webdriver.remote.webdriver import By
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys

import os
import time

class gptParser:
    def __init__(self,
                 driver,
                 gpt_url: str = 'https://chatgpt.com/'):
       
        # Start a webdriver instance and open ChatGPT
        self.driver = driver
        self.driver.get(gpt_url)

    @staticmethod
    def get_driver():
        uc.TARGET_VERSION = 124
        # options = uc.ChromeOptions()
        # options.add_argument("--incognito")
        driver = uc.Chrome()
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver = webdriver.Chrome(executable_path="C:/Users/AnnA/Desktop/chromedriver_win32/chromedriver.exe")
        return driver

    def __call__(self, msg: str):
        # Find the input field and send a question
        input_field = self.driver.find_elements(By.ID, 'prompt-textarea')[0]
        input_field.send_keys(msg)
        time.sleep(5)
        input_field.send_keys(Keys.RETURN)
        
        # previous information
        # 'p'：text, 'code':code
        try:
            all_elements = self.driver.find_elements(By.CSS_SELECTOR, "code, p")
            # Arrange the text and code in order
            indexed_elements = list(enumerate(all_elements))
            sorted_elements = sorted(indexed_elements, key=lambda x: x[0])
            self.history = [ele.text for idx, ele in sorted_elements]
            self.history.remove('ChatGPT')
        except:
            self.history = []

    def read_respond(self):
        try:
            l = []
            all_elements = self.driver.find_elements(By.CSS_SELECTOR, "code, p")
            indexed_elements = list(enumerate(all_elements))
            sorted_elements = sorted(indexed_elements, key=lambda x: x[0])
            # only return the newest information
            for i in range(len(self.history), len(sorted_elements)-1):
                response = sorted_elements[i][1].text
                l.append(response)
            return l
        except:
            return None

    def new_chat(self):
        self.driver.find_elements("class name", 'text-token-text-primary')[3].click()

    def close(self):
        self.driver.quit()
        
def ask_gpt_for_final_answer(question, answer_one, answer_two, num, fw):
    print(question)
    print("----------")
    
    driver = gptParser.get_driver()
    gpt_parser = gptParser(driver)

    query = "There is a farmer asking a question which is : " + question + "  " + "This is the first answer : " + answer_one + "  And this is the second answer : " + answer_two + "  Which of the following answers is better, the first answer or the second answer?  Give both answers a score in 100 seperatively."
    # print(query)
    # print("==========")

    time.sleep(5)
    gpt_parser(query)
    
    time.sleep(30)
    response = gpt_parser.read_respond()
    comparison = ""
    
    for r in response:
        comparison = comparison + "\n" + r
        
    fw.write("Comparison {} :\n".format(num))
    fw.write(comparison)
    fw.write("\n\n")
    
    time.sleep(10)
    driver.close()
    time.sleep(5)
    
    print(comparison)
    print("==========")
    

def ask_gpt_for_retrieve_result(question, answer_one, answer_two):
    driver = gptParser.get_driver()
    gpt_parser = gptParser(driver)

    '''query = "test"
    gpt_parser(query) 
    time.sleep(5)
    response = gpt_parser.read_respond() 
    for r in response:
        print(r)'''
        
    # new chat
    # gpt_parser.new_chat()

    query = "There is a farmer asking a question which is : " + question + "  " + "This is the first result from retriever : " + answer_one + "  And this is the second result from retriever : " + answer_two + "  Which retrieval result is more related with the question."
    print(query)
    print("==========")

    time.sleep(3)
    gpt_parser(query)
    
    time.sleep(5)
    response = gpt_parser.read_respond()
    for r in response:
        print(r)
    
    time.sleep(10)

input_dir = "input_file/"
output_dir = "output_file/"

if __name__ == "__main__":
    question_file = input_dir + "questions_100.txt"
    
    question_list = []
    
    with open(question_file, 'r') as qfr:
        for quest in qfr.read().split('\n'):
            question_list.append(quest)
        qfr.close()
        # print(len(question_list))
    
    file_1 = input_dir + "taide_100Q_1st_Ans.txt"
    file_2 = input_dir + "tart_stella1.5B_100Q_1st_Ans.txt"
    
    answer_1_list = []
    answer_2_list = []
    
    with open(file_1, 'r') as fr1:
        for ans in fr1.read().split('Answwer'):
            answer_1_list.append(ans)
        fr1.close()
        # print(len(answer_1_list))
    
    with open(file_2, 'r') as fr2:
        for ans in fr2.read().split('Answer'):
            answer_2_list.append(ans)
        fr2.close()
    
    output_dir = output_dir + "1st_answers/"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    
    file_out = output_dir + "taide_stella_comparison.txt"
    
    with open(file_out, 'a') as fw:
        for i in range(49, len(question_list)):
            answer_one = answer_1_list[i+1]
            answer_one = answer_one.split('{} :\n'.format(i))[1]
            answer_one = answer_one.replace('\n', ' ')
            answer_one = answer_one[:-3] + "."
            
            answer_two = answer_2_list[i+1]
            answer_two = answer_two.split('{} :\n'.format(i))[1]
            answer_two = answer_two.replace('\n', ' ')
        
            ask_gpt_for_final_answer(question_list[i], answer_one, answer_two, i, fw)
    
    # result_one = "Yang SY, Su SC, Liu T, Fan G, Wang J (2011). First report of anthracnose caused by Colletotrichum gloeosporioides on pistachio (Pistacia vera) in China. Plant Disease 95: 1314."
    
    # result_two = "(2002). 30. Novotny, D., Krizkova, I. & Salava, J. First report of anthracnose caused by Colletotrichum acutatum on strawberry in the Czech"

    # ask_gpt_for_retrieve_result(question, result_one, result_two)
