from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate

class LLM(ABC):
    @abstractmethod
    def perform_request(self, prompt:ChatPromptTemplate, prompt_replacements:dict):
        pass