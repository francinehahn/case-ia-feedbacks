import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repository.abstract_classes.feedback_repository import FeedbackRepository
from repository.abstract_classes.requested_features_repository import RequestedFeaturesRepository
from ai.abstract_classes.LLM import LLM
from schema.feedback_input_schema import FeedbackInputSchema
from prompts.prompt_creator import PromptCreator
import json

class FeedbackService():
    def __init__(
        self,
        feedback_repository:FeedbackRepository,
        requested_features_repository:RequestedFeaturesRepository,
        llm:LLM
    ):
        self.feedback_repository = feedback_repository
        self.requested_features_repository = requested_features_repository
        self.llm = llm
    
    def feedbacks(self, data):
        # data validation
        FeedbackInputSchema().validate_data(data)
        
        feedback_id = data['id']
        feedback = data['feedback']
        
        # check if the feedback is a spam
        spam_validator_prompt = PromptCreator.create_spam_prompt(feedback=feedback)
        llm_response = self.llm.perform_request(prompt=spam_validator_prompt)
        print(llm_response)
        

        return llm_response