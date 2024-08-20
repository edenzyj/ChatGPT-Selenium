from selenium.webdriver.remote.webdriver import By
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.keys import Keys

class gptParser:
    def __init__(self,
                 driver,
                 gpt_url: str = 'https://chat.openai.com/'):
       
        # Start a webdriver instance and open ChatGPT
        self.driver = driver
        self.driver.get(gpt_url)

    @staticmethod
    def get_driver():
        uc.TARGET_VERSION = 124
        driver = uc.Chrome()
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver = webdriver.Chrome(executable_path="C:/Users/AnnA/Desktop/chromedriver_win32/chromedriver.exe")
        return driver

    def __call__(self, msg: str):
        # Find the input field and send a question
        input_field = self.driver.find_elements(
            By.TAG_NAME, 'textarea')[0]
        input_field.send_keys(msg)
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
        
def ask_gpt_for_final_answer(question, answer_one, answer_two):
    driver = gptParser.get_driver()
    gpt_parser = gptParser(driver)

    '''query = "test"
    gpt_parser(query) 
    time.sleep(5)
    response = gpt_parser.read_respond() 
    for r in response:
        print(r)'''
        
    # new chat
    gpt_parser.new_chat()

    query = "There is a farmer asking about a question.  The question is : " + question + "  " + "This is the first answer : " + answer_one + "  And this is the second answer : " + answer_two + "  If you are a botanist, tell me which one is more precise."
    print(query)
    print("==========")

    gpt_parser(query)
    time.sleep(5)
    response = gpt_parser.read_respond()
    for r in response:
        print(r)
    
    time.sleep(20)

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
    gpt_parser.new_chat()

    query = "There is a farmer asking about a question.  The question is : " + question + "  " + "This is the first result from retriever : " + answer_one + "  And this is the second result from retriever : " + answer_two + "  Which retrieval result is more related with the question."
    print(query)
    print("==========")

    gpt_parser(query)
    time.sleep(5)
    response = gpt_parser.read_respond()
    for r in response:
        print(r)
    
    time.sleep(10)

if __name__ == "__main__":
    question = "What is Anthracnose caused by?"
    
    answer_one = "A classic reference! According to Ocfemia, GO, Agati JA (1925), anthracnose is caused by the fungus Colletotrichum lagenarium."

    answer_two = "Anthracnose is a fungal disease caused by various species of the genus Colletotrichum. The pathogen that causes anthracnose depends on the host plant and region. In some hosts or regions, a dominant Colletotrichum species may be responsible for the disease. In hosts such as coffee, citrus, and strawberries, the disease is often caused by Colletotrichum spp. such as C. kahawae, C. acutatum, and C. fragariae, respectively. In regions where the boniense clade is present, the disease is typically caused by Colletotrichum boniense. This clade is characterized by a specific set of morphological and molecular features. The boniense clade is widespread and has been reported to cause anthracnose in various hosts, including coffee, citrus, and other crops. It is considered a major threat to agriculture, as it can cause significant yield loss and reduce crop quality. In regions where the boniense clade is present, it is often the dominant cause of anthracnose, and its presence can have significant implications for disease management and crop protection strategies. It's worth noting that the boniense clade is not the only clade that can cause anthracnose, and other clades, such as the lindemuthianum and dematium clades, can also be responsible for the disease in different hosts and regions."
    
    ask_gpt_for_final_answer(question, answer_one, answer_two)
    
    result_one = "Ocfemia, GO, Agati JA (1925). The cause of anthracnose of avocado, mango and upo in the Philippine Islands. Philippine Agriculturalist 14: 199–216."
    
    result_two = "A classic reference! According to Ocfemia, GO, Agati JA (1925), anthracnose is caused by the fungus Colletotrichum lagenarium."

    # ask_gpt_for_retrieve_result(question, result_one, result_two)
