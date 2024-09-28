from selenium.webdriver.remote.webdriver import By
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.keys import Keys

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
        driver = uc.Chrome()
        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver = webdriver.Chrome(executable_path="C:/Users/AnnA/Desktop/chromedriver_win32/chromedriver.exe")
        return driver

    def __call__(self, msg: str):
        # Find the input field and send a question
        input_field = self.driver.find_elements(By.ID, 'prompt-textarea')[0]
        input_field.send_keys(msg)
        time.sleep(1)
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
    # gpt_parser.new_chat()

    query = "There is a farmer asking about a question.  The question is : " + question + "  " + "This is the first answer : " + answer_one + "  And this is the second answer : " + answer_two + "  If you are a botanist, tell me which one is more precise."
    print(query)
    print("==========")

    time.sleep(3)
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
    # gpt_parser.new_chat()

    query = "There is a farmer asking about a question.  The question is : " + question + "  " + "This is the first result from retriever : " + answer_one + "  And this is the second result from retriever : " + answer_two + "  Which retrieval result is more related with the question."
    print(query)
    print("==========")

    time.sleep(3)
    gpt_parser(query)
    
    time.sleep(5)
    response = gpt_parser.read_respond()
    for r in response:
        print(r)
    
    time.sleep(10)

if __name__ == "__main__":
    question = "How to prevent and treat Anthracnose?"
    
    answer_one = "To prevent and treat Anthracnose, employ these measures: Cultural Control: Rotate crops, remove infected plant debris, and ensure good air circulation. Resistant Varieties: Use plant varieties resistant to Anthracnose. Proper Watering: Avoid overhead irrigation to reduce leaf wetness. Fungicide Application: Apply appropriate fungicides as needed based on local recommendations. These practices help minimize disease spread and manage outbreaks effectively."

    answer_two = "Anthracnose, caused by Colletotrichum spp., can be prevented by using disease-free planting material, practicing crop rotation, and avoiding overhead irrigation. Applying fungicides like copper-based ones and maintaining good field hygiene, such as removing infected plant debris, also helps. For treatment, affected plants should be pruned to remove diseased parts, and appropriate fungicides should be applied according to local guidelines."
    
    ask_gpt_for_final_answer(question, answer_one, answer_two)
    
    result_one = "Yang SY, Su SC, Liu T, Fan G, Wang J (2011). First report of anthracnose caused by Colletotrichum gloeosporioides on pistachio (Pistacia vera) in China. Plant Disease 95: 1314."
    
    result_two = "(2002). 30. Novotny, D., Krizkova, I. & Salava, J. First report of anthracnose caused by Colletotrichum acutatum on strawberry in the Czech"

    # ask_gpt_for_retrieve_result(question, result_one, result_two)
