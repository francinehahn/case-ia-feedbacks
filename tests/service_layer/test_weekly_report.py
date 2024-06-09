from src.service.feedback_service import FeedbackService


# Only INCONCLUSIVO feedback data available for the last 7 days
def test_email_being_sent_with_feedback_data_last_7_days(mocker):
    # Mock dependencies
    feedback_repository = mocker.Mock()
    requested_features_repository = mocker.Mock()
    feature_codes_repository = mocker.Mock()
    llm = mocker.Mock()
    email_sender = mocker.Mock()

    # Initialize the service
    service = FeedbackService(
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm,
        email_sender=email_sender
    )

    # Mock repository methods to return empty data
    feedback_repository.get_feedbacks_sentiment_percentage.return_value = [('POSITIVO', 70.0), ('NEGATIVO', 20.0), ('INCONCLUSIVO', 10.0)]
    requested_features_repository.get_requested_features.return_value = [
        (1, 'EDITAR_PERFIL', 'Possibilidade de ediar o perfil na plataforma'),
        (1, 'FILTRAR_MEDITACOES_POR_DURACAO', 'Possibilidade de filtrar as meditações de acordo com a duração')
    ]

    # Call the method
    service.weekly_summary()

    # Assert the repository methods were called
    feedback_repository.get_feedbacks_sentiment_percentage.assert_called_once()
    requested_features_repository.get_requested_features.assert_called_once()

    # Assert the LLM and email sender were called
    llm.perform_request.assert_called_once()
    email_sender.send.assert_called_once()

# Only INCONCLUSIVO feedback data available for the last 7 days
def test_only_inconclusivo_feedback_data_last_7_days(mocker):
    # Mock dependencies
    feedback_repository = mocker.Mock()
    requested_features_repository = mocker.Mock()
    feature_codes_repository = mocker.Mock()
    llm = mocker.Mock()
    email_sender = mocker.Mock()

    # Initialize the service
    service = FeedbackService(
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm,
        email_sender=email_sender
    )

    # Mock repository methods to return empty data
    feedback_repository.get_feedbacks_sentiment_percentage.return_value = [('INCONCLUSIVO', 100)]
    requested_features_repository.get_requested_features.return_value = []

    # Call the method
    service.weekly_summary()

    # Assert the repository methods were called
    feedback_repository.get_feedbacks_sentiment_percentage.assert_called_once()
    requested_features_repository.get_requested_features.assert_called_once()

    # Assert the LLM and email sender were called
    llm.perform_request.assert_called_once()
    email_sender.send.assert_called_once()


# No feedback data available for the last 7 days
def test_no_feedback_data_last_7_days(mocker):
    # Mock dependencies
    feedback_repository = mocker.Mock()
    requested_features_repository = mocker.Mock()
    feature_codes_repository = mocker.Mock()
    llm = mocker.Mock()
    email_sender = mocker.Mock()

    # Initialize the service
    service = FeedbackService(
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository,
        feature_codes_repository=feature_codes_repository,
        llm=llm,
        email_sender=email_sender
    )

    # Mock repository methods to return empty data
    feedback_repository.get_feedbacks_sentiment_percentage.return_value = []
    requested_features_repository.get_requested_features.return_value = []

    # Call the method
    service.weekly_summary()

    # Assert the repository methods were called
    feedback_repository.get_feedbacks_sentiment_percentage.assert_called_once()
    requested_features_repository.get_requested_features.assert_called_once()

    # Assert the LLM and email sender were called
    llm.perform_request.assert_called_once()
    email_sender.send.assert_called_once()
    
