from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def perform_request(self, prompt:list):
        pass