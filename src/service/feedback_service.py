import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mysql.connector import Error
from repository.abstract_classes.feedback_repository import FeedbackRepository
from repository.abstract_classes.requested_features_repository import RequestedFeaturesRepository
from repository.abstract_classes.feature_codes_repository import FeatureCodesRepository
from ai.abstract_classes.LLM import LLM
from schema.feedback_input_schema import FeedbackInputSchema
from prompts.prompt_creator import PromptCreator
from entities.feature_code import FeatureCode
from entities.feedback import Feedback
from entities.requested_feature import RequestedFeature
from marshmallow import ValidationError

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
        try:
            # data validation
            FeedbackInputSchema().validate_data(data)
            
            feedback_id = data['id']
            feedback = data['feedback']
            
            # check if the feedback id already exists in the database
            feedback_data_db = self.feedback_repository.get_feedback_by_id(feedback_id=feedback_id)
            
            if feedback_data_db:
                raise ValueError('Feedback id already registered in the database.')
                
            # check if the feedback is a spam
            spam_validator_prompt = PromptCreator.create_spam_prompt(feedback=feedback)
            llm_spam_response = self.llm.perform_request(prompt=spam_validator_prompt)
            
            # if the feedback is classifies as a spam
            if llm_spam_response['spam'].lower() == 'sim':
                return {'id': feedback_id, 'sentiment': 'SPAM', 'requested_features': []}
            
            # get existing feature codes from the database
            codes_tuple = self.feature_codes_repository.get_codes()
            code_names = [code[1] for code in codes_tuple]
            
            # feedback classification
            sentiment_analysis_prompt = PromptCreator.create_sentiment_analysis_prompt(feedback=feedback, codes=str(code_names))
            llm_sentiment_analysis_result = self.llm.perform_request(prompt=sentiment_analysis_prompt)

            # get sentiment analysis results from the llm
            sentiment = llm_sentiment_analysis_result['sentiment']
            requested_features = llm_sentiment_analysis_result['requested_features']
            
            # insert feedback in the database
            feedback_entity = Feedback(id=feedback_id, feedback=feedback, sentiment=sentiment)
            self.feedback_repository.insert_feedback(feedback=feedback_entity)
            
            # go over all the requested features
            for feature in requested_features:
                feature_code = feature['code']
                reason = feature['reason']
                new_code_id = None
                
                # if the feature_code does not exist in the database -> insert it
                if feature_code not in code_names:
                    new_code = FeatureCode(code=feature_code)
                    self.feature_codes_repository.insert_code(new_code)
                    new_code_id = int(codes_tuple[-1][0]) + 1 if len(code_names) > 0 else 1
                else:
                    for code in codes_tuple:
                        code_id = code[0]
                        code_name = code[1]
                        
                        if feature_code == code_name:
                            new_code_id = code_id
                            
                # insert requested feature in the database
                requested_feature = RequestedFeature(feature=reason, code_id=new_code_id, feedback_id=feedback_id)
                self.requested_features_repository.insert_requested_feature(requested_feature=requested_feature)
            
            return {
                'id': feedback_id,
                'sentiment': sentiment,
                'requested_features': requested_features
            }
        
        except ValueError as e:
            raise ValueError(str(e)) from e
        except ValidationError as e:
            raise ValidationError(str(e)) from e
        except Error as e:
            raise Error(str(e)) from e
        except Exception as e:
            raise Exception(str(e)) from e