import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from abstract_classes.LLM import LLM
from langchain_cohere import ChatCohere
import json

class CommandRplus(LLM):
    def __init__(self):
        self.llm = ChatCohere(model='command-r-plus', cohere_api_key='XaIA761M7jcmrTdkJUU5yqX0czJKM0NiSOOp20Qj')
    
    def perform_request(self, prompt:list):
        try:
            successful = False
            attempts = 0
            
            while not successful and attempts < 3:
                try:
                    attempts += 1
                    result = self.llm.invoke(prompt)
                    print(result)
                    result_text = json.loads(result.content)
                    successful = True
                except:
                    pass
                
            if not successful:
                raise Exception('LLM connection error: Max call attempts!')
            
            return result_text
        except Exception as e:
            print(e)
            raise Exception(str(e)) from e