import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mysql.connector import Error
from schema.feedback_input_schema import FeedbackInputSchema
from prompts.prompt_creator import PromptCreator
from entities.feature_code import FeatureCode
from entities.feedback import Feedback
from entities.requested_feature import RequestedFeature
import smtplib
from marshmallow import ValidationError
from datetime import datetime, timedelta
import json

class FeedbackService():
    def __init__(
        self,
        db_connection,
        feedback_repository,
        requested_features_repository,
        feature_codes_repository,
        llm,
        email_sender
    ):
        self.db_connection = db_connection
        self.feedback_repository = feedback_repository
        self.requested_features_repository = requested_features_repository
        self.feature_codes_repository = feature_codes_repository
        self.llm = llm
        self.email_sender = email_sender
    
    def feedbacks(self, data):
        try:
            # Innit transaction
            self.db_connection.connect()
            self.db_connection.start_transaction()

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
            llm_spam_response = json.loads(self.llm.perform_request(prompt=spam_validator_prompt, temperature=0.0))
            
            # if the feedback is classifies as a spam
            if llm_spam_response['spam'].lower() == 'sim':
                return {'id': feedback_id, 'sentiment': 'SPAM', 'requested_features': []}
            
            # get existing feature codes from the database
            codes_tuple = self.feature_codes_repository.get_codes()
            code_names = [code[1] for code in codes_tuple]
            
            # feedback classification
            sentiment_analysis_prompt = PromptCreator.create_sentiment_analysis_prompt(feedback=feedback, codes=str(code_names))
            llm_sentiment_analysis_result = json.loads(self.llm.perform_request(prompt=sentiment_analysis_prompt, temperature=0.0))

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
                    codes_tuple = self.feature_codes_repository.get_codes()
                
                for code in codes_tuple:
                    code_id = code[0]
                    code_name = code[1]
                    
                    if feature_code == code_name:
                        new_code_id = code_id
                print('CODE ID: ', new_code_id)
                        
                # insert requested feature in the database
                requested_feature = RequestedFeature(feature=reason, code_id=new_code_id, feedback_id=feedback_id)
                self.requested_features_repository.insert_requested_feature(requested_feature=requested_feature)
            
            # commit
            self.db_connection.commit()

            return {
                'id': feedback_id,
                'sentiment': sentiment,
                'requested_features': requested_features
            }
        except ValueError as e:
            # rollback
            self.db_connection.rollback()
            raise ValueError(str(e)) from e
        except ValidationError as e:
            # rollback
            self.db_connection.rollback()
            raise ValidationError(str(e)) from e
        except Error as e:
            # rollback
            self.db_connection.rollback()
            raise Error(str(e)) from e
        except Exception as e:
            # rollback
            self.db_connection.rollback()
            raise Exception(str(e)) from e

    def feedbacks_report(self):
        try:
            # get sentiment percentages
            sentiment_percentages_db = self.feedback_repository.get_feedbacks_sentiment_percentage()
            sentiment_percentages_dict = {sentiment[0]: round(float(sentiment[1]),1) for sentiment in sentiment_percentages_db}
            
            # get main requested features
            requested_features_db = self.requested_features_repository.get_requested_features_percentage()
            requested_features_dict = {rf[0]: round(float(rf[1]),1) for rf in requested_features_db}
            
            return {
                'sentiment_percentages_dict': sentiment_percentages_dict,
                'requested_features_dict': requested_features_dict
            }
        except ValueError as e:
            raise ValueError(str(e)) from e
        except Error as e:
            raise Error(str(e)) from e
        except Exception as e:
            raise Exception(str(e)) from e
    
    def weekly_summary(self):
        try:
            # Calculates the date 7 days ago
            seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            
            # get sentiment percentages from the last 7 days
            sentiment_percentages_db = self.feedback_repository.get_feedbacks_sentiment_percentage(time_period=seven_days_ago)
            
            # if there are no feedbacks within the last 7 days, send an email informing this
            if sentiment_percentages_db:
                sentiment_percentages_dict = {sentiment[0]: float(sentiment[1]) for sentiment in sentiment_percentages_db}
                if 'INCONCLUSIVO' in sentiment_percentages_dict:
                    sentiment_percentages_dict.pop('INCONCLUSIVO')
            else:
                self.email_sender.send('Prezados,\nInformo que não recebemos nenhum feedback nos últimos 7 dias.\nAtenciosamente,\nAlumind Bot')
                return
            
            # get the requested features from the last 7 days
            requested_features_db = self.requested_features_repository.get_requested_features(time_period=seven_days_ago)
            requested_features_dict = {}
            for rf in requested_features_db:
                if rf[2] not in requested_features_dict:
                    requested_features_dict[rf[2]] = rf[1]
                else:
                    requested_features_dict[rf[2]] += '; ' + rf[1]
            
            # email prompt and llm response
            email_prompt = PromptCreator.create_email_prompt(
                feedback_percentages=str(sentiment_percentages_dict),
                requested_features=str(requested_features_dict)
            )
            email = self.llm.perform_request(prompt=email_prompt)
            
            # send email
            self.email_sender.send(email)
        except smtplib.SMTPException as e:
            raise smtplib.SMTPException(str(e))
        except Error as e:
            raise Error(str(e)) from e
        except Exception as e:
            raise Exception(str(e)) from e