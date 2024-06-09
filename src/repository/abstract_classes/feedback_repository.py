from abc import ABC, abstractmethod

class FeedbackRepository(ABC):
    @abstractmethod
    def insert_feedback(self, feedback):
        pass