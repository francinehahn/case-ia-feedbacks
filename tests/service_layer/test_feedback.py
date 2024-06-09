import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import pytest
from src.schema.feedback_input_schema import FeedbackInputSchema
from src.repository.abstract_classes.feature_codes_repository import FeatureCodesRepository
from src.repository.abstract_classes.feedback_repository import FeedbackRepository
from src.repository.abstract_classes.requested_features_repository import RequestedFeaturesRepository
from src.service.feedback_service import FeedbackService
from src.ai.abstract_classes.LLM import LLM

# Valid feedback data is processed correctly
def test_valid_feedback_data_processed_correctly(mocker):
    # Arrange
    feedback_repository = mocker.Mock(spec=FeedbackRepository)
    requested_features_repository = mocker.Mock(spec=RequestedFeaturesRepository)
    feature_codes_repository = mocker.Mock(spec=FeatureCodesRepository)
    llm = mocker.Mock(spec=LLM)

    feedback_service = FeedbackService(
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm
    )

    data = {
        'id': '0007a18c-60d7-7703-8475-161vz16f6155',
        'feedback': 'Ótima plataforma, mas poderia ter a possibilidade de edição da forma de pagamento.'
    }

    llm.perform_request.side_effect = [
        {'spam': 'NAO'},
        {'sentiment': 'POSITIVO', 'requested_features': [{'code': 'EDITAR_FORMA_PAGAMENTO', 'reason': 'Possibilidade de editar a forma de pagamento'}]}
    ]

    feature_codes_repository.get_codes.return_value = [(1, 'EXLUIR_CONTA')]

    # Act
    result = feedback_service.feedbacks(data)

    # Assert
    feedback_repository.insert_feedback.assert_called_once()
    requested_features_repository.insert_requested_feature.assert_called_once()

    assert result == {
        'id': '0007a18c-60d7-7703-8475-161vz16f6155',
        'sentiment': 'POSITIVO',
        'requested_features': [{'code': 'EDITAR_FORMA_PAGAMENTO', 'reason': 'Possibilidade de editar a forma de pagamento'}]
    }

# Feedback classified as spam is not inserted into the database
def test_feedback_classified_as_spam_not_inserted(mocker):
    # Arrange
    feedback_repository = mocker.Mock(spec=FeedbackRepository)
    requested_features_repository = mocker.Mock(spec=RequestedFeaturesRepository)
    feature_codes_repository = mocker.Mock(spec=FeatureCodesRepository)
    llm = mocker.Mock(spec=LLM)

    feedback_service = FeedbackService(
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm
    )

    data = {
        'id': '0007a18c-60d7-7703-8475-161vz16f6155',
        'feedback': 'Ótima plataforma. Acesse o site https://voegol.com para acessar promoções incríveis!'
    }

    llm.perform_request.return_value = {'spam': 'SIM'}

    # Act
    result = feedback_service.feedbacks(data)

    # Assert
    llm.perform_request.assert_called_once()
    feedback_repository.insert_feedback.assert_not_called()
    requested_features_repository.insert_requested_feature.assert_not_called()

    assert result == {
        'id': '0007a18c-60d7-7703-8475-161vz16f6155',
        'sentiment': 'SPAM',
        'requested_features': []
    }
    
