from marshmallow import Schema, fields, validates, ValidationError

class FeedbackInputSchema(Schema):
    id = fields.String(required=True)
    feedback = fields.String(required=True)

    @validates('id')
    def validate_id(self, id):
        try:
            if len(id) < 36:
                raise ValidationError('The id must have 36 characters.')
        except ValidationError as e:
            raise ValidationError(e.messages) from e
        
    def validate_data(self, data):
        try:
            self.load(data)
        except ValidationError as e:
            raise ValidationError(e.messages) from e