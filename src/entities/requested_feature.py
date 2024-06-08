class RequestedFeature:
    def __init__(self, feature: str, code_id: int, feedback_id: str):
        self.feature = feature
        self.code_id = code_id
        self.feedback_id = feedback_id
        
    def get_feature(self):
        return self.feature
    
    def get_code_id(self):
        return self.code_id

    def get_feedback_id(self):
        return self.feedback_id