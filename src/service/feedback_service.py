import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repository.abstract_classes.feedback_repository import FeedbackRepository
from repository.abstract_classes.requested_features_repository import RequestedFeaturesRepository
from schema.feedback_input_schema import FeedbackInputSchema

class FeedbackService():
    def __init__(self, feedback_repository:FeedbackRepository, requested_features_repository:RequestedFeaturesRepository):
        self.feedback_repository = feedback_repository
        self.requested_features_repository = requested_features_repository
    
    def feedbacks(self, data):
        # data validation
        FeedbackInputSchema().validate_data(data)
        
        print(data)