from __future__ import print_function
from app import app
from flask import render_template, request, jsonify
from .models import db, Client, FeatureRequest
from .dbschema import ClientSchema, FeatureRequestSchema
import sys
from collections import defaultdict

# def update_priorities(new_client_priority, client_id):
#     feature_request_dict = defaultdict()
#     all_requests = FeatureRequest.query.filter_by(client_id = client_id);

#     for request in all_requests:
#         feature_request_dict.setdefault(request.client_priority, request.id)

#     if new_client_priority not in feature_request_dict.keys():
#         return

#     j = new_client_priority

#     while j in feature_request_dict.keys():
#         j += 1

#     while j > new_client_priority:
#         fr_to_change = FeatureRequest.query.get(feature_request_dict[j - 1])
#         fr_to_change.client_priority = j
#         db.session.add(fr_to_change)
#         j -= 1

#     db.session.commit()

#     return

def update_priorities(new_priority, client_id):
    req = FeatureRequest.query.filter(FeatureRequest.client_id == client_id, FeatureRequest.client_priority >= new_priority).order_by(FeatureRequest.client_priority).all()
    i = int(new_priority)
    for f in req:
        f.client_priority = i + 1
        i += 1
        db.session.commit()

@app.route('/api/clients/', methods=('GET',))
def get_clients():
    clients = Client.query.all()
    clients_schema = ClientSchema()
    result = clients_schema.dump(clients, many=True)
    return jsonify({'clients': result.data})

@app.route('/api/feature_requests/<int:id>/', methods=('POST',))
def update_feature_request(id=None):
    if not id:
        return jsonify(
            {"message": "No id found."}
        ), 400

    json_data = request.get_json() or {}
    feature_request = FeatureRequest.query.get(id)

    if not feature_request:
        return jsonify(
            {"message": "Feature request not found."}
        ), 400

    feature_requests_schema = FeatureRequestSchema()

    data = feature_requests_schema.load(json_data)

    if not data:
        return jsonify({"errors": data}), 400

    update_priorities(json_data['client_priority'], json_data['client_id'])
    feature_request.from_dict(json_data)
    db.session.add(feature_request)
    db.session.commit()

    return jsonify(
        {
            "message": "Updated feature request.",
            "data": FeatureRequestSchema().dump(feature_request)
        }
    ), 200


@app.route('/api/feature_requests/add/', methods=('POST',))
def add_feature_request():
    feature_requests_schema = FeatureRequestSchema()
    json_data = request.get_json() or {}
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
        
    data = feature_requests_schema.load(json_data)

    if not data:
        return jsonify({"errors": data}), 400

    update_priorities(json_data['client_priority'], json_data['client_id'])
    feature_request = FeatureRequest()
    feature_request.from_dict(json_data)
    
    db.session.add(feature_request)
    db.session.commit()

    return jsonify(
        {
            "message": "Created new feature request.",
            "data": FeatureRequestSchema().dump(feature_request)
        }
    ), 201
