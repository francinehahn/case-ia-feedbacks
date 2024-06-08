import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repository.abstract_classes.feedback_repository import FeedbackRepository
from repository.abstract_classes.requested_features_repository import RequestedFeaturesRepository
from repository.abstract_classes.feature_codes_repository import FeatureCodesRepository
from ai.abstract_classes.LLM import LLM
from schema.feedback_input_schema import FeedbackInputSchema
from prompts.prompt_creator import PromptCreator

class FeedbackService():
    def __init__(
        self,
        feedback_repository:FeedbackRepository,
        requested_features_repository:RequestedFeaturesRepository,
        feature_codes_repository:FeatureCodesRepository,
        llm:LLM
    ):
        self.feedback_repository = feedback_repository
        self.requested_features_repository = requested_features_repository
        self.feature_codes_repository = feature_codes_repository
        self.llm = llm
    
    def feedbacks(self, data):
        # data validation
        FeedbackInputSchema().validate_data(data)
        
        feedback_id = data['id']
        feedback = data['feedback']
        
        # check if the feedback is a spam
        spam_validator_prompt = PromptCreator.create_spam_prompt(feedback=feedback)
        llm_spam_response = self.llm.perform_request(prompt=spam_validator_prompt)
        
        # if the feedback is classifies as a spam
        if llm_spam_response['spam'].lower() == 'sim':
            return {'id': feedback_id, 'sentiment': 'SPAM', 'requested_features': []}
        
        # get existing feature codes from the database
        codes = self.feature_codes_repository.get_codes()
        
        # feedback classification
        sentiment_analysis_prompt = PromptCreator.create_sentiment_analysis_prompt(feedback=feedback, codes=str(codes))
        llm_sentiment_analysis_result = self.llm.perform_request(prompt=sentiment_analysis_prompt)
        
        sentiment = llm_sentiment_analysis_result['sentiment']
        requested_features = llm_sentiment_analysis_result['requested_features']
        
            
            
        
        return {}