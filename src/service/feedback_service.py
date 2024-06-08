from src.repository.abstract_classes.feedback_repository import FeedbackRepository
from src.repository.abstract_classes.requested_features_repository import RequestedFeaturesRepository

class FeedbackService():
    def __init__(self, feedback_repository:FeedbackRepository, requested_features_repository:RequestedFeaturesRepository):
        self.feedback_repository = feedback_repository
        self.requested_features_repository = requested_features_repository
    
    def feedbacks(self):
        pass