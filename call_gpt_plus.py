from selenium import webdriver
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time
import json
import random

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
        self.history = []
        self.wait = WebDriverWait(self.driver, 30)

    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir=C:/Users/edenzytj/AppData/Local/Google/Chrome/User Data")
        options.add_argument("profile-directory=Profile 11")
        driver = webdriver.Chrome(options=options)

        return driver

    def wait_for_login(self):
        """Wait for user to complete Google login manually"""
        print("Please log in to ChatGPT using your Google account.")
        print("Once logged in and you see the ChatGPT interface, press Enter to continue...")
        input()  # Wait for user to press Enter
        
        # Verify we're logged in by checking for the chat interface
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, 'prompt-textarea')))
            print("Login successful! ChatGPT interface detected.")
            return True
        except TimeoutException:
            print("Login verification failed. Please try again.")
            return False

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
        
        # Wait for the stop button to disappear (indicating generation finished)
        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "[data-testid='stop-button']"))
            )
            print("Response generation completed!")
        except TimeoutException:
            print("Stop button didn't disappear, assuming response is complete")
        
        # Additional wait to ensure DOM is fully updated
        time.sleep(2)

    def send_message(self, msg: str):
        """Send a message and wait for response completion"""
        try:
            # Find and clear the input field
            input_field = self.wait.until(EC.element_to_be_clickable((By.ID, 'prompt-textarea')))
            input_field.clear()
            input_field.send_keys(msg)
            
            # Send the message
            input_field.send_keys(Keys.RETURN)
            print(f"Message sent: {msg[:50]}...")
            
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

    def start_new_chat(self):
        """Start a new chat conversation"""
        try:
            # Look for new chat button
            new_chat_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='new-chat-button']")
            new_chat_button.click()
            time.sleep(2)
            print("Started new chat")
        except NoSuchElementException:
            print("New chat button not found, continuing with current chat")

    def close(self):
        """Close the browser"""
        self.driver.quit()

def ask_gpt_for_final_answer(gpt_parser, question, answer_one, answer_two):
    """Ask GPT for comparison using the existing parser instance"""
    
    query = f"There is a farmer asking a question which is: {question} " \
            f"This is the first answer: {answer_one} " \
            f"And this is the second answer: {answer_two} " \
            f"Which of the following answers is better, the first answer or the second answer? " \
            f"Give both answers a score out of 100 separately."
    
    print(f"Sending comparison query...")
    
    try:
        gpt_parser.send_message(query)
        response = gpt_parser.get_latest_response()
        return response
    except Exception as e:
        print(f"Error in ask_gpt_for_final_answer: {e}")
        return f"Error: {e}"

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
    
    # Initialize driver and parser once
    print("Starting browser and navigating to ChatGPT...")
    driver = gptParser.get_driver()
    gpt_parser = gptParser(driver)
    
    # Wait for manual login
    if not gpt_parser.wait_for_login():
        print("Login failed. Exiting...")
        driver.quit()
        exit(1)
    
    try:
        # Process all questions with the same driver instance
        for i, qid in enumerate(random_numbers):
            print(f"\nProcessing question {i+1}/{len(random_numbers)} (ID: {qid})")
            
            item = answer_1_list[qid]
            query = item['query']
            answer_1 = item['answer']
            answer_2 = answer_2_list[qid]['answer']
            
            # Start new chat for each comparison to avoid context confusion
            if i > 0:  # Don't start new chat for the first question
                gpt_parser.start_new_chat()
            
            compare_result = ask_gpt_for_final_answer(gpt_parser, query, answer_1, answer_2)
            
            output_list.append({
                "query": query,
                "answer 1": answer_1,
                "answer 2": answer_2,
                "comparison": compare_result
            })
            
            print(f"Completed question {i+1}")
            
            # Save progress after each question
        with open(file_out, 'w') as fw:
            json.dump(output_list, fw, indent=4)
    
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        print("Closing browser...")
        gpt_parser.close()
        print("Done!")
