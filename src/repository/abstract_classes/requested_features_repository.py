from abc import ABC, abstractmethod

class RequestedFeaturesRepository(ABC):
    @abstractmethod
    def insert_requested_feature(self, requested_feature):
        pass