from flask import Flask, jsonify, request
from src.controller.feedback_controller import FeedbackController
from src.service.feedback_service import FeedbackService
from src.repository.implementations.feedback_mysql import FeedbackMySQL
from src.repository.implementations.requested_features_mysql import RequestedFeaturesMySQL
from src.db.connection import DatabaseConnection

app = Flask(__name__)

@app.route('/feedbacks', methods=['POST'])
def feedbacks():
    # get data from the client
    feedback_data = request.get_json()
    
    # database connection
    db_connection = DatabaseConnection()
    
    # repository layer
    feedback_repository = FeedbackMySQL(connection=db_connection)
    requested_features_repository = RequestedFeaturesMySQL(connection=db_connection)
    
    # service layer
    feedback_service = FeedbackService(
        feedback_repository=feedback_repository,
        requested_features_repository=requested_features_repository
    )
    
    # controller layer
    feedback_controller = FeedbackController(feedback_service=feedback_service)
    feedback = feedback_controller.feedbacks(feedback_data)
    
    return jsonify(feedback), 201

if __name__ == '__main__':
    app.run(debug=True)