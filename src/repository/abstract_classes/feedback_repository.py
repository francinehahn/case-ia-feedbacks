from abc import ABC, abstractmethod

class FeedbackRepository(ABC):
    @abstractmethod
    def insert_feedback(self, feedback):
        pass
    
    @abstractmethod
    def get_feedback_by_id(self, feedback_id:str):
        pass
    
    @abstractmethod
    def get_feedbacks_sentiment_percentage(self, time_period:str):
        pass