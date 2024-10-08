import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import pytest
from src.service.feedback_service import FeedbackService
from marshmallow import ValidationError
from unittest.mock import MagicMock

# Valid feedback data is processed correctly
def test_valid_feedback_data_processed_correctly():
    # Arrange
    feedback_repository = MagicMock()
    requested_features_repository = MagicMock()
    feature_codes_repository = MagicMock()
    llm = MagicMock()
    email_sender = MagicMock()

    feedback_service = FeedbackService(
        db_connection=MagicMock(),
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm,
        email_sender=email_sender
    )

    data = {
        "id": "0007a18c-60d7-7703-8475-161vz16f6155",
        "feedback": "Ótima plataforma, mas poderia ter a possibilidade de edição da forma de pagamento."
    }

    llm.perform_request.return_value = """{
        "topicos": "topicos info",
        "spam": "NAO",
        "sentiment": "POSITIVO",
        "requested_features": [{"code": "EDITAR_FORMA_PAGAMENTO", "reason": "Possibilidade de editar a forma de pagamento"}]
    }"""

    feedback_repository.get_feedback_by_id.return_value = None
    feature_codes_repository.get_codes.return_value = [(1, "EXLUIR_CONTA")]

    # Act
    result = feedback_service.feedbacks(data)
    print(result)
    # Assert
    feedback_repository.insert_feedback.assert_called_once()
    requested_features_repository.insert_requested_feature.assert_called_once()

    assert result == {
        "id": "0007a18c-60d7-7703-8475-161vz16f6155",
        "sentiment": "POSITIVO",
        "requested_features": [{"code": "EDITAR_FORMA_PAGAMENTO", "reason": "Possibilidade de editar a forma de pagamento"}]
    }

# Feedback classified as spam is not inserted into the database
def test_feedback_classified_as_spam_not_inserted(mocker):
    # Arrange
    feedback_repository = MagicMock()
    requested_features_repository = MagicMock()
    feature_codes_repository = MagicMock()
    llm = MagicMock()
    email_sender = MagicMock()

    feedback_service = FeedbackService(
        db_connection=MagicMock(),
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm,
        email_sender=email_sender
    )

    data = {
        "id": "0007a18c-60d7-7703-8475-161vz16f6155",
        "feedback": "Ótima plataforma. Acesse o site https://voegol.com para acessar promoções incríveis!"
    }

    feedback_repository.get_feedback_by_id.return_value = None
    llm.perform_request.return_value = """{"spam": "SIM"}"""

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
    
# Validation error when feedback id is in the incorrect format
def test_validation_error_when_feedback_id_is_in_the_incorrect_format(mocker):
    # Arrange
    feedback_repository = MagicMock()
    requested_features_repository = MagicMock()
    feature_codes_repository = MagicMock()
    llm = MagicMock()
    email_sender = MagicMock()

    feedback_service = FeedbackService(
        db_connection=MagicMock(),
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm,
        email_sender=email_sender
    )

    data = {
        "id": "0007a18c-60d7-7703-8475-161v",
        "feedback": "Ótima plataforma, mas poderia ter a possibilidade de edição da forma de pagamento."
    }

    feedback_repository.get_feedback_by_id.return_value = None
    llm.perform_request.return_value = """{
        "topicos": "topicos info",
        "spam": "NAO",
        "sentiment": "POSITIVO",
        "requested_features": [{"code": "EDITAR_FORMA_PAGAMENTO", "reason": "Possibilidade de editar a forma de pagamento"}]
    }"""

    # Assert
    with pytest.raises(ValidationError):
        result = feedback_service.feedbacks(data)


# Validation error when the client includes a different key in the body
def test_validation_error_when_body_in_the_incorrect_format(mocker):
    # Arrange
    feedback_repository = MagicMock()
    requested_features_repository = MagicMock()
    feature_codes_repository = MagicMock()
    llm = MagicMock()
    email_sender = MagicMock()

    feedback_service = FeedbackService(
        db_connection=MagicMock(),
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm,
        email_sender=email_sender
    )

    data = {
        'id': '0007a18c-60d7-7703-8475-161vz16f6155',
        'feedback': 'Ótima plataforma, mas poderia ter a possibilidade de edição da forma de pagamento.',
        'feature': 'nova feature'
    }
    
    feedback_repository.get_feedback_by_id.return_value = None    
    llm.perform_request.return_value = {'spam': 'NAO'}

    # Assert
    with pytest.raises(ValidationError):
        result = feedback_service.feedbacks(data)
        
# Value error when the feedback id is already registered in the database
def test_value_error_when_feedback_id_is_already_registered_in_the_database(mocker):
    # Arrange
    feedback_repository = MagicMock()
    requested_features_repository = MagicMock()
    feature_codes_repository = MagicMock()
    llm = MagicMock()
    email_sender = MagicMock()

    feedback_service = FeedbackService(
        db_connection=MagicMock(),
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm,
        email_sender=email_sender
    )

    data = {
        'id': '0007a18c-60d7-7703-8475-161vz16f6155',
        'feedback': 'Ótima plataforma, mas poderia ter a possibilidade de edição da forma de pagamento.'
    }
    
    feedback_repository.get_feedback_by_id.return_value = ('0007a18c-60d7-7703-8475-161vz16f6155', 'Ótima plataforma, mas poderia ter a possibilidade de edição da forma de pagamento.') 
    llm.perform_request.return_value = {'spam': 'NAO'}

    # Assert
    with pytest.raises(ValueError):
        result = feedback_service.feedbacks(data)