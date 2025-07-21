import time
import json
import random
from selenium import webdriver
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException


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
    def __init__(self, driver, gpt_url: str = gpt_url):
        self.driver = driver
        self.driver.get(gpt_url)
        self.history = []
        self.wait = WebDriverWait(self.driver, 30)

    @staticmethod
    def get_driver():
        uc.TARGET_VERSION = 138
        # options = uc.ChromeOptions()
        # options.add_argument("--incognito")

        driver = uc.Chrome()
        # driver = webdriver.Chrome()

        return driver
    
    def wait_for_response_complete(self):
        """Wait for ChatGPT to finish generating response"""
        print("Waiting for ChatGPT response to complete...")
        
        # Wait for the stop button to appear (indicating generation started)
        try:
            stop_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='stop-button']"))
            )
            print("Response generation started...")
        except TimeoutException:
            print("Stop button not found, response might be instant or already complete")
        
        time.sleep(30)
        
        # Wait for the speech button to appear (indicating generation finished)
        try:
            speech_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='composer-speech-button']"))
            )
            print("Response generation completed!")
        except TimeoutException:
            print("Stop button didn't disappear, assuming response is complete")
        
        # Additional wait to ensure DOM is fully updated
        time.sleep(5)

    def send_message(self, msg: str):
        """Send a message and wait for response completion"""
        try:
            # Find and clear the input field
            input_field = self.wait.until(EC.element_to_be_clickable((By.ID, 'prompt-textarea')))
            print("Find the text area!")
            input_field.clear()
            print("Make sure the text area is clear!")
            input_field.send_keys(msg)
            print("Input contents done!")
            
            time.sleep(5)
            
            # Send the message
            #send_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='send-button']")
            #send_button.click()
            input_field.send_keys(Keys.RETURN)
            print("Send the message done!")
            
            # Wait for response to complete
            self.wait_for_response_complete()
            
        except TimeoutException:
            print("Failed to send message - input field not found")
            raise

    def get_latest_response(self):
        """Get the latest response from ChatGPT"""
        try:
            # Get all message elements
            messages = self.driver.find_elements(By.CSS_SELECTOR, "[data-message-author-role]")
            
            if not messages:
                return "No messages found"
            
            # Get the last assistant message
            for message in reversed(messages):
                role = message.get_attribute("data-message-author-role")
                if role == "assistant":
                    # Get all text content from the message
                    text_elements = message.find_elements(By.CSS_SELECTOR, "p, li")
                    response_text = "\n".join([elem.text for elem in text_elements if elem.text.strip()])
                    return response_text
            
            return "No assistant response found"
            
        except Exception as e:
            print(f"Error getting response: {e}")
            return "Error retrieving response"

    def new_chat(self):
        self.driver.find_elements("class name", 'text-token-text-primary')[3].click()

    def close(self):
        self.driver.quit()
        
def ask_gpt_for_final_answer(gpt_parser, question, answer_one, answer_two):
    """Ask GPT for comparison using the existing parser instance"""
    
    query = f"Here is a farmer question: {question}  " \
            f"Answer 1: {answer_one}  " \
            f"Answer 2: {answer_two}  " \
            f"Which answer is more professional and focused? Please give each answer a separate score out of 100.  " \
            f"Reply me with the scores first, and then answer the reason less than 100 words."
    
    print(f"Sending comparison query...")
    
    try:
        gpt_parser.send_message(query)
        response = gpt_parser.get_latest_response()
        return response
    except Exception as e:
        print(f"Error in ask_gpt_for_final_answer: {e}")
        return f"Error: {e}"
    
    
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

input_dir = "input_file/3163/"
output_dir = "output_file/3163/"

if __name__ == "__main__":
    file_1 = input_dir + "graphRAG_Gen_1000Q_llama3.2.json"
    file_2 = input_dir + "pure_Gen_1000Q_llama3.2.json"
    
    with open(file_1, 'r') as fr1:
        answer_1_list = json.load(fr1)
        fr1.close()
    
    with open(file_2, 'r') as fr2:
        answer_2_list = json.load(fr2)
        fr2.close()
    
    file_out = output_dir + "graphRAG_pureLLM_comparison.json"
    
    random_numbers = [random.randint(0, 999) for _ in range(100)]
    
    output_list = []

    try:
        # Process all questions with the same driver instance
        for i, qid in enumerate(random_numbers):
            print(f"\nProcessing question {i+1}/{len(random_numbers)} (ID: {qid})")
            
            item = answer_1_list[qid]
            query = item['query']
            answer_1 = item['answer'].replace("<|start_header_id|>assistant<|end_header_id|>\n\n", "")
            answer_2 = answer_2_list[qid]['answer'].replace("<|start_header_id|>assistant<|end_header_id|>\n\n", "")
            
            # Initialize driver and parser once
            print("Starting browser...")
            driver = gptParser.get_driver()
            print("Navigating to ChatGPT...")
            gpt_parser = gptParser(driver)
            
            answer_1_no_newline = answer_1.replace("\n", " ")
            answer_2_no_newline = answer_2.replace("\n", " ")
            
            compare_result = ask_gpt_for_final_answer(gpt_parser, query, answer_1_no_newline, answer_2_no_newline)
            
            output_list.append({
                "qid": qid,
                "query": query,
                "answer 1": answer_1,
                "answer 2": answer_2,
                "comparison": compare_result
            })
            
            print(f"Completed question {i+1}")
            
            with open(file_out, 'w') as fw:
                json.dump(output_list, fw, indent=4)
                fw.close()
            
            gpt_parser.close()

            time.sleep(30)
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        print("Closing browser...")
        gpt_parser.close()
        print("Done!")
    
    # result_one = "Yang SY, Su SC, Liu T, Fan G, Wang J (2011). First report of anthracnose caused by Colletotrichum gloeosporioides on pistachio (Pistacia vera) in China. Plant Disease 95: 1314."
    
    # result_two = "(2002). 30. Novotny, D., Krizkova, I. & Salava, J. First report of anthracnose caused by Colletotrichum acutatum on strawberry in the Czech"

    # ask_gpt_for_retrieve_result(question, result_one, result_two)
