from src.repository.abstract_classes.feedback_repository import FeedbackRepository

class FeedbackMySQL(FeedbackRepository):
    def __init__(self, connection):
        self.connection = connection