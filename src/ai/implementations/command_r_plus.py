import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from abstract_classes.LLM import LLM
from langchain_cohere import ChatCohere
from dotenv import load_dotenv

load_dotenv()

class CommandRplus(LLM):
    def __connect(self, temperature: float = 0.7):
        llm = ChatCohere(
            model='command-r-plus',
            cohere_api_key=os.getenv('COHERE_API_KEY'),
            temperature=temperature
        )
        return llm
        
    def perform_request(self, prompt:list, temperature: float = 0.7):
        try:
            llm = self.__connect(temperature=temperature)
            successful = False
            attempts = 0
            
            while not successful and attempts < 3:
                try:
                    attempts += 1
                    result = llm.invoke(input=prompt)
                    result_text = result.content
                    successful = True
                except:
                    pass
                
            if not successful:
                raise Exception('LLM connection error: Max call attempts!')
            
            return result_text
        except Exception as e:
            print(e)
            raise Exception(str(e)) from e