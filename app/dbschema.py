from marshmallow import validate, Schema, fields

class FeatureRequestSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=[validate.Length(min=6, max=255)])
    description = fields.Str(required=True)
    client_id = fields.Int(required=True, load_from="client")
    client_priority = fields.Int(required=True, validate=[validate.Range(min=1)])
    target_date = fields.Str(required=True, validate=[validate.Length(min=4, max=65)])
    product_area = fields.Str(required=True, validate=[validate.Length(min=4, max=65)])

class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    feature_requests = fields.Nested(FeatureRequestSchema, many=True)
