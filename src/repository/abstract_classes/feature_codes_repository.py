from abc import ABC, abstractmethod

class FeatureCodesRepository(ABC):
    @abstractmethod
    def get_codes(self):
        pass
    
    @abstractmethod
    def insert_code(self, code):
        pass