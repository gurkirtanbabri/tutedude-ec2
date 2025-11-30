from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

mongo_uri = os.getenv('MONGO_URI')
port = os.getenv('PORT')

client = MongoClient(mongo_uri)
db = client.test # Uses the database name from the URI
todos_collection = db.todos

def serialize_todo(todo):
    return {
        'id': str(todo['_id']),
        'text': todo['text'],
        'completed': todo['completed']
    }

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = todos_collection.find()
    return jsonify([serialize_todo(todo) for todo in todos])

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    todo = {
        'text': data['text'],
        'completed': False
    }
    result = todos_collection.insert_one(todo)
    todo['_id'] = result.inserted_id
    return jsonify(serialize_todo(todo)), 201

@app.route('/api/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    update_data = {}
    if 'text' in data:
        update_data['text'] = data['text']
    if 'completed' in data:
        update_data['completed'] = data['completed']
    
    if not update_data:
        return jsonify({'error': 'No data to update'}), 400

    try:
        result = todos_collection.find_one_and_update(
            {'_id': ObjectId(todo_id)},
            {'$set': update_data},
            return_document=True
        )
        if result:
            return jsonify(serialize_todo(result))
        return jsonify({'error': 'Todo not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID'}), 400

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        result = todos_collection.delete_one({'_id': ObjectId(todo_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'Todo deleted'}), 200
        return jsonify({'error': 'Todo not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=port, host='0.0.0.0')
