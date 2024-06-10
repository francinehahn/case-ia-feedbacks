class Feedback:
    def __init__(self, id:str, feedback:str, sentiment:str):
        self.id = id
        self.feedback = feedback
        self.sentiment = sentiment
    
    def get_id(self):
        return self.id
    
    def get_feedback(self):
        return self.feedback
    
    def get_sentiment(self):
        return self.sentiment