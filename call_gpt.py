from selenium import webdriver
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys

import os
import time

class wait_for_text_to_stabilize:
    def __init__(self, locator, timeout=10):
        self.locator = locator
        self.timeout = timeout  # Time (in seconds) to wait for text to stabilize

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        current_text = element.text
        
        # Wait for the text to stop changing
        WebDriverWait(driver, self.timeout).until(
            lambda d: element.text == current_text and len(element.text) > 0
        )
        
        # After text stabilizes, return the element
        return element


gpt_url = 'https://chatgpt.com/'

class gptParser:
    def __init__(self,
                 driver,
                 gpt_url: str = gpt_url):
       
        # Start a webdriver instance and open ChatGPT
        self.driver = driver
        self.driver.get(gpt_url)

    @staticmethod
    def get_driver():
        uc.TARGET_VERSION = 131
        # options = uc.ChromeOptions()
        # options.add_argument("--incognito")

        driver = uc.Chrome()
        # driver = webdriver.Chrome()

        return driver

    def __call__(self, msg: str):
        # Find the input field and send a question
        input_field = self.driver.find_elements(By.ID, 'prompt-textarea')[0]
        input_field.send_keys(msg)
        time.sleep(5)

        input_field.send_keys(Keys.RETURN)
        # button = self.driver.find_element(By.ID, 'send-button')
        # button.click()
        
        # previous information
        # 'p'：text, 'li':listed text
        try:
            all_elements = self.driver.find_elements(By.CSS_SELECTOR, "p, li")
            # Arrange the text and code in order
            indexed_elements = list(enumerate(all_elements))
            sorted_elements = sorted(indexed_elements, key=lambda x: x[0])
            self.history = [ele.text for idx, ele in sorted_elements]
            self.history.remove('ChatGPT')
        except:
            self.history = []

    def read_respond(self):
        l = []
        while len(l) == 0:
            try:
                all_elements = self.driver.find_elements(By.CSS_SELECTOR, "p, li")
                indexed_elements = list(enumerate(all_elements))
                sorted_elements = sorted(indexed_elements, key=lambda x: x[0])
                for i in range(len(self.history), len(sorted_elements)-1):
                    response = sorted_elements[i][1].text
                    l.append(response)
                return l
            except:
                time.sleep(3)

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
    while driver.current_url != gpt_url:
        driver.close()
        time.sleep(5)
        driver = gptParser.get_driver()
        gpt_parser = gptParser(driver)
        time.sleep(5)

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
    
    # print(comparison)
    # print("==========")
    
    return
    
    
def ask_gpt_about_question(question, num, fw):
    driver = gptParser.get_driver()
    gpt_parser = gptParser(driver)

    query = "There is a farmer asking a question which is : " + question + "  " + "Is this question an agricultural issue? Give me a short answer only includes True or False."
    # print(query)
    # print("==========")

    time.sleep(5)
    gpt_parser(query)
    
    time.sleep(10)
    response = gpt_parser.read_respond()
    comfirm = ""
    
    for r in response:
        comfirm = comfirm + "\n" + r
        
    fw.write("Question comfirm {} :\n".format(num))
    fw.write(comfirm)
    fw.write("\n\n")
    
    time.sleep(10)
    driver.close()
    time.sleep(5)
    
    print(comfirm)
    print("==========")
    
    return
    

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
    
    file_1 = input_dir + "Llama3-8b_100Q_1st_Ans.txt"
    file_2 = input_dir + "tart_stella1.5B_100Q_1st_Ans.txt"
    
    answer_1_list = []
    answer_2_list = []
    
    with open(file_1, 'r', encoding='utf-8') as fr1:
        for ans in fr1.read().split('Answer'):
            answer_1_list.append(ans)
        fr1.close()
        # print(len(answer_1_list))
    
    with open(file_2, 'r') as fr2:
        for ans in fr2.read().split('Answer'):
            answer_2_list.append(ans)
        fr2.close()
    
    output_dir = output_dir + "naive/"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    
    file_out = output_dir + "llama3-8b_rag_comparison_revised.txt"
    
    with open(file_out, 'a') as fw:
        for i in range(len(question_list)):
            # TAIDE
            '''answer_one = answer_1_list[i+1]
            answer_one = answer_one.split('{} :\n'.format(i))[1]
            answer_one = answer_one.replace('\n', ' ')
            answer_one = answer_one[:-3] + "."
            
            if answer_one == "Sorry, this is not an agricultural issue. As a language model that strengthens agricultural knowledge and answer, Shennong Taide cannot deal with such problems.":
                print("*****TAIDE said the question is not an agricultural issue.*****")
                ask_gpt_about_question(question_list[i], i, fw)
                continue
                
            elif answer_one == "Sorry, the model cannot answer your questions according to the existing data set.":
                print("*****TAIDE said the question cannot be answered.*****")
                continue'''
                
            # Normal RAG outputs
            answer_one = answer_1_list[i+1]
            answer_one = answer_one.split('{} :\n'.format(i))[1]
            answer_one = answer_one.replace('\n', ' ')
            
            answer_two = answer_2_list[i+1]
            answer_two = answer_two.split('{} :\n'.format(i))[1]
            answer_two = answer_two.replace('\n', ' ')
            
            ask_gpt_for_final_answer(question_list[i], answer_one, answer_two, i, fw)
    
    # result_one = "Yang SY, Su SC, Liu T, Fan G, Wang J (2011). First report of anthracnose caused by Colletotrichum gloeosporioides on pistachio (Pistacia vera) in China. Plant Disease 95: 1314."
    
    # result_two = "(2002). 30. Novotny, D., Krizkova, I. & Salava, J. First report of anthracnose caused by Colletotrichum acutatum on strawberry in the Czech"

    # ask_gpt_for_retrieve_result(question, result_one, result_two)
