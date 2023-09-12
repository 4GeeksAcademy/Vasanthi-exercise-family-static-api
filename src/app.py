"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "age": 35,
    "first_name": 'Jane',
    "lucky_numbers": [10, 14, 3],
    "last_name": jackson_family.last_name,
    "id": jackson_family._generateId(),
})
jackson_family.add_member({
    "first_name": 'John',
    "age": 33,
    "lucky_numbers": [7, 13, 22],
    "last_name": jackson_family.last_name,
    "id": jackson_family._generateId(),
})
jackson_family.add_member({
    "first_name": 'Jimmy',
    "age": 5,
    "lucky_numbers": [1],
    "last_name": jackson_family.last_name,
    "id": jackson_family._generateId(),
})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_single_family_member(member_id):
    get_member = jackson_family.get_member(member_id)
    if get_member is not None:
      return jsonify(get_member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route('/member', methods=['POST'])
def create_member():
    member = request.get_json(force=True)
    member_obj = {
            "fist_name": member['first_name'],
             "last_name": jackson_family.last_name,
             "id": jackson_family._generateId(),
             "age": member['age'],
             "lucky_numbers": member['lucky_numbers']
        }
    jackson_family.add_member(member)
    return f'you successfully added {member["first_name"]} {jackson_family.last_name} to the list', 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    members = jackson_family.delete_member(member_id)
    return jsonify(members), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
