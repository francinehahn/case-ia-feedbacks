from src.repository.abstract_classes.requested_features_repository import RequestedFeaturesRepository

class RequestedFeaturesMySQL(RequestedFeaturesRepository):
    def __init__(self, connection):
        self.connection = connection